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

#===============================================================================
# def ozio_add_new_transaction(request):
#     transaction_form = TransactionForm(prefix='transaction')
#     
#     #rendered_form_template = render_to_string('ozio/ozio_form_transaction.html', {'transaction_form': transaction_form})
#     #context = {'rendered_form_template': rendered_form_template}
#     
#     context = {'transaction_form': transaction_form}
#     
#     return render(request, 'ozio/ozio_add_new_transaction.html', context)
#===============================================================================


def ozio_config(request):
    
    type_form = TypeForm(prefix='type', instance = Type.objects.get(pk=1))
    cate_form = CateForm(prefix='cate')
    subcate_form = SubCateForm(prefix='subcate')
    keyword_form = KeywordForm(prefix='keyword')
    sourcefile_form = SourceFileForm(prefix='sourcefile')
    transaction_form = TransactionForm(prefix='transaction')
    transactionfilter_form = TransactionFilterForm(prefix='transactionfilter')
    filtersql_form = FilterSQLForm(prefix='filtersql')
    open_dialog_name = ''
    active_tab = 'type'
    
    #import pdb;pdb.set_trace()
    if request.method == 'POST':
        if 'submit_type' in request.POST:
            type_form = TypeForm(request.POST, prefix='type')
            if type_form.is_valid():
                type_form.save()
                active_tab = 'type'
            else:
                open_dialog_name = 'type'
        elif 'submit_cate' in request.POST:
            cate_form = CateForm(request.POST, prefix='cate')
            if cate_form.is_valid():
                cate_form.save()
                active_tab = 'cate'
            else:
                open_dialog_name = 'cate'
        elif 'submit_subcate' in request.POST:
            subcate_form = SubCateForm(request.POST, prefix='subcate')
            if subcate_form.is_valid():
                subcate_form.save()
                active_tab = 'subcate'
            else:
                open_dialog_name = 'subcate'
        elif 'submit_keyword' in request.POST:
            keyword_form = KeywordForm(request.POST, prefix='keyword')
            if keyword_form.is_valid():
                keyword_form.save()
                active_tab = 'keyword'
            else:
                open_dialog_name = 'keyword'
        elif 'submit_sourcefile' in request.POST:
            sourcefile_form = SourceFileForm(request.POST, prefix='sourcefile')
            if sourcefile_form.is_valid():
                sourcefile_form.save()
                active_tab = 'sourcefile'
            else:
                open_dialog_name = 'sourcefile'
        elif 'submit_transaction' in request.POST:
            transaction_form = TransactionForm(request.POST, prefix='transaction')
            if transaction_form.is_valid():
                transaction_form.save()
                active_tab = 'transaction'
            else:
                open_dialog_name = 'transaction'
        elif 'submit_transactionfilter' in request.POST:
            transactionfilter_form = TransactionFilterForm(request.POST, prefix='transactionfilter')
            if transactionfilter_form.is_valid():
                transactionfilter_form.save()
                active_tab = 'transactionfilter'
            else:
                open_dialog_name = 'transactionfilter'
        elif 'submit_filtersql' in request.POST:
            filtersql_form = FilterSQLForm(request.POST, prefix='filtersql')
            if filtersql_form.is_valid():
                filtersql_form.save()
                active_tab = 'filtersql'
            else:
                open_dialog_name = 'filtersql'
        
    context = { 
        'type_form': type_form,
        'cate_form': cate_form,
        'subcate_form': subcate_form,
        'keyword_form': keyword_form,
        'sourcefile_form': sourcefile_form,
        'transaction_form': transaction_form,
        'transactionfilter_form': transactionfilter_form,
        'filtersql_form': filtersql_form,
        'open_dialog_name': open_dialog_name,
        'active_tab': active_tab,
        }
    
    return render(request, 'ozio/ozio_config.html', context)