from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

@login_required
@user_passes_test(lambda u: u.groups.all()[0].name == 'faculty', login_url='/accounts/login/')
def facultyHomePage(request):
    print(request.user.groups.all()[0].name)
    template_name = 'faculty_home_page.html'
    context = {}
    return render(request, template_name, context)
