from datetime import date

from django.db.models import Q
from django.db.models import Sum, Min, Max
from django.core.files.base import ContentFile

from ozio.models import *

import logging, re
logger = logging.getLogger(__name__)


def append_transaction_to_file(source_file, date, amount, info):
    tran = ','.join([date,amount,info,'0.00'])
    # If source_file is newly created and local_link is yet to link to a real file
    try:
        if not source_file.local_link:
            source_file.local_link.save(source_file.file_name, ContentFile(tran+'\n'))
        else:
            source_file.local_link.open('a') # Cannot write on the first open
            source_file.local_link.close()
            
            source_file.local_link.open('a')  # Open as append mode
            source_file.local_link.write(tran+'\n')
            source_file.local_link.close()
        return True
    except:
        return False
        

def new_tran(tran, shift):
    assert(shift >= 0)
    
    month = tran.date.month
    year = tran.date.year
    
    month = tran.date.month + shift
    year_adj = (month-1) // 12
    year += year_adj
    month = (month-1) % 12 + 1
    
    Transaction.objects.create(
        date = date(year, month, 1),
        amount = tran.amount / tran.keyword.type.span_months,
        info = tran.info,
        original_info = tran.id,
        source_file = tran.source_file,
        span_status = 'C'
    )
    
    

def split_transactions():
    
    span_tran = Transaction.objects.filter(span_status__exact = 'N')
    
    #import pdb;pdb.set_trace()
    for tran in span_tran:
        span_months = tran.keyword.type.span_months
        
        for i in range(span_months):
            new_tran(tran, i)
        
        tran.keyword = Keyword.objects.get(keyword__exact = 'SPLITTED SPAN TRANSACTIONS')
        tran.span_status = 'Y'
        tran.save()
         
def update_span_status():
    '''
    Span Status = {
        -: Freshly Imported
        N: Await For Spliting
        Y: Splitted Original Record
        C: Splitted Child Record
    }
    '''
    ### Get transactions whose span_months > 1 and span_status = '-'
    span_tran = Transaction.objects.select_related() \
                    .filter(keyword__type__span_months__gt = 1) \
                    .filter(span_status__exact = '-')
    span_tran.update(span_status = 'N')

def map_transactions():
    '''
    Resolve Keyword field in several ways:
    1. By mappings defined in configs.py
    2. By pairing up internal transfer made between Ed and Co
    '''
    # 1
    #import pdb;pdb.set_trace()
    keyword_mappings = Keyword.objects.all()
    
    for keyword_mapping in keyword_mappings:
        logging.debug("Updating records with key words: " + keyword_mapping.keyword)
        rows_match = Transaction.objects.filter( Q(info__icontains = keyword_mapping.keyword) &\
                                    Q(keyword__isnull = True) \
                                     ).update(keyword = keyword_mapping.id)
                                            
      
    # 2
    keyword = Keyword.objects.get(keyword__exact = 'INTERNALS')
    internals = Transaction.objects.filter( Q(keyword__isnull = True) & \
                                             ( Q(info__icontains = "TRANSFER FROM SHUQIN") | \
                                               Q(info__icontains = "TRANSFER FROM WENZHEN") \
                                             ) \
                                           )
    for internal in internals:
        # 0   1     2       3     4          5            6  
        #[id, date, amount, info, orig_info, source_file, keyword] = internal
        logging.info("Pairing internal transfer: " + ',' + str(internal.date) + ',' + str(internal.amount) + ',' + str(internal.info))
           
        lookfor_pattern = 'TRANSFER TO CBA A/C NETBANK ' + re.sub('TRANSFER FROM (.)+ NETBANK ','',internal.info)
        neg_amount = -1 * internal.amount
        paired_internals = Transaction.objects.filter( Q(keyword__isnull = True) & \
                                                       Q(amount__exact = neg_amount) & \
                                                       Q(info__icontains = lookfor_pattern) \
                                                     )
        
        if len(paired_internals) != 1:
            logging.warning("Failed to pair. " + str(len(paired_internals)) + " pairs found! Keyword not updated for record id = " + str(internal.id))
        else:
            #import pdb;pdb.set_trace()
            [paired_internal] = paired_internals
            logging.info("Paired: " + ',' + str(paired_internal.date) + ',' + str(paired_internal.amount) + ',' + str(paired_internal.info))
            internal.keyword = keyword
            internal.save()
            paired_internal.keyword = keyword
            paired_internal.save()
            
    
def handle_uploaded_file(file_id, uploaded_file):
    #import pdb; pdb.set_trace()
    line_counter=0
    transaction_counter = 0
    trans_accept_counter = 0
    trans_reject_counter = 0

    logger.info("Handling uploaded file:" + uploaded_file.name + ' id: ' + str(file_id))
    
    for chunk in uploaded_file.chunks():
        string_chunk = chunk.decode(encoding='UTF-8')
        for line in string_chunk.split('\n'):
            re.sub('\r','', line)
            
            # Skip blank line
            if re.search('^ *$', line): 
                continue
            line_counter += 1
            
            for tran in parse_transaction(line):
                transaction_counter += 1
                logger.debug("Handling transaction: " + str(tran))
                [date, amount, info, orig_info] = tran
                
                if Transaction.objects.filter(Q(date__exact = date) & Q(amount__exact = amount) &\
                                               Q(original_info__exact = orig_info)).count() != 0:
                    logger.debug("Duplicated, skipping transaction.")
                    trans_reject_counter += 1
                else:
                    Transaction.objects.create(date = date,
                                                amount = amount,
                                                info = info,
                                                original_info = orig_info,
                                                source_file = SourceFile.objects.get(pk=file_id))
                    trans_accept_counter += 1
                    
    logger.info('Finished processing file: ' + uploaded_file.name)
    msg = uploaded_file.name + ": Parsed %s lines into %s transactions. %s Accepted. %s Rejected." \
            % (line_counter, transaction_counter, trans_accept_counter, trans_reject_counter)
    return(msg)
            
def parse_transaction(line):
    logger.info('Processing: ' + line)
    #import pdb; pdb.set_trace()
    
    line = re.sub('"', '', line)
    [date, amount, orig_desc, balance] = line.split(',')
    balance = balance.replace('\n','')
    
    # Removing extra spaces and double quotes
    desc = re.sub(" +", " ", orig_desc).upper()
    orig_desc = orig_desc + ' Balance:' + balance
    
    # ======= Possible date manipulation put in here =======
    # If Value Date found, the transaction happened at Value Date
    # Then Set date to Value Date
    pos = desc.find('VALUE DATE:')
    if pos != -1:
        # Value Date means credit account was used, and Cash Out should be allowed from saving account only 
        assert desc.find('CASH OUT') == -1 
        date = desc[pos+12:pos+22]
        desc = desc[:pos] + desc[pos+22:]
    
    # ======= No date manipulation Onwards =======
    # Change Date format from dd/mm/yyyy to yyyy-mm-dd
    date = date[6:10] + '-' + date[3:5] + '-' + date[0:2]
    
    transactions = []
    # If Cash Out found, the transaction needed to be break into two transactions
    pos_cashout = desc.find('CASH OUT')
    pos_purchase = desc.find('PURCHASE')
    
    if pos_cashout != -1 and pos_purchase != -1:
        cash_out_amount = '-' + desc[pos_cashout+10:pos_purchase-1]
        cash_out_desc = 'CASH OUT'
        
        purchase_amount = '-' + desc[pos_purchase+10:]
        purchase_desc = desc[:pos_cashout]
        
        transactions.append([date, cash_out_amount, cash_out_desc, orig_desc+':Split'])
        transactions.append([date, purchase_amount, purchase_desc, orig_desc])
    else:
        transactions.append([date, amount, desc, orig_desc])
    
    return transactions

#################################################################
########################## FOR CHARTS ###########################
#################################################################
def get_filtered_transactions(filter_name, transactions=None):
    ### GET ALL TRANSACTIONS
    #import pdb;pdb.set_trace()
    if transactions == None:
        transactions = Transaction.objects.select_related()
    
    ### GET FILTERS
    filters = FilterSQL.objects.select_related() \
        .filter(filter__filter_name__exact = filter_name) \
        .filter(filter_onoff__exact = 'enabled') \
        .values('filter_type','filter_sql')
    
    ### APPLY FILTERS
    for filter in filters:
        transactions = eval("transactions." + filter['filter_type'] + "(" + filter['filter_sql'] + ")")
        
    return transactions

def get_mix_chart_data():
    
    transactions = get_filtered_transactions('Mix Chart - MonthlyBalance')
    mix_chart_series = []
    
    # ------------------------ MONTHLY BALANCE LINE DATA ------------------------
    monthly_total = transactions \
                    .extra(select={'YYYY-MM':"date_format(date,'%%Y-%%m')"}, order_by = ['YYYY-MM']) \
                    .values('YYYY-MM') \
                    .annotate(month_total=Sum('amount'))
    
    month_name_in_list = [m['YYYY-MM'] for m in monthly_total]                
    monthly_IO_in_list = [m['month_total'] for m in monthly_total]
    
    monthly_balance = { 'type': 'spline',
                        'name': 'Balance',
                        'yAxis': 1,
                        'data': [
                               {'name':month_name_in_list[i],
                                'y':round(sum(monthly_IO_in_list[:i+1]),2)
                                }  for i in range(len(month_name_in_list)) 
                           ],
                         'tooltip': { 'valueSuffix': ' AU$' }
                       }
    
    # ------------------------ MONTHLY I/O BAR DATA ------------------------
    monthly_income_tran = get_filtered_transactions('Mix Chart - MonthlyBalance - Income', transactions=transactions)
    monthly_income = monthly_income_tran \
                    .extra(select={'YYYY-MM':"date_format(date,'%%Y-%%m')"}, order_by = ['YYYY-MM']) \
                    .values('YYYY-MM') \
                    .annotate(month_total=Sum('amount'))
                    
    monthly_income_for_chart = {
                    'type': 'column',
                    'name': 'Income',
                    'data':[{'name':m['YYYY-MM'],
                             'y':round(m['month_total'], 2)
                            } for m in list(monthly_income)]}
                    
    monthly_expense_tran = get_filtered_transactions('Mix Chart - MonthlyBalance - Expense', transactions=transactions)
    monthly_expense = monthly_expense_tran \
                    .extra(select={'YYYY-MM':"date_format(date,'%%Y-%%m')"}, order_by = ['YYYY-MM']) \
                    .values('YYYY-MM') \
                    .annotate(month_total=Sum('amount'))
                    
    monthly_expense_for_chart = {
                    'type': 'column',
                    'name': 'Expense',
                    'data':[{'name':m['YYYY-MM'],
                             'y':round(m['month_total'] * -1.0 , 2)
                            } for m in list(monthly_expense)]}
                    
                    
    
    return [monthly_income_for_chart, monthly_expense_for_chart, monthly_balance]

def get_bar_chart_data():
    
    transactions = get_filtered_transactions('Bar Chart - MonthlyView')
        
    # ------------------------ MONTHLY VIEW ------------------------ 
    monthly_total = transactions \
                    .extra(select={'YYYY-MM':"date_format(date,'%%Y-%%m')"}, order_by = ['YYYY-MM']) \
                    .values('YYYY-MM') \
                    .annotate(month_total=Sum('amount'))
    
    ### Pass as series.data                
    #monthlyView = [{'drilldown':m['YYYY-MM'],'name':m['YYYY-MM'],'y':m['month_total'] * -1.0} for m in list(monthly_total)]
    
    ### Pass as series
    monthlyView = [{'id': 'Monthly View',
                    'name': 'Monthly View',
                    'colorByPoint': True,
                    'data':[{'drilldown':m['YYYY-MM'],
                             'name':m['YYYY-MM'],
                             'y':round(m['month_total'] * -1.0 , 2)
                            } for m in list(monthly_total)]}]
    
    
    # ------------------------ MONTH-CATE DRILL DOWN ------------------------ 
    monthly_cate_total = transactions \
                    .extra(select={'YYYY-MM':"date_format(date,'%%Y-%%m')"}) \
                    .values('YYYY-MM','keyword__cate__cate') \
                    .annotate(month_cate_total=Sum('amount'))
                    
    monthlyDrilldown = {}
    
    for t in monthly_cate_total:
        this_level = t['YYYY-MM']
        next_level = t['YYYY-MM']+":"+t['keyword__cate__cate']
        if this_level in monthlyDrilldown.keys():
            #===================================================================
            # monthlyDrilldown[t['YYYY-MM']]['data'].append([cate_dict[t['keyword__cate']],t['month_cate_total'] * -1.0])
            #===================================================================
            monthlyDrilldown[this_level]['data'].append({'drilldown': next_level,
                                                         'name': t['keyword__cate__cate'], 
                                                         'y':round(t['month_cate_total'] * -1.0, 2)
                                                        })
        else:
            #===================================================================
            # monthlyDrilldown[t['YYYY-MM']] = {'id':t['YYYY-MM'],'name':t['YYYY-MM'],
            #                                   'data':[[cate_dict[t['keyword__cate']],t['month_cate_total'] * -1.0]]}
            #===================================================================
            monthlyDrilldown[this_level] = {'id':this_level,
                                            'name':this_level,
                                            'colorByPoint': True,
                                            'data':[{'drilldown': next_level,
                                                     'name':t['keyword__cate__cate'], 
                                                     'y':round(t['month_cate_total'] * -1.0, 2)
                                                    }]
                                            }

    #monthlyDrilldown = list(monthlyDrilldown.values())
    
    # ------------------------ MONTH-CATE-SUBCATE DRILL DOWN ------------------------ 
    monthly_cate_subcate_total= transactions \
                        .extra(select={'YYYY-MM':"date_format(date,'%%Y-%%m')"}) \
                        .values('YYYY-MM','keyword__cate__cate','keyword__sub_cate__sub_cate') \
                        .annotate(month_cate_subcate_total=Sum('amount'))
                        
    monthlySubCateDrilldown = {}
    
    for t in monthly_cate_subcate_total:
        this_level = t['YYYY-MM']+":"+t['keyword__cate__cate']
        if this_level in monthlySubCateDrilldown.keys():
            monthlySubCateDrilldown[this_level]['data'].append({'name':t['keyword__sub_cate__sub_cate'], 
                                                                'y':round(t['month_cate_subcate_total'] * -1.0, 2)
                                                                })
        else:
            monthlySubCateDrilldown[this_level] = {'id':this_level,
                                                   'name':this_level,
                                                   'data':[{'name':t['keyword__sub_cate__sub_cate'], 
                                                              'y':round(t['month_cate_subcate_total'] * -1.0, 2)
                                                           }]
                                                   }
    
    #monthlySubCateDrilldown = list(monthlySubCateDrilldown.values())
    
    return [monthlyView, monthlyDrilldown, monthlySubCateDrilldown]
