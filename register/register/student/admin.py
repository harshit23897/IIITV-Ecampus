# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import student, AssignmentSubmission, UserProfile

admin.site.register(student)
admin.site.register(AssignmentSubmission)
admin.site.register(UserProfile)

