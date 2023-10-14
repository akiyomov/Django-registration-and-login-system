from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Course, Lesson, Enrollment, Attendance
from django.contrib.auth.decorators import login_required
import random
import string
from users.models import Profile

# Function to generate random code
def generate_code(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@login_required
def my_courses(request):
    profile_instance = Profile.objects.get(user=request.user)
    enrollments = Enrollment.objects.filter(student=profile_instance)
    return render(request, 'course/my_courses.html', {'enrollments': enrollments})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course)
    return render(request, 'course/course_detail.html', {'course': course, 'lessons': lessons})

@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    attendance_code = generate_code()

    # Logic to save code and its expiry time in the lesson object
    # Save this to the lesson object, for demonstration, adding as variable
    code_expiry_time = timezone.now() + timedelta(hours=2)

    return render(request, 'course/lesson_detail.html', {'lesson': lesson, 'attendance_code': attendance_code, 'code_expiry_time': code_expiry_time})

@login_required
def mark_attendance(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    user_input_code = request.POST.get('code')  # Assume form field name is 'code'

    # Dummy saved code and expiry time for demonstration
    saved_code = 'ABCD12'  # This should be fetched from the lesson object
    code_expiry_time = timezone.now() + timedelta(hours=2)  # This should be fetched from the lesson object

    if user_input_code == saved_code:
        if timezone.now() <= code_expiry_time:
            Attendance.objects.create(student=request.user, lesson=lesson, is_live_attendance=True)
            return redirect('course/lesson_detail', lesson_id=lesson.id)
        else:
            return redirect('course/lesson_detail', lesson_id=lesson.id)  # Redirect with error message, code expired
    else:
        return redirect('course/lesson_detail', lesson_id=lesson.id)  # Redirect with error message, wrong code

@login_required
def mark_manual_attendance(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    Attendance.objects.create(student=request.user, lesson=lesson, is_live_attendance=False)
    return redirect('course/lesson_detail', lesson_id=lesson.id)
