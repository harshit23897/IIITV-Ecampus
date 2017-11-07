# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.contrib.auth.models import User
from django.db import models

class course(models.Model):
    course_no = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=100, null=True, unique=True)
    faculty = models.ManyToManyField(User)

    def __str__(self):
        return self.course_no

class CourseMaterial(models.Model):
    course_no = models.ForeignKey(course, to_field='course_no', null=True)
    description = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='course/')
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)
    faculty = models.ForeignKey(User, null=True)

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return os.path.basename(self.file.name)

class AssignmentMaterial(models.Model):
    course_no = models.ForeignKey(course, to_field='course_no', null=True)
    description = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='assignment/')
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)
    faculty = models.ForeignKey(User, null=True)

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return os.path.basename(self.file.name)



