import json
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from .models import Student


class StudentModelTest(TestCase):
    """Tests for the Student model"""

    def setUp(self):
        """setUp runs before each test — creates fresh test data"""
        self.student = Student.objects.create(
            name   = "Arjun Sharma",
            course = "B.Tech CSE",
            email  = "arjun@college.edu"
        )

    def test_student_creation(self):
        """Test that a student is created correctly"""
        self.assertEqual(self.student.name, "Arjun Sharma")
        self.assertEqual(self.student.course, "B.Tech CSE")
        self.assertEqual(self.student.email, "arjun@college.edu")

    def test_student_str_representation(self):
        """Test the __str__ method"""
        expected = "Arjun Sharma - B.Tech CSE"
        self.assertEqual(str(self.student), expected)

    def test_student_email_is_unique(self):
        """Test that duplicate emails are rejected"""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Student.objects.create(
                name   = "Duplicate User",
                course = "MCA",
                email  = "arjun@college.edu"   # Same email — should fail
            )


class StudentAPITest(TestCase):
    """Tests for the Student REST API endpoints"""

    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(
            name   = "Priya Patel",
            course = "MCA",
            email  = "priya@college.edu"
        )

    def test_get_all_students_returns_200(self):
        """GET /api/students/ should return HTTP 200"""
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, 200)

    def test_get_all_students_returns_list(self):
        """GET /api/students/ should return a list with count"""
        response = self.client.get('/api/students/')
        data = json.loads(response.content)
        self.assertIn('students', data)
        self.assertIn('count', data)
        self.assertEqual(data['count'], 1)

    def test_create_student_returns_201(self):
        """POST /api/students/ with valid data should return HTTP 201"""
        new_student = {
            'name':   'Rahul Kumar',
            'course': 'B.Sc IT',
            'email':  'rahul@college.edu'
        }
        response = self.client.post(
            '/api/students/',
            data        = json.dumps(new_student),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, 201)

    def test_create_student_missing_field_returns_400(self):
        """POST without required fields should return HTTP 400"""
        incomplete_data = {'name': 'Test User'}   # missing course and email
        response = self.client.post(
            '/api/students/',
            data         = json.dumps(incomplete_data),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_get_single_student_returns_200(self):
        """GET /api/students/1/ should return HTTP 200"""
        response = self.client.get(f'/api/students/{self.student.id}/')
        self.assertEqual(response.status_code, 200)

    def test_get_nonexistent_student_returns_404(self):
        """GET /api/students/99999/ should return HTTP 404"""
        response = self.client.get('/api/students/99999/')
        self.assertEqual(response.status_code, 404)