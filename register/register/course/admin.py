# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import course, CourseMaterial, AssignmentMaterial, OfferedIn, CoursesInSemester

# Register your models here.

admin.site.register(course)
admin.site.register(CourseMaterial)
admin.site.register(AssignmentMaterial)
admin.site.register(OfferedIn)
admin.site.register(CoursesInSemester)
