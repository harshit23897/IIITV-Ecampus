# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from register.course.models import course

# Create your models here.
class Announcement(models.Model):
    announcement = models.CharField(max_length=500, blank=False, null=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    announcementUser = models.ForeignKey(User, null=True, blank=False)
    announcementCourse = models.ForeignKey(course, null=True, blank=False)