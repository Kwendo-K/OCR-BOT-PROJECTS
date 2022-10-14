"""
A python ocr bot extracting data from XTRA agency
"""
import re
import pandas as pd
import pdfplumber

# df = pd.DataFrame()

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

with pdfplumber.open('./SCAN_675_AMAZON_RENTAL_XTRA_TOLLS_SEPTEMBER_26_(SN).pdf') as pdf:
    for i, text in enumerate(pdf.pages):
        df = pd.DataFrame()
        pages = pdf.pages[i]
        page_data = pages.extract_text()
        # print(page_data)
        # print(page_data)

        invoice = re.findall(r'^Invoice\s*No\W*(\d*)\nInvoice\s*\Date\s*\d{2}\W*\d{2}\W*\d{4}', page_data)
        license_plate = re.findall(r'(\w{6})\s*\d{9}\s*\w*\s*\w*\W*\d*', page_data)
        agency_exit_time = re.findall(r'(\w{6})\s*\d{9}\s*\w*\s*\w*\W*\d*\W*Toll\s*\w*\s*\d{2}\W*\d{2}\W*\d{4}\s*\d{2}\W*\d{2}\W*\d{4}\W*(\d*\W*\d*)\W*\w*\n(\w*\W*\w*\W*\w*\W*\w*\W*\w*\s*\D*)loc(\D*)(\d*\D*\d*\D*\d*\D*\d*\D*\d*)', page_data)
        # amount_due = re.findall(r'^Toll\s*\w*\s*\d{2}\W*\d{2}\W*\d{4}\s*\d{2}\W*\d{2}\W*\d{4}\W*(\d*\W*\d*) ', page_data)
        for inv in invoice:
            stored_data['REFERENCE # OR INVOICE #'] = inv
        for lp in license_plate:
            stored_data['LP'] = lp
        for ag in agency_exit_time:
            outputlist =[]
            stored_data['LP'] = ag[0]
            amount_due = ag[1]
            agency = ag[2]
            exit_lane = ag[3]
            trxn_date_time = ag[4]
            
            #storing all the data in a dictionary
            
            
            stored_data['TOLL AGENCY'] = agency
            # stored_data['REFERENCE # OR INVOICE #'] = inv
            stored_data['TRXN DATE & TIME'] = trxn_date_time
            stored_data['EXITLANE/LOCATION'] = exit_lane
            stored_data['ACCOUNT #'] = ''
            stored_data['VIOLATION'] = ''
            stored_data['AMOUNT DUE'] = amount_due

            # print(stored_data['AMOUNT DUE'])
            outputlist.append(stored_data)
        # df = df.append(stored_data, ignore_index=True)
        # print(df)
            
            dff = pd.DataFrame(outputlist)
            df= pd.concat([df,dff])
    df.to_excel('scan675.xlsx', index=False)
    print("done")