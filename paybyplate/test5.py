'''
ocr bot extracting data from pay by plate agencny
'''
import re
import pandas as pd
import pdfplumber

#creating a dictionary to append data extracted from the pdf
stored_data = {
    'Toll Agency':'Pay by plate',
    'license plate':None,
    'Transaction date & time':None,
    'State':None,
    'Invoice #':None,
    'Amount due':None,
    'Exit Lane':None,
    'Due Date':None,
    'Previous Balance':None
}

df = pd.DataFrame()

#opening the pdf to extract data from
with pdfplumber.open('./scan_401mt_amazon_pay_by_plate_ma_(32)_sept_23_(nko).pdf') as pdf:
    #creating a loop to loop through the entire pdf opened
    for x, text in enumerate(pdf.pages):
        page = pdf.pages[x]
        page_data = page.extract_text()
        # print(page_data)

        all_data = re.findall(r'(\wR|\wN)\D*(\w{7}|...\w{5})\D*(\d*\/\d*\/\d{4}\D*\d*\:\d*\:\d*).(\D*.).(\D*\d*\D*\d*\n)', page_data)
        invoice_number = re.findall(r'\woice\WNumber\W*(\d*)', page_data)
        prev_balance = re.findall(r'(\$\d*\W*\d*)\s*(\$\d*\W*\d*)\s*(\$\d*\W*\d*)\s*(\$\d*\W*\d*)\s*(\$\d*\W*\d*)\s*(\d{2}\W*\d*\W*\d*)', page_data)

        # for inv in invoice_number:
        for inv in invoice_number:
            pass
        for prev_bal in prev_balance:
            pass
        for al in all_data:
            state = al[0]
            license_plate = al[1]
            trxn_date_time = al[2]
            exit_lane = al[3]
            amt_due = al[4]
            

            stored_data['State'] = state
            stored_data['license plate'] = license_plate
            stored_data['Transaction date & time'] = trxn_date_time
            stored_data['Exit Lane'] = exit_lane
            stored_data['Invoice #'] = inv
            stored_data['Amount due'] = amt_due
            stored_data['Previous Balance'] = prev_bal[0]

            df = df.append(stored_data, ignore_index = True)
            # df.drop_duplicates(inplace = True)
        print(df)
        df.to_excel('paybyplate401.xlsx', index=False)