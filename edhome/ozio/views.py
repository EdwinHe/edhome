from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils import simplejson
from django.template.loader import render_to_string

from ozio.models import *
from ozio.forms import *
from ozio.ozioUtils import *

# Create your views here.
def ozio_home(request):
    
    if request.method == 'POST':
        #import pdb;pdb.set_trace()
        upload_file_form = UploadFileForm(request.POST, request.FILES)
            
        if upload_file_form.is_valid():
            for file in upload_file_form.files.getlist('chosen_file'):
                if SourceFile.objects.filter(file_name__exact = file.name).count() == 0:
                    a_source_file = SourceFile.objects.create(file_name = file.name,
                                           local_link = file)
                    msg = handle_uploaded_file(a_source_file.pk, file)
                    
                    messages.success(request, msg)
                else:
                    messages.warning(request, file.name + ": Aborted! It has already been imported.")
            return HttpResponseRedirect(reverse('ozio:home'))
        else:
            #messages.warning(request, "Please choose a file, and try again!")
            messages.warning(request, upload_file_form.errors)
            
    else:
        upload_file_form = UploadFileForm()
    
    outstanding_tran_num = Transaction.objects.filter( keyword__isnull = True ).count()
    
    # For Pie Chart
    pie_chart_data = get_pie_chart_data()
    json_pie_chart_data = simplejson.dumps(pie_chart_data)
    
    # For Bar Chart
    [bar_chart_monthlyView,bar_chart_monthlyDrilldown,bar_chart_monthlySubCateDrilldown] = get_bar_chart_data()
    json_bar_chart_monthlyView = simplejson.dumps(bar_chart_monthlyView)
    json_bar_chart_monthlyDrilldown = simplejson.dumps(bar_chart_monthlyDrilldown)
    json_bar_chart_monthlySubCateDrilldown = simplejson.dumps(bar_chart_monthlySubCateDrilldown)
    
    context = {'upload_file_form': upload_file_form,
               'outstanding_tran_num': outstanding_tran_num,
               'json_pie_chart_data': json_pie_chart_data,
               'json_bar_chart_monthlyView': json_bar_chart_monthlyView,
               'json_bar_chart_monthlyDrilldown': json_bar_chart_monthlyDrilldown,
               'json_bar_chart_monthlySubCateDrilldown': json_bar_chart_monthlySubCateDrilldown,}
    return render(request, 'ozio/ozio_home.html', context)

def ozio_test(request):
    return render(request, 'ozio/ozio_test.html')

def ozio_add_manual_csv(request, file_name):
    SourceFile.objects.create(file_name = file_name,local_link ='TBC')
    return HttpResponse("Manual CSV " + file_name + " created.")

def ozio_map_transaction(request):
    map_transactions()
    return ozio_transaction(request)

def ozio_transaction(request):
    transactions = Transaction.objects.all().order_by('date')
    outstanding_transactions = Transaction.objects.filter(keyword__isnull = True).order_by('date')
    
    outstanding_tran_num = Transaction.objects.filter( keyword__isnull = True ).count()
    tran_num = Transaction.objects.all().count()

    context = { 'transactions': transactions, 
                'outstanding_transactions': outstanding_transactions,
                'outstanding_tran_num': outstanding_tran_num, 
                'tran_num': tran_num,
                }
    return render(request, 'ozio/ozio_transaction.html', context)


def ozio_config(request):
    return render(request, 'ozio/ozio_config.html')