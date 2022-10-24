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

with pdfplumber.open('./SCAN_675_AMAZON_RENTAL_XTRA_TOLLS_SEPTEMBER_26_(SN).pdf') as pdf:
    for i, text in enumerate(pdf.pages):
       
        pages = pdf.pages[i]
        page_data = pages.extract_text()
        # print(page_data)
        # print(page_data)

        invoice = re.findall(r'^Invoice\s*No\W*(\d*)\nInvoice\s*\Date\s*\d{2}\W*\d{2}\W*\d{4}', page_data)
        license_plate = re.findall(r'(\w{6})\s+\d+\s+\w+\s+\w+\W+\d+\W+', page_data)
        alldata = re.findall(r'Toll\s+\w+\s+\d{2}\/\d{2}\/\d{4}\s+\d{2}\/\d{2}\/\d{4}\D+(\d+\D+\d+)\s+\w+\n(\D+)loc:\W+(\D+)on:\W+(\d{4}\W*\d{2}\W*\d{2}\s*\d{2}\W*\d{2})|Toll\s+\w+\s+\d{2}\/\d{2}\/\d{4}\s+\d{2}\/\d{2}\/\d{4}\D+(\d+\D+\d+)\W+\w+\W+(.*)loc:\W+(\S+\W+\S+\W+\S+\W+)\S+\W+(\S+\W+\d+\W+\d+)|Toll Fee\W+\S+\W+\S+\W+(\d+\D+\d+)\W+(.*\W+.*)loc:\W+(.*)on:\W+(\S+\W+\d+\W+\d+\W+\d+)|Toll Fee\W+\S+\W+\S+\W+(\d+\D+\d+)\W+(.*\W+.*)loc:\W+(.*\W+.*)on:\W+(\S+\W+\d+\W+\d+)|Toll Fee\W+\S+\W+\S+\W+(\d+\D+\d+)\W+(.*\W+.*\W+.*)loc:\W+(.*\W+.*\W+.*)on:\W+(\S+\W+\d+\W+\d+)|Toll Fee\W+\S+\W+\S+\W+(\d+\D+\d+)\W+\w+\W+(.*\W+.*\W+.*)loc:\W+(.*\W+.*)on:\W+(\S+\W+\d+\W+\d+)', page_data)

        
        # for l_p in license_plate:
        #     lp = l_p
        for i_nv in invoice:
            inv = i_nv
        for a_l in alldata:
            al = list(filter(None, a_l))
            # print(al)

            amount = al[0]
            agency = al[1]
            exit_lane = al[2]
            trxn_date_time = al[3]

            for l_p in license_plate:
                lp = l_p
            
            stored_data['REFERENCE # OR INVOICE #'] = inv
            stored_data['TOLL AGENCY'] = agency
            stored_data['LP'] = lp
            stored_data['AMOUNT DUE'] = amount
            stored_data['EXITLANE/LOCATION'] = exit_lane
            stored_data['TRXN DATE & TIME'] = trxn_date_time

            df = df.append(stored_data, ignore_index=True)
        print(df)
df.to_excel('scan675.xlsx', index=False)