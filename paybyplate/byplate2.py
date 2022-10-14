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
    'Due Date':None
}

df = pd.DataFrame()

#opening the pdf to extract data from
with pdfplumber.open('./angie/scan_2mt_amazon_pay_by_plate_ma_(23)_oct_3_(nko).pdf') as pdf:
    #creating a loop to loop through the entire pdf opened
    for x, text in enumerate(pdf.pages):
        page = pdf.pages[x]
        page_data = page.extract_text()
        # print(page_data)

        all_data = re.findall(r'(\wR|\wN)\D*(\w{7}|...\w{5})\D*(\d*\/\d*\/\d{4}\D*\d*\:\d*\:\d*).(\D*.).\D*(\d*\D*\d*\n)', page_data)
        invoice_number = re.findall(r'\woice\WNumber\W*(\d*)', page_data) 

        # for inv in invoice_number:
        for inv in invoice_number:
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

            df = df.append(stored_data, ignore_index = True)
            # df.drop_duplicates(inplace = True)
        print(df)
        df.to_excel('paybyplate23.xlsx', index=False)
            
#             license_plate = re.findall(r'\wR\D*(\w{7}|...\w{5})\D*\d*\/\d*\/\d{4}\D*\d*\:\d*\:\d*.\D*..\D*\d*\D*\d*\n', al)
#             trxn_date_time = re.findall(r'\wR\W*[\-|\W*]\w*\W*\w*\W*\w*\W*(\d{2}\/\d{2}\/\d{4}\W*\d{2}\W\d{2}\W\d{2})\W*\w*\W*\w*\W*\d*\W*[\$|\W]\d*\W*\d*', al)
#             state = re.findall(r'(\wR)\D*\w{7}|...\w{5}\D*\d*\/\d*\/\d{4}\D*\d*\:\d*\:\d*.\D*..\D*\d*\D*\d*\n', al)
#             invoice_number = re.findall(r'\woice\WNumber\W*(\d*)', al)
#             amount_due = re.findall(r'\wR\W*[\-|\W*]\w*\W*\w*\W*\w*\W*\d{2}\/\d{2}\/\d{4}\W*\d{2}\W\d{2}\W\d{2}\W*\w*\W*\w*\W*\d*\W*([\$|\W]\d*\W*\d*)', al)
#             exit_lane = re.findall(r'\wR[\-|\W*]\w*\W*\w*\W*\w*\W*\d{2}\/\d{2}\/\d{4}\W*\d{2}\W\d{2}\W\d{2}\W*(\w*\W*\w*\W*\d*)\W*[\$|\W]\d*\W*\d*', al)
#             print(license_plate)
            
#             # if license_plate:
#             for lp in license_plate:
#                 # print(lp)
#                 stored_data['license plate'] = lp
#             for trxn in trxn_date_time:
#                 print(trxn)
#                 # stored_data['Transaction date & time'] = trxn
#             for st in state:
#                 # print(st)
#                 stored_data['State'] = st
#             for inv in invoice_number:
#                 # print(inv)
#                 stored_data['Invoice #'] = inv
#             for amt in amount_due:
#                 # print(amt)
#                 stored_data['Amount due'] = amt
#                 # print(stored_data['Amount due'])
#             for el in exit_lane:
#                 print(el)
#                 stored_data['Exit Lane'] = el
                
#     print(df.to_string())
# df.to_excel('paybyplate77.xlsx', index=False)