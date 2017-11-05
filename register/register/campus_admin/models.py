from django.db import models


class Semester(models.Model):
    acadYear = models.CharField(default='',max_length=200)
    semesterNo = models.IntegerField(default='')

    class Meta:
        unique_together = (('acadYear', 'semesterNo'),)


class Courses(models.Model):
    courseNo = models.CharField(max_length = 10, default = '',primary_key = True)
    courseName = models.CharField(max_length = 100, default = '')
    credits = models.IntegerField(default = 0)

    def __str__(self):
        return self.courseNo


class Student(models.Model):
    studentId = models.IntegerField(default=0, primary_key=True)
    studentName = models.CharField(max_length=100, default='')
    batch = models.CharField(default = '',max_length=20)
    programName = models.CharField(max_length=20,default='',null=True)

    def __str__(self):
        return self.studentName


class Registers(models.Model):
    studentId = models.ForeignKey(Student,related_name='%(class)s_studentId',null=True)
    acadYear = models.ForeignKey(Semester,related_name='acadYear+',null=True)
    semesterNo = models.ForeignKey(Semester, related_name='semesterNo+', null=True)
    courseNo = models.ForeignKey(Courses, related_name='courseNo+', null=True)
    grade = models.CharField(max_length=4,null=True,blank=True)

    class Meta:
        unique_together = (('acadYear','semesterNo','courseNo','studentId'),)


class Offers(models.Model):
    acadYear = models.ForeignKey(Semester, related_name='acadYear+', null=True)
    semesterNo = models.ForeignKey(Semester, related_name='semesterNo+', null=True)
    courseNo = models.ForeignKey(Courses, related_name='courseNo+', null=True)

    class Meta:
        unique_together = (('acadYear','semesterNo','courseNo'),)


class FeeReceipt(models.Model):
    studentId = models.ForeignKey(Student,related_name='%(class)s_studentId',null=False,default="0")
    acadYear = models.ForeignKey(Semester, related_name='acadYear+', null=True)
    semesterNo = models.ForeignKey(Semester, related_name='semesterNo+', null=True)
    receiptId = models.CharField(max_length=30,null=False,blank=True,default="0")
    status = models.CharField(max_length=50,null=False,blank=True,default='Not Paid')

    class Meta:
        unique_together = (('acadYear','semesterNo','studentId'),)


class Result(models.Model):
    studentId = models.ForeignKey(Student, related_name='studentId+')
    acadYear = models.ForeignKey(Semester, null=True, related_name='acadYear+')
    semesterNo = models.ForeignKey(Semester, null=True, related_name='semesterNo+')
    SPI = models.FloatField(default='',blank=True,null=True)

