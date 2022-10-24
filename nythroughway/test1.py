'''
Ny througway python ocr script
'''
import re
import pandas as pd
import pdfplumber

df = pd.DataFrame()

stored_data = {
    'TOLL AGENCY':'NEW YORK THRUWAY',
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

with pdfplumber.open('./scn_91_ny_thruway-amazon_(3)_october_13_(bm).pdf') as pdf:
    for i, text in enumerate(pdf.pages):
        pages = pdf.pages[i]
        page_data = pages.extract_text()
        # print(page_data)

        transactions = re.findall(r'(\w{13}\W+\w{5})\W+(\w{2})\W+(\S{7})\D+\w+\D+(\S+)\W+(\S+\W+\d+\D+\d+\D+\d+)\W+\d+\D+\d+\D+\d+\D+\d+\D+(\d+\D+\d+)|(.*[-]\w{5})\W+(\w{2})\W+(\w{7})\W+\w+\W+(\S+)\W+(\S+\W+\d+\D+\d+\D+\d+)\W+\d+\D+\d+\D+\d+\D+\d+\D+(\d+\D+\d+)', page_data)

        for t_r in transactions:
            tr = list(filter(None, t_r))
            print(tr)

            violation = tr[0]
            state = tr[1]
            lp = tr[2]
            exit_lane = tr[3]
            trxn_date = tr[4]
            amount = tr[5]

            stored_data['LP STATE'] = state
            stored_data['LP'] = lp
            stored_data['EXIT LANE/LOCATION'] = exit_lane
            stored_data['VIOLATION'] = violation
            stored_data['TRXN DATE & TIME'] = trxn_date
            stored_data['AMOUNT DUE'] = amount

            df = df.append(stored_data, ignore_index=True)
        print(df)
df.to_excel('NYT91.xlsx', index=False)