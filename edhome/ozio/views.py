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
    
    outstanding_tran_num = get_filtered_transactions('Outstanding Transactions').count()
    span_tran_num = get_filtered_transactions('Span Transactions').count()
    
    # For Bar Chart
    [bar_chart_monthlyView,bar_chart_monthlyDrilldown,bar_chart_monthlySubCateDrilldown] = get_bar_chart_data()
    json_bar_chart_monthlyView = simplejson.dumps(bar_chart_monthlyView)
    json_bar_chart_monthlyDrilldown = simplejson.dumps(bar_chart_monthlyDrilldown)
    json_bar_chart_monthlySubCateDrilldown = simplejson.dumps(bar_chart_monthlySubCateDrilldown)
    
    # For Mix Chart
    mix_chart_data = get_mix_chart_data()
    json_mix_chart_data = simplejson.dumps(mix_chart_data)
    
    context = {'upload_file_form': upload_file_form,
               'outstanding_tran_num': outstanding_tran_num,
               'span_tran_num': span_tran_num,
               # Bar Chart
               'json_bar_chart_monthlyView': json_bar_chart_monthlyView,
               'json_bar_chart_monthlyDrilldown': json_bar_chart_monthlyDrilldown,
               'json_bar_chart_monthlySubCateDrilldown': json_bar_chart_monthlySubCateDrilldown,
               # Mix Chart
               'json_mix_chart_data': json_mix_chart_data,
               }
    return render(request, 'ozio/ozio_home.html', context)

def ozio_test(request):
    return render(request, 'ozio/ozio_test.html')

def ozio_add_manual_csv(request, file_name):
    SourceFile.objects.create(file_name = file_name,local_link ='TBC')
    return HttpResponse("Manual CSV " + file_name + " created.")

def ozio_map_transaction(request):
    map_transactions()
    update_span_status()
    return ozio_transaction(request)

def ozio_split_transaction(request):
    split_transactions()
    return ozio_transaction(request)

def ozio_transaction(request):
    # Exclude some columns from config
    tran_exclude_cols = {'#id_thead_outstanding_tran':['id', 'span_status', 'keyword', 'type', 'span_months', 'cate', 'subcate'],
                         '#id_thead_span_tran':['id', 'original_info', 'span_status'],
                         '#id_thead_tran':['id', 'span_status', 'span_months'],
                         };
    json_tran_exclude_cols = simplejson.dumps(tran_exclude_cols)
    
    outstanding_transactions = get_filtered_transactions('Outstanding Transactions').order_by('date')
    span_transactions = get_filtered_transactions('Span Transactions')
    transactions = Transaction.objects.all().order_by('date')
    
    outstanding_tran_num = outstanding_transactions.count()
    span_tran_num = span_transactions.count()
    tran_num = transactions.count()
    
    context = { 'outstanding_transactions': outstanding_transactions,
                'outstanding_tran_num': outstanding_tran_num,
                'span_transactions': span_transactions,
                'span_tran_num': span_tran_num,
                'transactions': transactions,
                'tran_num': tran_num,
                'json_tran_exclude_cols' : json_tran_exclude_cols,
                }
    return render(request, 'ozio/ozio_transaction.html', context)


def ozio_config(request):
    
    # Exclude some columns from config
    config_exclude_cols = {'type':['id'],
                           'cate':['id'],
                           'subcate':['id'],
                           'keyword': ['id'],
                           'sourcefile':['id'],
                           'transaction':['id', 'span_status'],
                           'transactionfilter':['id'],
                           'filtersql':['id'],
                           };
    json_config_exclude_cols = simplejson.dumps(config_exclude_cols)
    
    context = {'json_config_exclude_cols' : json_config_exclude_cols,
               }
    
    return render(request, 'ozio/ozio_config.html', context)

def ozio_add_or_edit(request, obj_type, obj_id):
        
    if obj_type == 'type':
        obj_class_name = 'Type'
    elif obj_type == 'cate':
        obj_class_name = 'Cate'
    elif obj_type == 'subcate':
        obj_class_name = 'SubCate'
    elif obj_type == 'keyword':
        obj_class_name = 'Keyword'
    elif obj_type == 'sourcefile':
        obj_class_name = 'SourceFile'
    elif obj_type == 'transaction':
        obj_class_name = 'Transaction'
    elif obj_type == 'transactionfilter':
        obj_class_name = 'TransactionFilter'
    elif obj_type == 'filtersql':
        obj_class_name = 'FilterSQL'
        
    #import pdb;pdb.set_trace()
    try: ### Modify 
        instance = eval(obj_class_name + '.objects.get(id=' + obj_id + ')')
        form = eval(obj_class_name + 'Form(request.POST or None, instance = instance)')
    except: ### Add
        form = eval(obj_class_name + 'Form(request.POST or None)')
        
    if form.is_valid():
        form.save()
        return HttpResponse('')
        
    context = {'form': form,
               'obj_type': obj_type,
               'obj_id': obj_id,}
    return render(request, 'ozio/ozio_form_add_or_edit.html', context)