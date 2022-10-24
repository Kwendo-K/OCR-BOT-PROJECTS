'''
python ocr bot extracting data from mta bridges
and tunnels agency
'''
import re
import pandas as pd
import pdfplumber

df = pd.DataFrame()
stored_data = {
    'TOLL AGENCY':'MTA BRIGES AND TUNNELS(TOLLS BY MAIL)',
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
output_list = []

with pdfplumber.open('./scan_506mt_amazon-mta_(tolls_by_mail)_(7)_oct_23_(nko).pdf') as pdf:
    for i, text in enumerate(pdf.pages):
        pages = pdf.pages[i]
        page_data = pages.extract_text()
        # print(page_data)
        
        # all_table = re.findall(r'(\w{2})\W+(\S+)\W+\S+\W+(.*\w[a-zA-Z])\W+(\d{2}\W+\d{2}\W+\d+\W+\d{2}\W+\d{2}\W+\d{2})\W+(\d+\W+\d{2})|(\w{2})\W+(\S+)\W+\S+\W+(.*\w[a-zA-Z])\W+\w+\W+(\d{2}\W+\d{2}\W+\d+\W+\d{2}\W+\d{2}\W+\d{2})\W+(\d+\W+\d{2})', page_data)
        all_table = re.findall(r'(\wN|\wR)\W+(\S{7}|\S{6})\W+\S+\W+(.*)\w[a-zA-Z]\W+(.*)\W[$](\d+\W+\d{2})|(\wN|\wR)(\S{7}|\S{6})\W+\S+\W+(\S+\W+\S+)\W+\w+\W+(\S+\W+\S+)\W+(\d+\W+\d{2})', page_data)
        invoice = re.findall(r'TOLL BILL No:\W+(\S+)', page_data)
        due_date = re.findall(r'Received by\W+(\S{2}\W+\S{2}\W+\S{2})', page_data)

        for d_d in due_date:
            dd = d_d
        for i_nv in invoice:
            inv = i_nv
        for al in all_table:
            # print(all_table)
            state = al[0]
            license_plate = al[1]
            exit_lane = al[2].upper()
            trxn_date_time = al[3]
            amount = al[4]
            # print(al[0], al[1], al[2], al[3], al[4], al[5], pages)
            # print(state, license_plate, exit_lane, trxn_date_time, inv, amount, pages)

            stored_data['LP'] = license_plate
            stored_data['LP STATE'] = state
            stored_data['EXIT LANE/LOCATION'] = exit_lane
            stored_data['REF # OR INVOICE #'] = inv
            stored_data['AMOUNT DUE'] = amount
            stored_data['TRXN DATE & TIME'] = trxn_date_time
            stored_data['DUE DATE'] = dd

            # output_list.append(stored_data)
            # df = pd.concat([df, pd.DataFrame([output_list])])
            df = df.append(stored_data, ignore_index=True)
        print(df)
df.to_excel('tollsbymail506.xlsx', index=False)