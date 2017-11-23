# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from register.course.models import AssignmentMaterial
from register.course.models import course, OfferedIn
from django.core.urlresolvers import reverse

class student(models.Model):
    course_no = models.ManyToManyField(course)
    user_student= models.ForeignKey(User, null=True)
    student_id = models.CharField(max_length=20, null=True, unique=True)
    program = models.CharField(max_length=20, null=True)
    batch = models.CharField(max_length=20, null=True)

    @classmethod
    def create(cls, user_student, student_id, program, batch):
        student = cls(user_student=user_student, student_id=student_id, program=program, batch=batch)
        return student

    def __str__(self):
        return self.student_id

class AssignmentSubmission(models.Model):
    assignment = models.ManyToManyField(AssignmentMaterial)
    file = models.FileField(upload_to='assignment-submission/')
    student = models.ForeignKey(User, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.file.name

class UserProfileManager(models.Manager):
    def get_queryset(self):
        return super(UserProfileManager, self).get_queryset().order_by('phone')

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    image = models.ImageField(null=True, blank=True, height_field='height_field', width_field='width_field')
    height_field = models.IntegerField(default=1944)
    width_field = models.IntegerField(default=2592)
    city = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=20, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.CharField(max_length=100, default='')
    order_byPhone = UserProfileManager()

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('view_profile', kwargs={'course_no': self.course_no})

def create_profile( sender, **kwargs):
    user = kwargs['instance']
    if kwargs['created']:
        user_profile = UserProfile(user=user)
        user_profile.save()

post_save.connect(create_profile, sender = User)







