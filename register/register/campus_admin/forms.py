from django import forms
from django.contrib.auth.models import User
from register.course.models import course
from .models import Registers,FeeReceipt




class CoursesForm(forms.ModelForm):


    class Meta:
        model = course
        fields = ['courseNo','course_name','credits','offered_in','elective','offered_to','faculty']

    def clean_courseNo(self):
        courseNo = self.cleaned_data['courseNo']
        length = len(courseNo)
        if length == 5:
            string_part = courseNo[0:2]
            integer_part = courseNo[2:5]
            if string_part == 'CS' or  string_part == 'IT' or  string_part =='HM'  or  string_part =='SC':
                for i in range(0,len(integer_part)):
                    if ord(integer_part[i])<48 or ord(integer_part[i])>57:
                        raise forms.ValidationError("Invalid CourseNo")
            else:
                raise forms.ValidationError("Invalid CourseNo")

            if course.objects.filter(courseNo = courseNo):
                raise forms.ValidationError("CourseNo already exists")

        elif length == 0:
            raise forms.ValidationError("Please Enter a valid courseNo")

        else:
            raise forms.ValidationError("Invalid CourseNo")
        return courseNo



    def clean_courseName(self):
        courseName = self.cleaned_data['courseName']
        if courseName.__len__() != 0:
            if Courses.objects.filter(courseName=courseName):
                raise forms.ValidationError("CourseName already exists")
        else:
            raise forms.ValidationError("Please Enter a valid CourseName")
        return courseName

    def clean_assigned_to(self):
        facultyList = User.objects.filter(groups__name='faculty')
        facultyName = self.cleaned_data['assigned_to']
        if Courses.objects.filter(assigned_to=facultyName):
            raise forms.ValidationError(facultyName.facultyName +" is already assigned one course ")

        return facultyName


class RegistersForm(forms.ModelForm):
    class Meta:
        model = Registers
        fields = ['grade']

    def clean_grade(self):
        grade = self.cleaned_data['grade']
        length = len(grade)
        if length == 2:
            for i in range(0,length):
                if ord(grade[i])<65  or  ord(grade[i])>68:
                    raise forms.ValidationError("Invalid Data")
        else :
            raise forms.ValidationError("Invalid Data")


class FeeReceiptForm(forms.ModelForm):
    class Meta:
        model = FeeReceipt
        fields = ['receiptId','status']

    def clean_receiptId(self):
        receiptId = self.cleaned_data['receiptId']
        if receiptId.__len__() != 0:
            if FeeReceipt.objects.filter(receiptId = receiptId):
                raise forms.ValidationError("ReceiptId already exists")
        else:
            raise forms.ValidationError("Please Enter a valid ReceiptId")
        return receiptId


class FacultyForm(forms.ModelForm):

    class Meta:
        model = Faculty
        fields = ['facultyId','facultyName']

    def clean_facultyId(self):
        facultyId = self.cleaned_data['facultyId']
        if facultyId != 0:
            if Faculty.objects.filter(facultyId = facultyId) and  facultyId != 0:
                raise forms.ValidationError("FacultyId already exists")
        else:
            raise forms.ValidationError("Enter Valid FacultyId")
        return facultyId

    def clean_facultyName(self):
        facultyName = self.cleaned_data['facultyName']
        if facultyName != None:
            if Faculty.objects.filter(facultyName = facultyName):
                raise forms.ValidationError("FacultyName already exists")
        else:
            raise forms.ValidationError("Enter Valid FacultyName")
        return facultyName

''' 
class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['SPI']

    def _clean_SPI(self):
        SPI = self.cleaned_data['SPI']
        if SPI <= 10 :
           length = len(SPI)
           if length <= 4 :
               for i in range(0, length):
                   if ord(SPI[i]) < 48 or ord(SPI[i]) > 57:
                       raise forms.ValidationError("Invalid Data")
        else:
            raise forms.ValidationError("Invalid Data")
'''