from django import forms
from django.contrib.auth.models import User
import django.contrib.auth.password_validation as validators
from django.core import exceptions
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
        course_name = self.cleaned_data['course_name']
        if course_name.__len__() != 0:
            if course.objects.filter(course_name=course_name):
                raise forms.ValidationError("Course Name already exists")
        else:
            raise forms.ValidationError("Please Enter a valid CourseName")
        return course_name

    def clean_faculty(self):
        facultyList = User.objects.filter(groups__name='faculty')
        facultyName = self.cleaned_data['faculty']
        courses_of_current_faculty = course.objects.filter(faculty=facultyName)
        course_name = self.cleaned_data['course_name']
        if course_name in courses_of_current_faculty:
            raise forms.ValidationError(facultyName.facultyName +" is already assigned this course ")

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
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password',]

    def clean_username(self):
        username = self.cleaned_data['username']
        if username != 0:
            if User.objects.filter(username = username) and  username != 0:
                raise forms.ValidationError("Username already exists")
        else:
            raise forms.ValidationError("Enter Valid username")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email != None:
            if User.objects.filter(email = email):
                raise forms.ValidationError("Email already exists.")
        else:
            raise forms.ValidationError("Enter Valid FacultyName")
        return email

    def first_name(self):
        first_name = self.cleaned_data['first_name']
        if first_name == None:
            raise forms.ValidationError("Please enter First name.")
        return first_name

    def last_name(self):
        last_name = self.cleaned_data['last_name']
        if last_name == None:
            raise forms.ValidationError("Please enter last name.")
        return last_name

    def validate(self):
        password = self.cleaned_data['password']
        errors = dict()
        try:
            validators.validate_password(password=password, user=User)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        return password

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