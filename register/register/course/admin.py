# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import course, CourseMaterial

# Register your models here.

admin.site.register(course)
admin.site.register(CourseMaterial)
