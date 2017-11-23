# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from register.course.models import course
from .forms import AnnouncementForm
from .models import Announcement

# Create your views here.
@login_required
@user_passes_test(lambda u: u.groups.all()[0].name == 'faculty', login_url='/accounts/login/')
def announcement_upload(request, course_no):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            unsaved_form = form.save(commit=False)
        unsaved_form.announcementUser = request.user
        currentCourse = course.objects.get(courseNo=course_no)
        unsaved_form.announcementCourse = currentCourse
        unsaved_form.save()
        return redirect('index')
    else:
        form = AnnouncementForm()

    return render(request, 'announcement_upload.html', {
        'form': form
    })

class AnnouncementView(LoginRequiredMixin ,ListView):
    template_name = 'announcement_view.html'

    def get_queryset(self):
        print(self.kwargs['course_no'])
        return Announcement.objects.filter(announcementUser__username__exact=self.request.user,
                                           announcementCourse__courseNo__exact=self.kwargs['course_no'])