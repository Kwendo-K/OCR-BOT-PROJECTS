'''
python ocr bot extracting data from mta bridges
and tunnels agency
'''
import re
import pandas as pd
import pdfplumber

df = pd.DataFrame()
stored_data = {
    'TOLL AGENCY':'PORT AUTHORITY NY NJ',
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

with pdfplumber.open('./scn_119_port_authority_ny__nj-amazon_(24)_october_14_(bm) (1).pdf') as pdf:
    for i, text in enumerate(pdf.pages):
        pages = pdf.pages[i]
        page_data = pages.extract_text()
        print(page_data)

        all_table = re.findall(r'(\w{13}\W+\w{5})\W+\S+\W+(\w{2})(\w{7})\W(\S+\W+\S+)\W+(\S+\W+\d+\W+\d+\W+\d+)\W+\d+\W+\d+\D+\d+\W+\d+\D+(\d+\W+\d+)|(\w{13}\W+\w{5})\W+(\w{2})(\w{7})\W+(\S+\W+\S+)\W+(\S+\W+\d+\W+\d+\W+\d+)\D+\d+\W+\d+\W+\S+\W+\S+\W+\S+\W+(\d+\W+\d+)', page_data)
        due_date = re.findall(r'Total Due by\W+(\d+\W+\d+\W+\d+)|is due\W+(\w+)|required(immediately)|full(immediately)|TotalDueby(\d+\D+\d+\D+\d+)', page_data)
        
        for d_d in due_date:
            dd = list(filter(None, d_d))
            d_due = ''.join(dd)
            # print(d_due.upper())
        for a_l in all_table:
            al = list(filter(None, a_l))
            # print(al)
            #storing the length of the table(al) in size variable
            size = len(al)
            # print(size)
            if size > 5:
                violation = al[0]
                state = al[1]
                lp = al[2]
                exit_lane = al[3]
                trxn_date = al[4]
                amount = al[5]
                # print(violation, state, lp, exit_lane, trxn_date, amount)
                stored_data['VIOLATION'] = violation
                stored_data['LP STATE'] = state
                stored_data['LP'] = lp
                stored_data['EXIT LANE/LOCATION'] = exit_lane
                stored_data['TRXN DATE & TIME'] = trxn_date
                stored_data['AMOUNT DUE'] = amount
                stored_data['DUE DATE'] = d_due.upper()
            elif size <= 5:
                violation = al[0]
                state = al[1]
                lp = al[2]
                exit_lane = al[3]
                trxn_date = al[4]

                stored_data['VIOLATION'] = violation
                stored_data['LP STATE'] = state
                stored_data['LP'] = lp
                stored_data['EXIT LANE/LOCATION'] = exit_lane
                stored_data['AMOUNT DUE'] = ''
                stored_data['TRXN DATE & TIME'] = trxn_date
                stored_data['DUE DATE'] = d_due.upper()
                # if d_due.isdigit():
                #     stored_data['DUE DATE'] = d_due
                # else:
                #     ddd = d_due.upper()
                #     stored_data['DUE DATE'] = ddd
                # print(violation, state, lp, exit_lane, trxn_date)
            df = df.append(stored_data, ignore_index=True)
            print(df)
df.to_excel('scan119.xlsx', index=False)