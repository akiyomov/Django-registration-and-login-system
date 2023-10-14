from django.db import models
from users.models import Profile
# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.ForeignKey(Profile, related_name='courses_taught', on_delete=models.CASCADE)
    students = models.ManyToManyField(Profile, through='Enrollment', related_name='courses_enrolled')

    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_live = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} enrolled in {self.course.name}"

class Attendance(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    date_attended = models.DateTimeField(auto_now_add=True)
    is_live_attendance = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} attended {self.lesson.name}"
