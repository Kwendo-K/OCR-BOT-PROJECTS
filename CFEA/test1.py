'''
A python script extracting data from CFEA agency
'''

import re
import pandas as pd
import pdfplumber

df = pd.DataFrame()

stored_data = {
    'TOLL AGENCY':'',
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

with pdfplumber.open('./scn_176_cfea(pay_by_plate)-amazon_(3)_october_20_(bm).pdf') as pdf:
    for i, text in enumerate(pdf.pages):
        pages = pdf.pages[i]
        page_data = pages.extract_text()
        # print(page_data)

        exit_trxn_amt = re.findall(r'(.*\D[()]\W+\S+)\W+(\d+\W+\d+\W+\d+\W+\d+\W+\d+\W+\d{2}\W+\wM)\W+(\d+\W+\d{2})|(.*\D[()]\W+\S+)\W+(\d+\D+\d+\D+\S+\W+\wM)\D+(\d+\D+\d+)', page_data)
        inv_lp_st_dte_total = re.findall(r'(\w{8})\W+(\w{7})\W+(\w{2})\W+(\d{2}\W+\d{2}\W+\d+)\W+(\d{2}\W+\d{2}\W+\d+)\W+(\d+\W+\d+)', page_data)
        for d_t in inv_lp_st_dte_total:
            dt = list(d_t)
            # print(dt)
            invoice = dt[0]
            lp = dt[1]
            state = dt[2]
            date_due = dt[4]
            total_amount = dt[5]
            print(invoice, lp, state, date_due, total_amount)
        for e_x in exit_trxn_amt:
            ex = list(e_x)
            exit_lane = ex[0]
            trxn_date_time = ex[1]
            amount = ex[2]
            
            stored_data['LP'] = lp
            stored_data['LP STATE'] = state
            stored_data['TRXN DATE & TIME'] = trxn_date_time
            stored_data['EXIT LANE/LOCATION'] = exit_lane
            stored_data['REFERENCE # OR INVOICE #'] = invoice
            stored_data['DUE DATE'] = date_due
            stored_data['AMOUNT DUE'] = amount

            df = df.append(stored_data, ignore_index = True)
        print(df)
df.to_excel('scan176.xlsx', index=False)
            # print(exit_lane, exit_lane, trxn_date_time, amount)