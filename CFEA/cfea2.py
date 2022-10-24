'''
A python script extracting data from CFEA agency
'''

import re
import pandas as pd
import pdfplumber

df = pd.DataFrame()

stored_data = {
    'TOLL AGENCY':'CENTRAL FLORIDA EXPRESSWAY AUTHORITY',
    'LP':None,
    'LP STATE':None,
    'TRXN DATE & TIME':None,
    'EXIT LANE/LOCATION':None,
    'ACCOUNT':None,
    'REFERENCE # OR INVOICE #':None,
    'VIOLATION':None,
    'AMOUNT DUE':None,
    'DUE DATE':None,
}

with pdfplumber.open('./scan_298mt_amazon_cfea_(22)_oct_17_(nko).pdf') as pdf:
    for i, text in enumerate(pdf.pages):
        pages = pdf.pages[i]
        page_data = pages.extract_text()
        # print(page_data)

        # exit_trxn_amt = re.findall(r'(.*\D[()]|.*\D[()]\W+\S+)\W+(\d+\W+\d+\W+\d+\W+\d+\W+\d+\W+\d{2}\W+\wM)\W+(\d+\W+\d{2})|(.*\D[()]\W+\S+)\W+(\d+\W+\d+\W+\d+\W+\d+\W+\d+\W+\d{2}\W+\wM).*[$](\d+\W+\d{2})', page_data)
        exit_trxn_amt = re.findall(r'(.*\D[()]\W+\S+|.*\D[()]])\W+(.*)[$](\d+\W+\d+)|(.*\D[()]|.*\D[()]\W+\S+)\W+(\d+\W+\d+\W+\d+\W+\d+\W+\d+\W+\d{2}\W+\wM)\W+(\d+\W+\d{2})|(.*\D[()]\W+\S+)\W+(\d+\W+\d+\W+\d+\W+\d+\W+\d+\W+\d{2}\W+\wM).*[$](\d+\W+\d{2})', page_data)
        inv_lp_st_dte_total = re.findall(r'(\w{8})\W+(\w{7})\W+(\w{2})\W+\d+\W+\d+\W+\d+\W+(\d+\W+\d+\W+\d+)\W+(\d+\W+\d+)|(\w{8})\W+(\w{7})(\w{2})\W+\d+\W+\d+\W+\d+\W+(\d+\W+\d+\W+\d+)\W+(\d+\W+\d+)|(\w{8})\W+(\w{7})(\w{2})\W+(\d+\W+\d+\W+\d+)\W+(\d+\W+\d+)', page_data)
        inv_lp_st_dte_total2 = re.findall(r'Reference \W+(\w{8})\W+License Plate\W+(\w{7}|\w{6})\W+(\S{2})\W+.*\W+Amount Due\W+(\d+\D+\d+)\W+Due Date\W+(\d+\D+\d+\D+\d+)|Reference \W+(\w{8})\W+License Plate\W+(\w{7}|\w{6})\W+(\w{2})\W+.*\W+.*\W+Amount Due\W+(\d+\W+\d+)\W+Due Date\W+(\d+\D+\d+\D+\d+)', page_data)
        
        for i_v in inv_lp_st_dte_total:
            iv = list(filter(None, i_v))
            # print(iv)
            invoice = iv[0]
            lp = iv[1]
            state = iv[2]
            due_date = iv[3]
            total_amount = iv[4]
            # print(invoice)
            if len(exit_trxn_amt) <= 0:
                if len(inv_lp_st_dte_total) > 0:
                    stored_data['LP'] = lp
                    stored_data['LP STATE'] = state
                    stored_data['TRXN DATE & TIME'] = ''
                    stored_data['EXIT LANE/LOCATION'] = ''
                    stored_data['REFERENCE # OR INVOICE #'] = invoice
                    stored_data['DUE DATE'] = due_date
                    stored_data['AMOUNT DUE'] = total_amount

                    df = df.append(stored_data, ignore_index=True)
                elif len(inv_lp_st_dte_total) <= 0:
                    for i_v2 in inv_lp_st_dte_total2:
                        iv2 = list(filter(None, i_v2))
                        # print(iv2)
                        invoice2 = iv2[0]
                        lp2 = iv2[1]
                        state2 = iv2[2]
                        total_amount2 = iv2[3]
                        due_date2 = iv2[4]

                        stored_data['LP'] = lp2
                        stored_data['LP STATE'] = state2
                        stored_data['TRXN DATE & TIME'] = ''
                        stored_data['EXIT LANE/LOCATION'] = ''
                        stored_data['REFERENCE # OR INVOICE #'] = invoice2
                        stored_data['DUE DATE'] = due_date2
                        stored_data['AMOUNT DUE'] = total_amount2

                        df = df.append(stored_data, ignore_index=True)
            # print(df)
            
        for e_x in exit_trxn_amt:
            ex = list(e_x)
            exit_lane = ex[0]
            trxn_date_time = ex[1]
            amount = ex[2]

            if len(exit_trxn_amt) >= 1:
                stored_data['LP'] = lp
                stored_data['LP STATE'] = state
                stored_data['TRXN DATE & TIME'] = trxn_date_time
                stored_data['EXIT LANE/LOCATION'] = exit_lane
                stored_data['REFERENCE # OR INVOICE #'] = invoice
                stored_data['DUE DATE'] = due_date
                stored_data['AMOUNT DUE'] = amount
                df = df.append(stored_data, ignore_index=True)
        print(df)
df.to_excel('CFEA298.xlsx', index=False)
