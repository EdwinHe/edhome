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
            messages.warning(request, upload_file_form.errors)
            
    else:
        upload_file_form = UploadFileForm()
    
    outstanding_tran_num = Transaction.objects.filter(keyword__isnull = True).count()
    span_tran_num = Transaction.objects.filter(span_status__exact = 'N').count()
    
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
    SourceFile.objects.create(file_name = file_name,local_link =None)
    return HttpResponse("Manual CSV " + file_name + " created.")

def ozio_add_manual_transaction(request):
    
    
    if request.method == 'POST':
        amount = request.POST['amount']
        date = request.POST['date']
        info = request.POST['info']
        original_info = request.POST['original_info']
        source_file_name = request.POST['source_file_name']
        
        try:
            source_file, created = SourceFile.objects.get_or_create(file_name = source_file_name)
        except SourceFile.DoesNotExist:
            source_file, created = SourceFile.objects.create(file_name = source_file_name)
            if not created:
                return HttpResponse('Tried to create file ' + source_file_name + ' but failed.')
        
        tran_form = TransactionForm({'amount':amount, 
                               'date': date,
                               'info': info,
                               'original_info': original_info,
                               'source_file': source_file.id})  
        
        #import pdb;pdb.set_trace()
        
        if tran_form.is_valid():
            # Save Transaction
            tran_id = tran_form.save().id
            
            # Save record to file
            saved = append_transaction_to_file(source_file, date, amount, info)
            
            if saved:
                return HttpResponse('Transaction id=' + str(tran_id) + ' saved!', status=200)
            else:
                return HttpResponse('Save transaction id=' + str(tran_id) + ' to file failed!', status=500)
        else:
            return HttpResponse(simplejson.dumps(tran_form.errors), status=500, content_type="application/json")
    else:
        return HttpResponse('Non POST request is not expected!', status=500)

def ozio_map_transaction(request):
    map_transactions()
    update_span_status()
    return ozio_transaction(request)

def ozio_split_transaction(request):
    split_transactions()
    return ozio_transaction(request)

def ozio_on_object_delete(request, obj_name, obj_id):
    #import pdb;pdb.set_trace()
    if (obj_name == 'sourcefile'):
        try:
            sf = SourceFile.objects.get(id = obj_id)
            local_name = sf.local_link.name
            sf.local_link.delete()
            if sf.local_link:
                return HttpResponse('Failed to Delete Local Link of SourceFile id='+str(obj_id), status=500)
            else:
                return HttpResponse('Deleted Local Link: ' + local_name +' of SourceFile id='+str(obj_id), status=200)
        except SourceFile.DoesNotExist:
            return HttpResponse('SourceFile id=' + str(obj_id) + ' not found!', status=500)
    else:
        return HttpResponse(status=200)

def ozio_transaction(request):
    # Exclude some columns from config
    tran_exclude_cols = {'#id_thead_outstanding_tran':['id', 'span_status', 'keyword', 'type', 'span_months', 'cate', 'subcate'],
                         '#id_thead_span_tran':['id', 'original_info', 'span_status'],
                         '#id_thead_tran':['id', 'span_status', 'span_months'],
                         };
    json_tran_exclude_cols = simplejson.dumps(tran_exclude_cols)
    
    outstanding_tran_num = Transaction.objects.filter(keyword__isnull = True).count()
    span_tran_num = Transaction.objects.filter(span_status__exact = 'N').count()
    tran_num = Transaction.objects.all().count()
    
    context = { 'outstanding_tran_num': outstanding_tran_num,
                'span_tran_num': span_tran_num,
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