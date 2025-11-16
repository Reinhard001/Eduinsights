# backend/students/serializers.py
from rest_framework import serializers
from .models import Student, PerformanceRecord


class PerformanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceRecord
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    records = PerformanceRecordSerializer(many=True, read_only=True)
    
    class Meta:
        model = Student
        fields = ["id", "student_id", "full_name", "age", "gender", "records"]
