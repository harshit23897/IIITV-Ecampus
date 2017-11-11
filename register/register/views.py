from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

def home(request):
    if not request.user.is_anonymous():
        if is_faculty(request.user):
            return HttpResponseRedirect('/faculty/')
        else:
            return HttpResponseRedirect('/student/')
    template = loader.get_template('site_base.html')
    # print(request.user.email)
    context = {}
    return HttpResponse(template.render(context, request))

def index(request):
    template = loader.get_template('index.html')
    # print(request.user.email)
    context = {}
    return HttpResponse(template.render(context, request))

def is_faculty(user):
    return user.groups.filter(name='faculty').exists()
