from django.shortcuts import render, redirect
from .forms import SubjectFileForm
from .models import SubjectFile
from django.template import TemplateDoesNotExist


def upload_file(request):
    try:
        if request.method == 'POST':
            form = SubjectFileForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('upload_file')
        else:
            form = SubjectFileForm()
        
        files = SubjectFile.objects.all().order_by('subject')
        return render(request, 'uploads/upload.html', {'form': form, 'files': files})
    except TemplateDoesNotExist as e:
        print(f"Template does not exist: {e}")
        return render(request, 'uploads/upload.html', {'form': form, 'files': files})