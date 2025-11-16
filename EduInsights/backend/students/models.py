# backend/students/models.py
from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    student_id = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=200)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.student_id})"


class PerformanceRecord(models.Model):
    student = models.ForeignKey(Student, related_name='records', on_delete=models.CASCADE)
    term = models.CharField(max_length=50)
    attendance_rate = models.FloatField(help_text="Percent, 0-100")
    avg_assignment_score = models.FloatField()
    midterm_score = models.FloatField()
    missing_assignments = models.IntegerField()
    participation = models.FloatField()
    lms_hours = models.FloatField()
    final_grade = models.FloatField(null=True, blank=True)  # if available
    passed = models.BooleanField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.full_name} - {self.term}"
