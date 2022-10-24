'''
ocr bot extracting data from pay by plate agencny
'''
from multiprocessing.resource_sharer import stop
import re
import pandas as pd
import pdfplumber

#creating a dictionary to append data extracted from the pdf
stored_data = {
    'TOLL AGENCY':'PAY BY PLATE MA',
    'LP':None,
    'LP STATE':None,
    'TRXN DATE & TIME':None,
    'EXIT LANE/LOCATION':None,
    'ACCOUNT':None,
    'REFERENCE # OR INVOICE #':None,
    'VIOLATION':None,
    'AMOUNT DUE':None,
    'DUE DATE':None,
    'PIN #':None
}

df = pd.DataFrame()

#opening the pdf to extract data from
with pdfplumber.open('./scan_102mt_amazon__pay_by_plate_ma_(46)_oct_6_(jm).pdf') as pdf:
    #creating a loop to loop through the entire pdf opened
    for x, text in enumerate(pdf.pages):
        # print(f"Page {x}")
        page = pdf.pages[x]
        page_data = page.extract_text()
        # print(page_data)

        transactions = re.findall(r'\d+\W+\d+\W+\d+\W+\w+\W+\D+\W+(\w{2})\W+(\w{7})\D+(\d+\W+\d+\W+\d+\W+\d+\W+\d+\W+\d+)\W+(\D+)\w+\W+(\d+\W+\d+)|\d+\W+\d+\W+\d+.*[()]\W+(\w{2})\W+(\w{7})\W+(\S+\W+\S+)\W+(\D+)\d+\W+(\d+\W+\d+)', page_data)
        invoice_fee = re.findall(r'\d+\W+\d+\W+\d+\W+Invoice Fee\W+\d+\W+\d+\W+\d+\W+\d+\W+\d+\W+\d+\W+(\d+\W+\d+)', page_data)
        prev_balance = re.findall(r'', page_data)
        
        for i_v in invoice_fee:
            inv_fee = i_v

        last_transaction_index = len(transactions) - 1
        transaction_index = 0
        for t_r in transactions:
            tr = list(filter(None, t_r))
            state = tr[0]
            lp = tr[1]
            trxn_date_time = tr[2]
            exit_lane = tr[3]
            amount = tr[4]

            if  transaction_index != last_transaction_index:
                stored_data['AMOUNT DUE'] = float(amount)
            else:
                final_amount = float(amount) + float(inv_fee)
                stored_data['AMOUNT DUE'] = final_amount
            stored_data['LP STATE'] = state
            stored_data['LP'] = lp
            stored_data['TRXN DATE & TIME'] = trxn_date_time
            stored_data['EXIT LANE/LOCATION'] = exit_lane.upper()

            df = df.append(stored_data, ignore_index=True)
        print(df)