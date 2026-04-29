from django.http import JsonResponse
from django.views import View
from .models import Student
import json

class StudentListView(View):
    """
    GET  /api/students/     → returns list of all students
    POST /api/students/     → creates a new student
    """

    def get(self, request):
        students = list(Student.objects.values(
            'id', 'name', 'course', 'email'
        ))
        return JsonResponse({'students': students, 'count': len(students)})

    def post(self, request):
        try:
            data = json.loads(request.body)
            student = Student.objects.create(
                name   = data['name'],
                course = data['course'],
                email  = data['email'],
            )
            return JsonResponse({
                'id':     student.id,
                'name':   student.name,
                'course': student.course,
                'email':  student.email,
            }, status=201)
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {e}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class StudentDetailView(View):
    """
    GET /api/students/<id>/  → returns one student
    """

    def get(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
            return JsonResponse({
                'id':     student.id,
                'name':   student.name,
                'course': student.course,
                'email':  student.email,
            })
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)