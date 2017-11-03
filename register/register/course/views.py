import os
import mimetypes
from django.conf import settings
from django.utils.encoding import smart_str
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from wsgiref.util import FileWrapper

from .forms import CourseMaterialForm
from .models import CourseMaterial

def course_material_upload(request):
    if request.method == 'POST':
        form = CourseMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            unsaved_form = form.save(commit=False)
        unsaved_form.faculty = request.user
        unsaved_form.save()
        return redirect('course_material_upload')
    else:
        form = CourseMaterialForm()

    return render(request, 'course_material_upload.html', {
        'form': form
    })

def files_list(request):
    material = CourseMaterial.objects.filter(faculty__username__contains=request.user)
    return render(request, 'course_material_view.html',
                              {'course_material': material,
                               'path':settings.MEDIA_ROOT},
                              )

def download(request, file_name):
    print('Hello')
    file_path = settings.MEDIA_ROOT +'/'+ file_name
    file_wrapper = FileWrapper(open(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    return response
