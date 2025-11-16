# backend/students/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, dashboard_view, StudentListView, StudentDetailView

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = [
    # Template views
    path('', dashboard_view, name='dashboard'),
    path('students/', StudentListView.as_view(), name='student_list'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    
    # API endpoints
    path("api/", include(router.urls)),
]
