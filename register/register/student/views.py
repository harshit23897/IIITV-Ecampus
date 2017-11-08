# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404
from django.views.generic.list import ListView
from .models import student

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from register.course.models import course, CourseMaterial, AssignmentMaterial

@login_required
def student_home_page(request):
    student_ = student.objects.filter(student_id=request.user.email[:-19])
    if student_.count() == 0:
        print('Hello')
        batch = request.user.email[:4]
        batch = batch
        program_ = request.user.email[4:6]
        if program_ == '51':
            program = 'CS'
        else:
            program = 'IT'

        student_ = student(user_student=User.objects.get(email=request.user.email),
                           student_id=request.user.email[:-19],
                           program=program,
                           batch=batch)
        student_.save()
        course_set = course.objects.all()
        for courses in course_set:
            student_.course_no.add(courses)
        student_.save()

    return render(request,
                  'student_home_page.html',
                  {})

class StudentCourseList(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    template_name = "student_course_view.html"

    # def get_extra_context(self, **kwargs):
    #     context = super(StudentCourseList, self).get_context_data(**kwargs)
    #     context['']
    def get_queryset(self):
        return student.objects.filter(student_id='201551056')[0].course_no.all()

@login_required
def student_course_detail_view(request, pk):
    template_name = 'student_course_detail_view.html'
    return render(request,
                  template_name,
                  {'pk': pk})
