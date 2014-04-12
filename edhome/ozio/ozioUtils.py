from django.db.models import Q
from ozio.models import Transaction, SourceFile
import logging, re
logger = logging.getLogger(__name__)

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