'''
ocr bot extracting data from pay by plate agencny
'''
import re
import pandas as pd
import pdfplumber

#creating a dictionary to append data extracted from the pdf
stored_data = {
    'Toll Agency':'PAY BY PLATE MA',
    'license plate':None,
    'State':None,
    'Transaction date & time':None,
    'Exit Lane':None,
    'Account':None,
    'Invoice # Ref #':None,
    'Amount due':None,
    'Due Date':None,
}

df = pd.DataFrame()

#opening the pdf to extract data from
with pdfplumber.open('./angie/scan_495mt_amazon_pay_by_plate_(36)_sept_28_(nko).pdf') as pdf:
    #creating a loop to loop through the entire pdf opened
    for x, text in enumerate(pdf.pages):
        print(f"Page {x}")
        page = pdf.pages[x]
        page_data = page.extract_text()
        # print(page_data)

        # all_data = re.findall(r'(\wR|\wN)\D*(\w{7}|...\w{5})\D*(\d*\/\d*\/\d{4}\D*\d*\:\d*\:\d*).(\D*.)\d.(\D*\d*\D*\d*\n)', page_data)
        all_data = re.findall(r'(\wR|\wN)\D*(\w{7}|...\w{5})\D*(\d*\/\d*\/\d{4}\D*\d*\:\d*\:\d*).(\D*.)\d.(\D*\d*\D*\d*\n)\d{2}\W*\d{2}\W*\d{4}\W*\w*\W*\w*\W*\d{2}\W*\d{2}\W*\d{4}\W*\d{2}\W*\d{2}\W*\d{2}\s*(\W*\d*\W*\d*)', page_data)
        invoice_number = re.findall(r'\woice\WNumber\W*(\d*)', page_data)
        prev_balance = re.findall(r'(\$\d*\W*\d*)\s*(\$\d*\W*\d*)\s*(\$\d*\W*\d*)\s*(\$\d*\W*\d*)\s*(\$\d*\W*\d*)\s*(\d{2}\W*\d*\W*\d*)', page_data)
        
        # for inv in invoice_number:
        for inv in invoice_number:
            pass
        for prev_bal in prev_balance:
            pass
        if len(prev_balance) > 0:
            stored_data['State'] = ""
            stored_data['Transaction date & time'] = ""
            stored_data['Exit Lane'] = ""
            stored_data['Invoice # Ref #'] = ""
            stored_data['Amount due'] = prev_bal[0]
            df = df.append(stored_data, ignore_index = True)
        
        for al in all_data:
            state = al[0]
            license_plate = al[1]
            trxn_date_time = al[2]
            exit_lane = al[3]
            amt_due = al[4]
            inv_fee = al[5]
            

            stored_data['State'] = state
            stored_data['license plate'] = license_plate
            stored_data['Transaction date & time'] = trxn_date_time
            stored_data['Exit Lane'] = exit_lane
            stored_data['Invoice #'] = inv
            stored_data['Amount due'] = amt_due
            # stored_data['Previous Balance'] = prev_bal[0]

            df = df.append(stored_data, ignore_index = True)
            df.drop_duplicates(inplace = True)
        print(df)
        df.to_excel('paybyplate495.xlsx', index=False)