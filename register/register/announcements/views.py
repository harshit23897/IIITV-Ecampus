# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from .forms import AnnouncementForm
from .models import Announcement

# Create your views here.
def announcement_upload(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AnnouncementForm()

    return render(request, 'announcement_upload.html', {
        'form': form
    })

class AnnouncementView(ListView):
    template_name = 'announcement_view.html'
    queryset = Announcement.objects.all()