'''
ocr bot extracting data from pay by plate agencny
'''
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
with pdfplumber.open('./angie/scan_102mt_amazon__pay_by_plate_ma_(46)_oct_6_(jm).pdf') as pdf:
    #creating a loop to loop through the entire pdf opened
    for x, text in enumerate(pdf.pages):
        print(f"Page {x}")
        page = pdf.pages[x]
        page_data = page.extract_text()
        # print(page_data)

        # all_data = re.findall(r'(\wR|\wN)\D*(\w{7}|...\w{5})\D*(\d*\/\d*\/\d{4}\D*\d*\:\d*\:\d*).(\D*.)\d.(\D*\d*\D*\d*\n)', page_data)
        all_data = re.findall(r'(\wR|\wN)\D*(\w{7}|...\w{5})\D*(\d*\/\d*\/\d{4}\D*\d*\:\d*\:\d*).(\D*.)\d.\D*(\d*\D*\d*\n)', page_data)
        invoice_number = re.findall(r'\woice\WNumber\W*(\d*)', page_data)
        prev_balance = re.findall(r'\$(\d*\W*\d*)\s*\$(\d*\W*\d*)\s*\$(\d*\W*\d*)\s*\$(\d*\W*\d*)\s*\$(\d*\W*\d*)\s*(\d{2}\W*\d*\W*\d*|\w*)', page_data)
        non_ma_fee = re.findall(r'Non\s+MA\s+Fee\s+\d{2}\W+\d{2}\W+\d{4}\s+\d{2}\W+\d{2}\W+\d+\s+\W+(\d+\W+\d+)', page_data)
        invoice_fee = re.findall(r'Invoice\W*Fee\W*\d{2}\W*\d{2}\W*\d{4}\W*\d{2}\W*\d{2}\W*\d{2}\W*(\d\W*\d*)', page_data)
        # due_date = re.findall(r'', page_data)

        extra_fee = 0
        for n_fee in non_ma_fee:
            # print(n_fee)
            if "." in n_fee:
                extra_fee += float(n_fee)

        # print(all_data)
        # for inv in invoice_number:
        for inv in invoice_number:
            pass
        for prev_bal in prev_balance:
            prev_b = prev_bal[0]
            due_date = prev_bal[5]
        for f_fee in invoice_fee:
            fee = f_fee
        
        
        final_trans_index = len(all_data) - 1
        trans_index = 0
        for al in all_data:
            state = al[0]
            license_plate = al[1]
            trxn_date_time = al[2]
            exit_lane = al[3].upper()
            amt_due = al[4]
            

            stored_data['LP STATE'] = state
            stored_data['LP'] = license_plate
            stored_data['TRXN DATE & TIME'] = trxn_date_time
            stored_data['EXIT LANE/LOCATION'] = exit_lane
            stored_data['REFERENCE # OR INVOICE #'] = inv
            final_amt_due = float(amt_due) if trans_index != final_trans_index else float(amt_due) + float(fee) + extra_fee
            stored_data['AMOUNT DUE'] = final_amt_due
            if due_date.isdigit():
                stored_data['DUE DATE'] = due_date
            else:
                d = due_date.upper()
                stored_data['DUE DATE'] = d
                print(stored_data['DUE DATE'])
            # stored_data['Previous Balance'] = prev_bal[0]

            # df = df.astype({'Amount due':'float64'})
            df = pd.concat([df, pd.DataFrame([stored_data])])
            df.drop_duplicates(inplace = True)
            trans_index += 1

        if len(prev_balance) > 0:
            
            # stored_data['LP'] = ""
            stored_data['TRXN DATE & TIME'] = ""
            stored_data['EXIT LANE/LOCATION'] = ""
            # stored_data['REFERENCE # OR INVOICE #'] = ""
            stored_data['AMOUNT DUE'] = prev_b
            stored_data['DUE DATE'] = ""
            df = df.append(stored_data, ignore_index = True)
        print(df)
df.to_excel('paybyplate102.xlsx', index=False)
