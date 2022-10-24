'''
python ocr bot extracting data from mta bridges
and tunnels agency
'''
import re
import pandas as pd
import pdfplumber

df = pd.DataFrame()
stored_data = {
    'TOLL AGENCY':'MTA BRIGES AND TUNNELS',
    'LP':None,
    'LP STATE':None,
    'TRXN DATE & TIME':None,
    'EXIT LANE/LOCATION':None,
    'ACCOUNT':None,
    'REF # OR INVOICE #':None,
    'VIOLATION':None,
    'AMOUNT DUE':None,
    'DUE DATE':None,
    'PIN #':None
}

with pdfplumber.open('./scan_294mt_amazon_mta_(bridges__tunnels)_(29)_oct_17_(nko).pdf') as pdf:
    for i, text in enumerate(pdf.pages):
        pages = pdf.pages[i]
        page_data = pages.extract_text()
        # print(page_data)
        
        # all_table = re.findall(r'(\w{13}\D+\w{5})\s+\w+\s+(\w{2})\s+(\w+)\s+(\w+|\D*\s+\d+)\s+(\d{2}\W+\d{2}\W+\d+\s+\d{2}\W+\d{2}\W+\d{2})\W+\S+\W+\S+\D+(\d+\D+\d+)', page_data)
        # all_table = re.findall(r'(\w{13}\W+\w{5})\W+\S+\W+(\w{2})(\w{7})\W+(\S+\W+\S+)\W+(\S+\W+\d+\D+\d+\D+\d+)\W+\S+\W+\S+\W+(\d+\D+\d+)|(\w{13}\W+\w{5})\W+\S+\W+(\w{2})\W+(\S+)\W+(\S+\W+\S+)\W+(\S+\W+\d+\W+\d+\W+\d+)\W+\S+\W+\S+\W+(\d+\W+\d+)|(\w{13}\D+\w{5})\s+\w+\s+(\w{2})\s+(\w+)\s+(\w+|\D*\s+\d+)\s+(\d{2}\W+\d{2}\W+\d+\s+\d{2}\W+\d{2}\W+\d{2})\W+\S+\W+\S+\D+(\d+\D+\d+)', page_data)
        all_table = re.findall(r'(\w{13}\W+\w{5})\W+\S+\W+(\w{2})(\w{7})\W+(\S+\W+\S+)\W+(\S+\W+\d+\D+\d+\D+\d+)\D+\S+\D+\S+\D+(\d+\D+\d+)|(\w{13}\W+\w{5})\W+\S+\W+(\w{2})\W+(\S+)\W+(\S+\W+\S+)\W+(\S+\W+\d+\W+\d+\W+\d+)\W+\S+\W+\S+\W+(\d+\W+\d+)', page_data)
        # due_date = re.findall(r'Due by\s+(\d{2}\W+\d{2}\W+\d{4})|Due is required\s+(\w+)', page_data)
        due_date = re.findall(r'Due by\s+(\d{2}\W+\d{2}\W+\d{4})|Due by(\d+\D+\d+\D+\d+)|Due is required\s+(\w+)|Dueisrequired(\w+)', page_data)
        for d in due_date:
            dd = list(filter(None, d))
            print(dd)
            d_due = ''.join(dd)
            # print(d_due)
        for al in all_table:
            # print(al)

            #getting ref #/violation #
            reference = al[0]
            state = al[1]
            lp = al[2]
            exit_lane = al[3]
            trxn_date_time = al[4]
            amount = al[5]
            
            #appending extracted data to a dictionary
            stored_data['LP'] = lp
            stored_data['LP STATE'] = state
            stored_data['TRXN DATE & TIME'] = trxn_date_time
            stored_data['EXIT LANE/LOCATION'] = exit_lane
            stored_data['ACCOUNT'] = ''
            stored_data['REF # OR INVOICE #'] = ''
            stored_data['VIOLATION'] = reference
            stored_data['AMOUNT DUE'] = amount
            if d_due.isdigit():
                stored_data['DUE DATE'] = d_due
            else:
                due_d = d_due.upper()
                stored_data['DUE DATE'] = due_d
            stored_data['PIN #'] = ''
            # print(stored_data)

            df = df.append(stored_data, ignore_index = True)
        print(df)
df.to_excel('scan294.xlsx', index=False)