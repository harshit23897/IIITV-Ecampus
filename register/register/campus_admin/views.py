from django.shortcuts import render
from django.http import HttpResponse
from .models import Student,Registers,FeeReceipt
from django.shortcuts import redirect
from .forms import ResultForm,FeeReceiptForm

def index(request):
    template = 'homepage.html'
    return render(request, template)


def result(request):

    # student = Student.objects.get(studentId='201552078')
    # year = student.batch
    # program = student.programName
    # present_acadYear = student.acadYear.acadYear
    # present_semester = student.semesterNo.semesterNo
    # args = {'present_acadYear':present_acadYear,'present_semester':present_semester}

    all_batches = Student.objects.order_by('batch').values('batch').distinct()
    # batches = tuple(all_batches)
    # length = len(batches)
    # number = len(batches)
    # for i in all_batches:
    #     print(i)
    args = {'batches':all_batches}
    return render(request, 'campus_admin/result_base.html', args)


def result_base(request,pk,pk4):
    student = Student.objects.filter(batch=pk,programName=pk4)
    args = {'student':student,'pk4':pk4}
    return render(request, 'campus_admin/student_View_result.html', args)


def fee_receipt_base(request,pk):
    student = Student.objects.filter(batch=pk,programName='CS')
    args = {'student':student}
    return render(request, 'campus_admin/student_View_result.html', args)


def sem_view_result(request,pk,pk1,pk4):
    return render(request, 'campus_admin/semester_View_result.html', {'pk':pk, 'pk1':pk1,'pk4':pk4})


def sem_view_fee(request,pk,pk1):
    return render(request, 'campus_admin/semester_View_fee.html', {'pk':pk, 'pk1':pk1})


def course_list(request,pk,pk1,pk2,pk4):

    student = Registers.objects.filter(studentId=pk)
    args = {'student':student,'pk1':pk1,'pk2':pk2,'pk4':pk4}
    return render(request,'campus_admin/course_list.html',args)


def result_add(request,pk,pk1,pk2,pk3,pk4):

    if request.method == 'POST':
        form = ResultForm(request.POST)

        if form.is_valid():
            temp = form.save(commit=False)
            grade = form.cleaned_data['grade']
            Registers.objects.get(studentId=pk, courseNo=pk1).update(grade=grade)
           # print(form.instance.grade)
           # form.instance.grade = Registers.objects.filter(studentId=pk, courseNo=pk1)

        # return redirect('campus_admin:result_view',pk,pk1)

    else:
        form = ResultForm()

    return render(request,'campus_admin/result_add.html',{'form':form})


def fee_receipt_add(request,pk,pk1,pk2):

    if request.method == 'POST':
        form = FeeReceiptForm(request.POST)

        if form.is_valid():
            temp = form.save(commit=False)
            data = form.cleaned_data['receiptId']
            data1 = form.cleaned_data['status']

            FeeReceipt.objects.get(studentId=pk,acadYear__acadYear=pk1,semesterNo=pk2).update(receiptId=data)
            FeeReceipt.objects.get(studentId=pk,acadYear__acadYear=pk1,semesterNo=pk2).update(status=data1)

        # return redirect('campus_admin:result_view', pk,pk1)

    else:
        form = FeeReceiptForm()

    return render(request,'campus_admin/fee_receipt_add.html',{'form':form})


def result_view(request,pk,pk1,pk2,pk4):

    course = Registers.objects.filter(studentId=pk)
    return render(request, 'campus_admin/result_view.html', {'course':course, 'pk1':pk1, 'pk2':pk2})


def fee_receipt_view(request,pk,pk1,pk2,pk4):

    fee = FeeReceipt.objects.get(studentId=pk,acadYear__acadYear=pk1,semesterNo=pk2)
    return render(request, 'campus_admin/fee_receipt_view.html', {'fee': fee, 'pk1':pk1, 'pk2':pk2})










'''
    grade1 = Registers.objects.filter(courseNo = student.courseNo.courseNo)[0]
    grade2 = Registers.objects.filter(courseNo=student.courseNo.courseNo)[1]
    grade3 = Registers.objects.filter(courseNo=student.courseNo.courseNo)[2]
    grade4 = Registers.objects.filter(courseNo=student.courseNo.courseNo)[3]
    grade5 = Registers.objects.filter(courseNo=student.courseNo.courseNo)[4]'''