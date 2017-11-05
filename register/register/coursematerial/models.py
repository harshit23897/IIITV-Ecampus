import os
from register.course.models import course
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class CourseMaterial(models.Model):
    course_no = models.OneToOneField(course, to_field='course_no')
    description = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='')
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    faculty = models.ForeignKey(User, null=True)

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return os.path.basename(self.file.name)
