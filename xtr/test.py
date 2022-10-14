"""
A python ocr bot extracting data from XTRA agency
"""
import re
import pandas as pd
import pdfplumber

df = pd.DataFrame()

stored_data = {
    'TOLL AGENCY':None,
    'LP':None,
    'TRXN DATE & TIME':None,
    'EXITLANE/LOCATION':None,
    'ACCOUNT #':None,
    'REFERENCE # OR INVOICE #':None,
    'VIOLATION':None,
    'AMOUNT DUE':None,
    'DUE DATE':None,
    'PIN #':None
}

with pdfplumber.open('./SCAN_676_AMAZON_RENTAL_XTRA_TOLLS_SEPTEMBER_26_(SN).pdf') as pdf:
    for i, text in enumerate(pdf.pages):
        pages = pdf.pages[i]
        page_data = pages.extract_text()
        # print(page_data)
        # print(page_data)

        invoice = re.findall(r'^Invoice\s*No\W*(\d*)\nInvoice\s*\Date\s*\d{2}\W*\d{2}\W*\d{4}', page_data)
        license_plate = re.findall(r'(\w{6}|d{6})\s*\w{9}\s*\S*\s*\w*\W*\d{2}\W*', page_data)
        agency_exit_time = re.findall(r'Toll\s*\w*\s*\d{2}\W*\d{2}\W*\d{4}\s*\d{2}\W*\d{2}\W*\d{4}\W*(\d*\W*\d*)\W*\w*\n(\w*\W*\w*\W*\w*\W*\w*\W*\w*\s*\D*)loc(\D*)(\d*\D*\d*\D*\d*\D*\d*\D*\d*)', page_data)
        amount_due = re.findall(r'Toll\s*\w*\s*\d{2}\W*\d{2}\W*\d{4}\s*\d{2}\W*\d{2}\W*\d{4}\W*(\d*\W*\d*)', page_data)
        trxn_date_time = re.findall(r'\wn\W*(\d{4}\W*\d{2}\W*\d{2}\W*\d{2}\W*\d{2})', page_data)

        # for inv in invoice:
        #     print(inv)
        
        for lp in license_plate:
            stored_data['LP'] = lp
           
        for trxn in trxn_date_time:
            stored_data['TRXN DATE & TIME'] = trxn
        for amt in amount_due:
            stored_data['AMOUNT DUE'] = amt
        for al in agency_exit_time:
            agency = al[1]
            exit_lane = al[2]
            stored_data['TOLL AGENCY'] = agency
            stored_data['EXITLANE/LOCATION'] = exit_lane
            # print(agency)
            # print(exit_lane)
        for inv in invoice:
            stored_data['REFERENCE # OR INVOICE #'] = inv

        print(lp, trxn, pages,)
        print('---------------------')

        # df = df.append(stored_data, ignore_index = True)
        # print(df)
        # df.to_excel('scan676.xlsx', index=False)
            
        
        
        # for lp in license_plate:
        #     stored_data['LP'] = lp
        # for trxn in trxn_date_time:
        #     pass
        # for ag in agency_exit_time:
        #     # amount_due = ag[0]
        #     agency = ag[1]
        #     exit_lane = ag[2]
        #     # trxn_date_time = ag[3]
            
        #     #storing all the data in a dictionary
        #     stored_data['TOLL AGENCY'] = agency
        #     stored_data['TRXN DATE & TIME'] = trxn
        #     stored_data['EXITLANE/LOCATION'] = exit_lane
        #     stored_data['ACCOUNT #'] = ''
        #     stored_data['VIOLATION'] = ''
        #     stored_data['AMOUNT DUE'] = amount_due

        # df = df.append(stored_data, ignore_index = True)
        # print(df)
        # df.to_excel('scan676.xlsx', index=False)