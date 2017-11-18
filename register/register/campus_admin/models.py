from django.db import models
from register.course.models import OfferedIn, course
from register.student.models import student

class Courses(models.Model):
    courseNo = models.CharField(max_length = 10, default = '',primary_key = True)
    courseName = models.CharField(max_length = 100, default = '')
    credits = models.IntegerField(default = 0)

    def __str__(self):
        return self.courseNo

class Registers(models.Model):
    studentId = models.ForeignKey(student,related_name='student_id+',null=True)
    acadYear = models.ForeignKey(OfferedIn,related_name='acadYear+',null=True)
    semesterNo = models.ForeignKey(OfferedIn, related_name='semester+', null=True)
    courseNo = models.ForeignKey(course, related_name='courseNo+', null=True)
    grade = models.CharField(max_length=4,null=True,blank=True)

    class Meta:
        unique_together = (('acadYear','semesterNo','courseNo','studentId'),)


class Offers(models.Model):
    acadYear = models.ForeignKey(OfferedIn, related_name='acadYear+', null=True)
    semesterNo = models.ForeignKey(OfferedIn, related_name='semester+', null=True)
    courseNo = models.ForeignKey(course, related_name='courseNo+', null=True)

    class Meta:
        unique_together = (('acadYear','semesterNo','courseNo'),)


class FeeReceipt(models.Model):
    studentId = models.ForeignKey(student,related_name='student_id+',null=False,default="0")
    acadYear = models.ForeignKey(OfferedIn, related_name='acadYear+', null=True)
    semesterNo = models.ForeignKey(OfferedIn, related_name='semester+', null=True)
    receiptId = models.CharField(max_length=30,null=False,blank=True,default="0")
    status = models.CharField(max_length=50,null=False,blank=True,default='Not Paid')

    class Meta:
        unique_together = (('acadYear','semesterNo','studentId'),)


class Result(models.Model):
    studentId = models.ForeignKey(student, related_name='student_id+')
    acadYear = models.ForeignKey(OfferedIn, null=True, related_name='acadYear+')
    semesterNo = models.ForeignKey(OfferedIn, null=True, related_name='semester+')
    SPI = models.FloatField(default='',blank=True,null=True)

