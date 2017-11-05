# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

class course(models.Model):
    course_no = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=100, null=True)
    faculty = models.ManyToManyField(User)

    def __str__(self):
        return self.course_no



