from django.urls import path
from . import views

app_name = 'course'  # This is to namespace the app, allowing you to use names like 'course:course_detail'

urlpatterns = [
    path('my_courses/', views.my_courses, name='my_courses'),
    path('course_detail/<int:course_id>/', views.course_detail, name='course_detail'),
    path('lesson_detail/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('mark_attendance/<int:lesson_id>/', views.mark_attendance, name='mark_attendance'),
    path('mark_manual_attendance/<int:lesson_id>/', views.mark_manual_attendance, name='mark_manual_attendance'),
]
