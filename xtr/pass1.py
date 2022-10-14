"""
A python ocr bot extracting data from XTRA agency
"""
from operator import is_
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
curr_lp = ""

with pdfplumber.open('./SCAN_675_AMAZON_RENTAL_XTRA_TOLLS_SEPTEMBER_26_(SN).pdf') as pdf:
    for i, text in enumerate(pdf.pages):
       
        pages = pdf.pages[i]
        page_data = pages.extract_text()
        # print(page_data)
        # print(page_data)

        reference = re.findall(r'(\w{6})\s+\d+\s+\w+\s+\w+\W+\d+\W+\n|Toll\s+\w+\s+\d{2}\/\d{2}\/\d{4}\s+\d{2}\/\d{2}\/\d{4}\D+(\d+\D+\d+)\s+\w+\n(\D+)loc:[\w\d. \n\(\)\/-]*on:\s*(\d{4}\W*\d{2}\W*\d{2}\s*\d{2}\W*\d{2})|Toll\s+\w+\s+\d{2}\/\d{2}\/\d{4}\s+\d{2}\/\d{2}\/\d{4}\D+(\d+\D+\d+)\s+\w+\n(\w+\W+\d+\D+)loc:[\w\d. \n\(\)\/-]*on:\s*(\d{4}\W*\d{2}\W*\d{2}\s*\d{2}\W*\d{2})', page_data)
        invoice = re.findall(r'^Invoice\s*No\W*(\d*)\nInvoice\s*\Date\s*\d{2}\W*\d{2}\W*\d{4}', page_data)
        license_plate = re.findall(r'(\w{6})\s+\d+\s+\w+\s+\w+\W+\d+\W+', page_data)
        amt_ag = re.findall(r'Toll\s+\w+\s+\d{2}\/\d{2}\/\d{4}\s+\d{2}\/\d{2}\/\d{4}\D+(\d+\D+\d+)\s+\w+\n(\D+)loc|Toll\s+\w+\s+\d{2}\/\d{2}\/\d{4}\s+\d{2}\/\d{2}\/\d{4}\D+(\d+\D+\d+)\s+\w+\n(\w+\W+\d+\D+)loc', page_data)
        trxn_date_time = re.findall(r'on:\s*(\d{4}\W*\d{2}\W*\d{2}\s*\d{2}\W*\d{2})', page_data)

        # for amt in amt_ag:
        #     amount = amt[0]
        #     agency = amt[1]
        #     amnt['Amount Due'] = amount
        #     agcy['Toll Agency'] = agency
        # for trxn in trxn_date_time:
        #     trxn_date['Transaction Date & Time'] = trxn
        #     # pass
        for inv in invoice:
            invo['Reference # Invoice #'] = inv
            # print(trxn)
        # for lp in license_plate:
        #     l_p['License Plate'] = lp
        
        i = 0
        while i < len(reference):
            is_lp = True
            amt_index = 0
            for val in reference[i]:
                if "." in val:
                    is_lp = False
                    break
                amt_index += 1
            if is_lp:
                # print("Found LP")
                lp = reference[i][0]
                # print("LP CHANGE")
                curr_lp = lp
                i += 1
                continue
            amt = reference[i][amt_index]
            agency = reference[i][amt_index+1]
            trxn_dt = reference[i][amt_index+2]
            # print('Invoice: ',inv)
            # print('LP: ',lp)
            # print('Trnx DT: ',trxn_dt)
            # print('Amount: ',amt)
            # print('Agency: ',agency)

            stored_data['TOLL AGENCY'] = agency
            stored_data['LP'] = curr_lp
            stored_data['TRXN DATE & TIME'] = str(trxn_dt).replace("\n", "")
            stored_data['EXITLANE/LOCATION'] = ''
            stored_data['REFERENCE # OR INVOICE #'] = inv
            stored_data['AMOUNT DUE'] = amt
            i += 1
            df = pd.concat([df, pd.DataFrame([stored_data])])
        print(df)
df.to_excel('scan675.xlsx', index=False)
            
            
            
            # print(agcy['Toll Agency'], l_p['License Plate'], )
            
            
            # print(stored_data['TOLL AGENCY'], stored_data['REFERENCE # OR INVOICE #'],stored_data['LP'] ,stored_data['AMOUNT DUE'])
    #     df = df.append(stored_data, ignore_index = True)
    #     print(df)
    # df.to_excel('scan675.xlsx', index=False)
            
            # print(amt)
           