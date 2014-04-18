from django.db.models import Q
from ozio.models import *
import logging, re
logger = logging.getLogger(__name__)

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
    msg = "Parsed %s lines into %s transactions. %s Accepted. %s Rejected." \
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