import datetime
from django.shortcuts import render,get_object_or_404,redirect
from .models import Registers,FeeReceipt,Result
from register.student.models import student
from .forms import RegistersForm,FeeReceiptForm,CoursesForm,FacultyForm
from django.http import HttpResponse
import math
from django.db.models import Max,Min


def index(request):
    template = 'campus_admin/homepage.html'
    return render(request, template)


def registration(request):
    return  HttpResponse('<p> Nothing to Show </p>')


def result(request):

    # student = Student.objects.get(studentId='201552078')
    # year = student.batch
    # program = student.programName
    # present_acadYear = student.acadYear.acadYear
    # present_semester = student.semesterNo.semesterNo
    # args = {'present_acadYear':present_acadYear,'present_semester':present_semester}

    all_batches = student.objects.order_by('batch').values('batch').distinct()
    # batches = tuple(all_batches)
    # length = len(batches)
    # number = len(batches)
    # for i in all_batches:
    #     print(i)
    args = {'batches': all_batches}
    return render(request, 'campus_admin/result_base.html', args)


def fee_receipt(request):

    # student = Student.objects.get(studentId='201552078')
    # year = student.batch
    # program = student.programName
    # present_acadYear = student.acadYear.acadYear
    # present_semester = student.semesterNo.semesterNo
    # args = {'present_acadYear':present_acadYear,'present_semester':present_semester}

     # dictlist = []

    all_batches = student.objects.order_by('batch').values('batch').distinct()
    print(all_batches)
    # for key,value in all_batches.items():
     #   temp = [key,value]
      #  dictlist.append(temp)

    # length = len(batches)
    # number = len(batches)
    # for i in all_batches:
    #     print(i)
    args = {'batches':all_batches}
    return render(request, 'campus_admin/fee_receipt_base.html', args)


def result_base(request,pk,pk4):
    student1 = student.objects.filter(batch=pk, program=pk4)
    args = {'student':student1,'pk4':pk4}
    return render(request, 'campus_admin/student_View_result.html', args)


def fee_receipt_base(request,pk,pk4):
    # print(student.objects.filter(batch=pk, program=pk4))
    student1 = student.objects.filter(batch=pk, program=pk4)
    print(student1)
    args = {'student':student1,'pk4':pk4}
    return render(request, 'campus_admin/student_View_fee.html', args)


def sem_view_result(request,pk,pk1,pk4):
    temp = Registers.objects.filter(studentId=pk)
    semNo = temp.order_by('semesterNo').values('semesterNo').distinct()
    max = semNo.aggregate(Max('semesterNo'))
    value = max['semesterNo__max']
    value = value
    #  max = int(max) - 1
    # print(value)
    return render(request, 'campus_admin/semester_View_result.html', {'pk': pk, 'pk1': pk1, 'pk4': pk4, 'value': value})


def sem_view_fee(request,pk,pk1,pk4):
    print(pk)
    print(pk1)
    print(pk4)
    current_student = student.objects.get(student_id=pk)
    # print(current_student)
    current_semester = datetime.datetime.now().year - int(current_student.batch)
    current_semester = current_semester * 2 + 1
    # print(current_semester)
    #  max = int(max) - 1
    #  print(value)
    return render(request, 'campus_admin/semester_View_fee.html',
                  {'pk': pk, 'pk1': pk1, 'pk4': pk4, 'pk2': current_semester})


def course_list(request,pk,pk1,pk2,pk4):

    student = Registers.objects.filter(studentId=pk,semesterNo=pk2)
    args = {'student':student,'pk1':pk1,'pk2':pk2,'pk4':pk4}
    return render(request,'campus_admin/course_list.html',args)

'''
def result_add(request,pk,pk1,pk2,pk3,pk4):

    if request.method == 'POST':
        form = ResultForm(request.POST)

        if form.is_valid():

            grade = request.POST.get('grade')
            # print(grade)
            Registers.objects.filter(studentId=pk, courseNo=pk3).update(grade=grade)
           # print(form.instance.grade)
           # form.instance.grade = Registers.objects.filter(studentId=pk, courseNo=pk1)

        # return redirect('campus_admin:success')

    else:
        form = ResultForm()

    return render(request,'campus_admin/result_add.html',{'form':form})
'''


def add_faculty(request):

    if request.method == "POST":
        form = FacultyForm(request.POST)

        if form.is_valid():
            temp = form.save()
            return redirect('campus_admin:success')
    else:
        form = FacultyForm

    return render(request,'campus_admin/faculty_add.html',{'form':form})


def success(request):
    return render(request,'campus_admin/success.html')


def add_course(request):

    if request.method == "POST":
        form = CoursesForm(request.POST or None)
        # print(form.assigned_to)
        if form.is_valid():
            temp=form.save()
            return redirect('campus_admin:success')
    else:
        form = CoursesForm
    return render(request,'campus_admin/courses_add.html',{'form':form})


def result_add(request,pk,pk1,pk2,pk3,pk4):

    student = get_object_or_404(Registers,studentId=pk,courseNo=pk3,semesterNo=pk2)
    form = RegistersForm(request.POST or None,instance=student)

    if form.is_valid():
        temp = form.save(commit=False)
        grade = request.POST.get('grade')
        Registers.objects.filter(studentId=pk, courseNo=pk3).update(grade=grade)
        # temp.save()
        return redirect('campus_admin:success_result',pk=pk,pk4=pk4,pk1=pk1,pk2=pk2,pk3=pk3)

    return render(request, 'campus_admin/result_add.html', {'form': form})


def success_result(request, pk4, pk1, pk, pk2, pk3):

    args = {'pk4':pk4 ,'pk1':pk1}
    return render(request, 'campus_admin/successful_result_update.html', args)


def success_fee_receipt(request, pk4, pk1, pk, pk2, pk3):

    args = {'pk4': pk4,'pk1':pk1}
    return render(request, 'campus_admin/successful_fee_receipt_update.html', args)


def fee_receipt_add(request,pk,pk1,pk2,pk4):

    current_student = student.objects.get(student_id=pk)
    form = FeeReceiptForm(request.POST or None, instance=student)

    if form.is_valid():
        temp = form.save(commit=False)
        data = request.POST.get('receiptId')
        data1 = request.POST.get('status')

        FeeReceipt.objects.filter(studentId=pk,semesterNo=pk2).update(receiptId=data)
        FeeReceipt.objects.filter(studentId=pk,semesterNo=pk2).update(status=data1)
        return redirect('campus_admin:success_fee_receipt', pk=pk, pk4=pk4, pk1=pk1, pk2=pk2)

    #print(form.errors)
    return render(request,'campus_admin/fee_receipt_add.html',{'form':form})

'''
def add_grade(request,pk,pk1,pk2,pk4):
    student = get_object_or_404(Result,studentId=pk ,semesterNo=pk2,acadYear__acadYear=pk1)
    form = ResultForm(request.POST or None, instance=student)

    if form.is_valid():
        temp = form.save(commit=False)
        data = request.POST.get('SPI')

        Result.objects.filter(studentId=pk,acadYear__acadYear=pk1,semesterNo=pk2).update(SPI=data)

    return render(request,'campus_admin/add_grade.html',{'form':form})
'''


def final_result_view(request,pk,pk1,pk4):
    temp = Registers.objects.filter(studentId=pk)
    semNo = temp.order_by('semesterNo').values('semesterNo').distinct()
    max = semNo.aggregate(Max('semesterNo'))
    value = max['semesterNo__max']
    value = value - 1
   #  max = int(max) - 1
   #  print(value)
    return render(request,'campus_admin/final_result_view.html',{'pk':pk,'pk1':pk1,'pk4':pk4,'value':value})


def final_fee_receipt_view(request,pk,pk1,pk4):
    temp = FeeReceipt.objects.filter(studentId=pk)
    semNo = temp.order_by('semesterNo').values('semesterNo').distinct()
    max = semNo.aggregate(Max('semesterNo'))
    value = max['semesterNo__max']
    #  max = int(max) - 1
    #  print(value)
    return render(request, 'campus_admin/final_fee_receipt_view.html', {'pk': pk, 'pk1': pk1, 'pk4': pk4, 'value': value})


def result_view(request,pk,pk1,pk2,pk4):

    temporary = Result.objects.get(studentId=pk, semesterNo=pk2)
    course = Registers.objects.filter(studentId=pk, semesterNo=pk2)
    total = 0
    CPI = 0.0

    if temporary.SPI == None:

        for c in course:
            total = total + c.courseNo.credits
        SPI = (math.ceil(calculate_points(pk,pk2,total)*100)/100)
        # print(SPI)
        temporary = Result.objects.get(studentId=pk,semesterNo=pk2)
        temporary.SPI = SPI
        temporary.save()
        # print(SPI,pk2)

    else:
        SPI = temporary.SPI
    # print(temp)

    temp = int(pk2) - 1

    if pk2 == '1':
        CPI = SPI
    else:
        while temp > 0 :
            temporary = Result.objects.get(studentId=pk, semesterNo=temp)
            CPI = SPI+temporary.SPI
          #  print(CPI)
            temp = temp - 1

        CPI = CPI/int(pk2)
        CPI = (math.ceil(CPI * 100) / 100)
    iterate = int(pk2)-1
    # print(CPI,SPI)
    return render(request, 'campus_admin/result_view.html', {'course':course, 'pk1':pk1, 'pk2':pk2,'pk4':pk4,'pk':pk,'iterate':iterate,'total':total,'SPI':SPI,'CPI':CPI})


def calculate_points(pk,pk2,total):

    course = Registers.objects.filter(studentId=pk, semesterNo=pk2)
    credits_scored = 0
    for c in course:
        if c.grade == "AA":
            credits_scored = credits_scored + 10 * c.courseNo.credits
        if c.grade == "AB":
            credits_scored = credits_scored + 9 * c.courseNo.credits
        if c.grade == "BB":
            credits_scored = credits_scored + 8 * c.courseNo.credits
        if c.grade == "BC":
            credits_scored = credits_scored + 7 * c.courseNo.credits
        if c.grade == "CC":
            credits_scored = credits_scored + 6 * c.courseNo.credits
        if c.grade == "CD":
            credits_scored = credits_scored + 5 * c.courseNo.credits
        if c.grade == "DD":
            credits_scored = credits_scored + 4 * c.courseNo.credits
        if c.grade == "FF":
            credits_scored = credits_scored + 0 * c.courseNo.credits
    print(credits_scored,total)
    SPI = credits_scored / total
    return SPI


def fee_receipt_view(request,pk,pk1,pk2,pk4):

    fee = FeeReceipt.objects.get(studentId=pk,semesterNo=pk2)
    iterate = int(pk2) - 1
    return render(request, 'campus_admin/fee_receipt_view.html', {'fee': fee, 'pk1':pk1, 'pk2':pk2,'pk':pk,'pk4':pk4,'iterate':iterate})



