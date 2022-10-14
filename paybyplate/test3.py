'''
ocr bot extracting data from pay by plate agencny
'''
import re
from sre_parse import State
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
with pdfplumber.open('./scn_123_pay_by_plate_ma-amazon_(5)_august_19_(bm).pdf') as pdf:
    #creating a loop to loop through the entire pdf opened
    for x, text in enumerate(pdf.pages):
        page = pdf.pages[x]
        page_data = page.extract_text()
        # print(page_data)

        license_plate = re.findall(r'\wR\W*([\-|\W*]\w*)\W*\w*\W*\w*\W*\d{2}\/\d{2}\/\d{4}\W*\d{2}\W\d{2}\W\d{2}\W*\w*\W*\w*\W*\d*\W*[\$|\W]\d*\W*\d*', page_data)
        trxn_date_time = re.findall(r'\wR\W*[\-|\W*]\w*\W*\w*\W*\w*\W*(\d{2}\/\d{2}\/\d{4}\W*\d{2}\W\d{2}\W\d{2})\W*\w*\W*\w*\W*\d*\W*[\$|\W]\d*\W*\d*', page_data)
        state = re.findall(r'(\wR)\W*[\-|\W*]\w*\W*\w*\W*\w*\W*\d{2}\/\d{2}\/\d{4}\W*\d{2}\W\d{2}\W\d{2}\W*\w*\W*\w*\W*\d*\W*[\$|\W]\d*\W*\d*', page_data)
        invoice_number = re.findall(r'\woice\WNumber\W*(\d*)', page_data)
        amount_due = re.findall(r'\wR\W*[\-|\W*]\w*\W*\w*\W*\w*\W*\d{2}\/\d{2}\/\d{4}\W*\d{2}\W\d{2}\W\d{2}\W*\w*\W*\w*\W*\d*\W*([\$|\W]\d*\W*\d*)', page_data)
        exit_lane = re.findall(r'\wR[\-|\W*]\w*\W*\w*\W*\w*\W*\d{2}\/\d{2}\/\d{4}\W*\d{2}\W\d{2}\W\d{2}\W*(\w*\W*\w*\W*\d*)\W*[\$|\W]\d*\W*\d*', page_data)
        print(license_plate)
        
        if len(amount_due) > 0:
            stored_data['Amount due'] = amount_due
            index = 0
            while index < len(amount_due):
                stored_data['license plate'] = license_plate[index]
                stored_data['Transaction date & time'] = trxn_date_time
                stored_data['State'] = State
                stored_data['Invoice #'] = invoice_number
                
                stored_data['Exit Lane'] = exit_lane
                df = df.append(stored_data, ignore_index = True)
                index += 1
            print(df)
            df.to_excel('paybyplate77.xlsx', index=False)



    #     for lp in license_plate:
    #         print(lp)
    #         stored_data['license plate'] = lp
    #     for trxn in trxn_date_time:
    #         print(trxn)
    #         stored_data['Transaction date & time'] = trxn
    #     for st in state:
    #         print(st)
    #         stored_data['State'] = st
    #     for inv in invoice_number:
    #         print(inv)
    #         stored_data['Invoice #'] = inv
    #     for amt in amount_due:
    #         print(amt)
    #         stored_data['Amount due'] = amt
    #         print(stored_data['Amount due'])
    #     for el in exit_lane:
    #         print(el)
    #         stored_data['Exit Lane'] = el
    #         df = df.append(stored_data, ignore_index = True)
    #         df.drop_duplicates(inplace = True)
    # print(df)
    # df.to_excel('paybyplate.xlsx', index=False)