# backend/students/admin.py
from django.contrib import admin
from .models import Student, PerformanceRecord


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'full_name', 'age', 'gender']
    search_fields = ['student_id', 'full_name']
    list_filter = ['gender']


@admin.register(PerformanceRecord)
class PerformanceRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'term', 'attendance_rate', 'avg_assignment_score', 'midterm_score', 'passed', 'created_at']
    search_fields = ['student__student_id', 'student__full_name', 'term']
    list_filter = ['term', 'passed', 'created_at']
    readonly_fields = ['created_at']
