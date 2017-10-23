from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('index.html')
    if request.user.is_authenticated():
        print(request.user.email)
    context = {}
    return HttpResponse(template.render(context, request))


