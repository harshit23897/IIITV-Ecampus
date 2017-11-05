# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import course

def course_list_of_faculty(request):
    courses_of_current_faculty = course.objects.filter(faculty__username__exact=request.user)
    return render(request,
                  'course_list_of_current_faculty.html',
                  {'courses_of_current_faculty': courses_of_current_faculty})

def course_detail_view(request, pk):
    template_name='course_detail_view.html'
    print('Hello')
    return render(request,
                  template_name,
                  {'pk': pk})

