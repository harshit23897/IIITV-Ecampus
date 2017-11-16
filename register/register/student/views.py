# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django import forms
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.db.models import Q
from django.http import Http404
from django.views.generic.list import ListView
from .forms import AssignmentSubmissionForm
from .models import student, AssignmentSubmission

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from register.announcements.models import Announcement
from register.course.models import course, CourseMaterial, AssignmentMaterial, OfferedIn, CoursesInSemester

@login_required
def student_home_page(request):
    student_ = student.objects.filter(student_id=request.user.email[:-19])
    if student_.count() == 0:
        batch = request.user.email[:4]
        batch = batch
        program_ = request.user.email[4:6]
        if program_ == '51':
            program = 'CS'
        else:
            program = 'IT'
        # print(User.objects.get(email=request.user.email))
        student_ = student(user_student=User.objects.get(email=request.user.email),
                           student_id=request.user.email[:-19],
                           program=program,
                           batch=batch)
        student_.save()
        return redirect('student:course_registration_view')
    else:
        student_courses = student.objects.filter(user_student=request.user)[0].course_no.all()
        announcement_in_courses = Announcement.objects.filter(announcementCourse__in=student_courses)
        return render(request,
                      'student_home_page.html',
                      {'student_courses': student_courses,
                       'announcement_in_courses': announcement_in_courses})

class StudentCourseList(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    template_name = "student_course_view.html"

    # def get_extra_context(self, **kwargs):
    #     context = super(StudentCourseList, self).get_context_data(**kwargs)
    #     context['']
    def get_queryset(self):
        return student.objects.filter(user_student=self.request.user)[0].course_no.all()

@login_required
def student_course_detail_view(request, course_no):
    template_name = 'student_course_detail_view.html'
    return render(request,
                  template_name,
                  {'course_no': course_no})

class AnnouncementView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    template_name = "announcement_view.html"

    def get_queryset(self):
        course_name = course.objects.get(courseNo__exact=self.kwargs['course_no'])
        announcements_in_current_course = Announcement.objects.filter(announcementCourse__exact=course_name)
        return announcements_in_current_course

@login_required
def student_assignment_files_list(request, course_no):
    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES)
        current_assignment = AssignmentMaterial.objects.filter(id=request.POST['file.id'])
        assignment_submission = AssignmentSubmission.objects.filter(assignment=current_assignment,
                                                                    student=request.user)
        if (form.is_valid() and
            timezone.now() <= current_assignment.first().submission_last_date and
            assignment_submission.count() == 0):
            unsaved_form = form.save(commit=False)
            current_file = unsaved_form.file
            if current_file.size > 5242880:
                raise forms.ValidationError(_('Please keep filesize under 50 MB'))
            unsaved_form.student = request.user
            unsaved_form.save()
            unsaved_form.assignment.add(current_assignment.first())
            unsaved_form.save()
        elif assignment_submission.count() != 0:
            raise forms.ValidationError(_('You already submitted.'))
        else:
            raise forms.ValidationError(_('The time of assignment submission has passed. Better luck next time.'))
        return redirect('student:student_home_page')
    else:
        material = AssignmentMaterial.objects.filter(course_no=course_no)
        form = AssignmentSubmissionForm()
    return render(request, 'student_assignment_files_list.html', {
        'form': form,
        'assignment_material': material,
        'path': settings.MEDIA_ROOT,
    })

@login_required
@user_passes_test(lambda u: u.groups.all().count() == 0, login_url='/accounts/login/')
def course_registration_view(request):
    if request.method == 'POST':
        print(request.POST.getlist('courses[]'))
        current_student = student.objects.filter(user_student=request.user)
        for selected_course in request.POST.getlist('courses[]'):
            temp = course.objects.filter(courseNo=selected_course)
            current_student[0].course_no.add(temp[0])
        print(current_student[0].course_no)
        return redirect('/')
    else:
        current_student = student.objects.get(user_student=request.user)
        # print('Hello')
        if current_student.course_no.all().count() > 0:
            return redirect('student:student_home_page')
        # print('Hello')
        current_semester = datetime.datetime.now().year - int(current_student.batch)
        current_semester = current_semester * 2 + 1
        # if int(datetime.datetime.now().month) >= 1 and int(datetime.datetime.now().month) <= 5:
        #     current_semester = current_semester + 1
        sem = OfferedIn.objects.filter(semester=current_semester)
        # print('Hello')
        if(sem.count() > 0):
            courses_offered = course.objects.filter(offered_in=sem[0]).order_by('elective')
            courses_offered_in_current_semester = CoursesInSemester.objects.filter(semester=sem[0])
            # print('Hello')
            # print(courses_offered_in_current_semester[0].number_of_core)
            if courses_offered.count() > 0 and courses_offered_in_current_semester.count() > 0:
                return render(request,
                              'course_registration_view.html',
                              {'number_of_core': courses_offered_in_current_semester[0].number_of_core,
                               'number_of_electives': courses_offered_in_current_semester[0].number_of_electives,
                               'courses_offered': courses_offered,
                               'current_semester': current_semester
                               })
            else:
                raise Http404("Page not found.")
        else:
            raise Http404("Page not found.")






