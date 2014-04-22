from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils import simplejson
from django.template.loader import render_to_string

from ozio.models import *
from ozio.forms import *
from ozio.ozioUtils import *

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
    elif obj_type == 'transaction_filter':
        obj_class_name = 'TransactionFilter'
    elif obj_type == 'filter_sql':
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
