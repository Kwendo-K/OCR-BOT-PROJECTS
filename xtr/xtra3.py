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
invo = {'Reference # Invoice #':None}
agcy = {'Toll Agency':None}
l_p = {'License Plate':None}
amnt = {'Amount Due':None}
trxn_date = {'Transaction Date & Time':None}
output_list = []

with pdfplumber.open('./SCAN_675_AMAZON_RENTAL_XTRA_TOLLS_SEPTEMBER_26_(SN).pdf') as pdf:
    for i, text in enumerate(pdf.pages):
       
        pages = pdf.pages[i]
        page_data = pages.extract_text()
        # print(page_data)
        # print(page_data)

        invoice = re.findall(r'^Invoice\s*No\W*(\d*)\nInvoice\s*\Date\s*\d{2}\W*\d{2}\W*\d{4}', page_data)
        license_plate = re.findall(r'(\w{6})\s+\d+\s+\w+\s+\w+\W+\d+\W+', page_data)
        alldata = re.findall(r'Toll Fee\W+\S+\W+\S+\W+(\d+\W+\d+)\W+\w+\n(\S+.*)loc\W+(.*\n.*)on\W+(\S+\W+\d+\W+\d+)|Toll Fee\W+\S+\W+\S+\W+(\d+\W+\d+)\W+\w+\n(.*\n.*)\n\S+\W+(.*)on\W+(\S+\W+\d+\W+\d+)|Toll Fee\W+\S+\W+\S+\W+(\d+\W+\d+)\W+\w+\W+(.*\W+)\S+\W+(.*)on\W+(\S+\W+\d+\W+\d+)|Toll Fee\W+\S+\W+\S+\W+(\d+\W+\d+)\W+\w+\W+(.*)\W+\S+\W+(.*)\W+\S+\W+(\S+\W+\d+\W+\d+)|Toll Fee\W+\S+\W+\S+\W+(\d+\W+\d+)\W+\w+\W+(.*\n.*\n.*)loc\W+(.*\n.*\n.*)on\W+(\S+\W+\d+\W+\d+)', page_data)

        for i_nv in invoice:
            inv = i_nv
        # for l_p in license_plate:
        #     lp = l_p
        for a_l in alldata:
            al = list(a_l)
            
            amount = al[0]
            agency = al[1].upper()
            exit_lane = al[2].upper()
            trxn_date_time = al[3]
            for l_p in license_plate:
                lp = l_p
            # print(inv, lp, amount, agency, exit_lane, trxn_date_time)

            stored_data['TOLL AGENCY'] = agency
            stored_data['LP'] = lp
            stored_data['AMOUNT DUE'] = amount
            stored_data['TRXN DATE & TIME'] = trxn_date_time
            stored_data['EXITLANE/LOCATION'] = exit_lane

            df = df.append(stored_data, ignore_index=True)
        print(df)
df.to_excel('scan675.xlsx', index=False)