# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import course

def course_list_of_faculty(request):
    courses_of_current_faculty = course.objects.all()
    print(courses_of_current_faculty.query)
    # print(courses_of_current_faculty.count())
    return render(request,
                  'course_list_of_current_faculty.html',
                  {'courses_of_current_faculty': courses_of_current_faculty})