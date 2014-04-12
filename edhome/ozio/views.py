from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages

from ozio.models import *
from ozio.forms import UploadFileForm
from ozio.ozioUtils import handle_uploaded_file

# Create your views here.
def ozio_home(request):
    
    transactions = Transaction.objects.all().order_by('date')
    keywords = Keyword.objects.all()
    types = Type.objects.all()
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        
        if form.is_valid():
            if SourceFile.objects.filter(file_name__exact = request.FILES['chosen_file'].name).count() == 0:
                #import pdb;pdb.set_trace()
                a_source_file = SourceFile.objects.create(file_name = request.FILES['chosen_file'].name,
                                       local_link = request.FILES['chosen_file'])
                msg = handle_uploaded_file(a_source_file.pk, request.FILES['chosen_file'])
                
                messages.success(request, msg)
                return HttpResponseRedirect(reverse('ozio:home'))
            else:
                messages.warning(request, "Aborted! You have already imported this file.")
        else:
            messages.warning(request, "Please choose a file, and try again!")
    else:
        form = UploadFileForm()
    
    context = {'form': form, 'transactions':transactions, 'keywords':keywords, 'types':types}
    return render(request, 'ozio/ozio_home.html', context)

def ozio_test(request):
    return render(request, 'ozio/ozio_test.html')