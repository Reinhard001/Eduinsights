# backend/students/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student, PerformanceRecord
from .serializers import StudentSerializer, PerformanceRecordSerializer
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.db.models import Q, Avg
import joblib
import numpy as np
import os

MODEL_PATH = os.path.join(settings.BASE_DIR, "ml", "model_store", "rf_model.joblib")
FEATURE_ORDER = ["attendance_rate", "avg_assignment_score", "midterm_score", "missing_assignments", "participation", "lms_hours"]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=True, methods=["get"])
    def predict(self, request, pk=None):
        """
        Return prediction and top features for the latest record for this student
        """
        student = self.get_object()
        latest = student.records.first()
        if not latest:
            return Response({"error": "No performance records for student"}, status=404)

        # load model
        if not os.path.exists(MODEL_PATH):
            return Response({"error": "Model not found. Train model first."}, status=500)
        
        model = joblib.load(MODEL_PATH)

        X = np.array([[getattr(latest, f) for f in FEATURE_ORDER]])
        proba = model.predict_proba(X)[0]  # if classifier, order classes
        pred = model.predict(X)[0]
        
        # basic importance: use model.feature_importances_
        importances = model.feature_importances_
        feature_contribs = sorted(zip(FEATURE_ORDER, importances), key=lambda x: x[1], reverse=True)[:3]
        
        # Simple recommendations mapping:
        recs = generate_recommendations(latest, feature_contribs)
        
        return Response({
            "student": student.full_name,
            "prediction": str(pred),
            "probabilities": proba.tolist() if hasattr(model, "predict_proba") else None,
            "top_features": feature_contribs,
            "recommendations": recs
        })


def generate_recommendations(record: PerformanceRecord, top_features):
    """Simple rule-based recommendations based on the top problematic features"""
    recs = []
    
    # if attendance low
    if record.attendance_rate < 75:
        recs.append("Attendance is low. Watch recorded lectures + arrange weekly catch-up with tutor.")
    if record.avg_assignment_score < 60:
        recs.append("Focus on assignment practice: try 3 weekly practice problems and seek feedback.")
    if record.midterm_score < 50:
        recs.append("Midterm performance low: revise core concepts and schedule 2 tutoring sessions.")
    if record.lms_hours < 2:
        recs.append("Increase LMS engagement: spend at least 4 hours/week on course materials.")
    
    if not recs:
        recs.append("Keep up the good work. Maintain current study habits and continue practice.")
    
    return recs


# Template Views
def dashboard_view(request):
    """Main dashboard view showing statistics and at-risk students"""
    # Get all students and their latest records
    students = Student.objects.all()
    total_students = students.count()
    
    # Calculate statistics
    at_risk_students = 0
    performing_well = 0
    at_risk_list = []
    
    for student in students:
        latest_record = student.records.first()
        if latest_record:
            # Simple risk assessment based on thresholds
            is_at_risk = (
                latest_record.attendance_rate < 75 or
                latest_record.avg_assignment_score < 60 or
                latest_record.midterm_score < 50
            )
            if is_at_risk:
                at_risk_students += 1
                student.latest_record = latest_record
                at_risk_list.append(student)
            else:
                performing_well += 1
    
    # Calculate average performance metrics
    records = PerformanceRecord.objects.all()
    avg_metrics = records.aggregate(
        avg_attendance=Avg('attendance_rate'),
        avg_assignment=Avg('avg_assignment_score'),
        avg_midterm=Avg('midterm_score'),
        avg_participation=Avg('participation'),
        avg_lms_hours=Avg('lms_hours')
    )
    
    # Calculate overall average performance
    if avg_metrics['avg_attendance'] and avg_metrics['avg_assignment'] and avg_metrics['avg_midterm']:
        avg_performance = round(
            (avg_metrics['avg_attendance'] + avg_metrics['avg_assignment'] + avg_metrics['avg_midterm']) / 3
        )
    else:
        avg_performance = 0
    
    # Check if model exists
    model_exists = os.path.exists(MODEL_PATH)
    
    # Get recent records
    recent_records = PerformanceRecord.objects.select_related('student').order_by('-created_at')[:5]
    
    context = {
        'total_students': total_students,
        'at_risk_students': at_risk_students,
        'performing_well': performing_well,
        'avg_performance': avg_performance,
        'at_risk_list': at_risk_list[:5],  # Top 5 at-risk students
        'model_exists': model_exists,
        'recent_records': recent_records,
        'avg_attendance': round(avg_metrics['avg_attendance'] or 0, 1),
        'avg_assignment': round(avg_metrics['avg_assignment'] or 0, 1),
        'avg_midterm': round(avg_metrics['avg_midterm'] or 0, 1),
        'avg_participation': round(avg_metrics['avg_participation'] or 0, 1),
        'avg_lms_hours': round(avg_metrics['avg_lms_hours'] or 0, 1),
    }
    
    return render(request, 'dashboard.html', context)


class StudentListView(ListView):
    """List view for all students with search and filter"""
    model = Student
    template_name = 'student_list.html'
    context_object_name = 'students'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Student.objects.all().prefetch_related('records')
        
        # Add latest record and prediction status to each student
        for student in queryset:
            student.latest_record = student.records.first()
            if student.latest_record:
                # Simple risk assessment
                is_at_risk = (
                    student.latest_record.attendance_rate < 75 or
                    student.latest_record.avg_assignment_score < 60 or
                    student.latest_record.midterm_score < 50
                )
                student.prediction_status = 'at_risk' if is_at_risk else 'performing_well'
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(full_name__icontains=search_query) |
                Q(student_id__icontains=search_query)
            )
        
        # Filter by status
        status_filter = self.request.GET.get('status', '')
        if status_filter:
            filtered_students = []
            for student in queryset:
                if hasattr(student, 'prediction_status') and student.prediction_status == status_filter:
                    filtered_students.append(student.id)
            queryset = queryset.filter(id__in=filtered_students)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['status_filter'] = self.request.GET.get('status', '')
        return context


class StudentDetailView(DetailView):
    """Detail view for a single student with predictions"""
    model = Student
    template_name = 'student_detail.html'
    context_object_name = 'student'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()
        
        # Get all performance records
        context['records'] = student.records.all()
        context['has_records'] = student.records.exists()
        
        return context
