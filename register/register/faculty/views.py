from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from register.course.models import course
from register.student.models import AssignmentSubmission

@login_required
@user_passes_test(lambda u: u.groups.all()[0].name == 'faculty', login_url='/accounts/login/')
def facultyHomePage(request):
    print(request.user.groups.all()[0].name)
    template_name = 'faculty_home_page.html'
    context = {}
    return render(request, template_name, context)

@login_required
@user_passes_test(lambda u: u.groups.all()[0].name == 'faculty', login_url='/accounts/login/')
def student_assignment_submission_view(request, **kwargs):
    current_course = course.objects.get(courseNo__exact=kwargs['course_no'])
    assignment_submission = AssignmentSubmission.objects.filter(assignment__id__exact=kwargs['assignment_id'])
    return render(request,
                  'student_assignment_submission_view.html',
                  {'course_no': kwargs['course_no'],
                   'assignment_list': assignment_submission})
