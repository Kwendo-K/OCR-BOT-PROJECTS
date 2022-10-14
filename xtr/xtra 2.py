"""
A python ocr bot extracting data from XTRA agency
"""
from ast import And
import re
import pandas as pd
import pdfplumber

import pandas as pd
df = pd.DataFrame()

stored_data = {
    'TOLL AGENCY':None,
    'LP':None,
    'STATE':None,
    'TRXN DATE & TIME':None,
    'EXITLANE/LOCATION':None,
    'ACCOUNT #':None,
    'REFERENCE # OR INVOICE #':None,
    'VIOLATION':None,
    'AMOUNT DUE':None,
    'DUE DATE':None,
    'PIN #':None
}


# output_list = []
pdf = pdfplumber.open('./SCAN_675_AMAZON_RENTAL_XTRA_TOLLS_SEPTEMBER_26_(SN).pdf')



for i, text in enumerate(pdf.pages):

    pages = pdf.pages[i]
    page_data = pages.extract_text()
    

    row_dict = {"Invoice Number": "", "Page": "", "LP": "",
                    "State": "", "Exit Date Time": "", "Loc": "", "Amount": ""}
        # print(page_data)

    invoice = re.findall(r'^Invoice\s*No\W*(\d*)\nInvoice\s*\Date\s*\d{2}\W*\d{2}\W*\d{4}', page_data)
    license_plate = re.findall(r'(\w{6})\s+\d+\s+\w+\s+\w+\W+\d+\W+', page_data)
    agency_exit_time = re.findall(r'Toll\s*\w*\s*\d{2}\W*\d{2}\W*\d{4}\s*\d{2}\W*\d{2}\W*\d{4}\W*(\d*\W*\d*)\W*\w*\n(\w*\W*\w*\W*\w*\W*\w*\W*\w*\s*\D*)loc(\D*)(\d*\D*\d*\D*\d*\D*\d*\D*\d*)', page_data)
    amount_due = re.findall(r'Toll\s*\w*\s*\d{2}\W*\d{2}\W*\d{4}\s*\d{2}\W*\d{2}\W*\d{4}\W*(\d*\W*\d*)', page_data)
    trxn_date_time = re.findall(r'\wn\W*(\d{4}\W*\d{2}\W*\d{2}\W*\d{2}\W*\d{2})', page_data)
    grabUnitRgx = re.compile(r'^(\w{6})\s+\d+\s+\w+\s+\w+\W+\d+\W+')
    grabTollFee = re.compile(r'^Toll Fee')

    print(trxn_date_time)
    lpNameArry =[]
    for i_nv in invoice:
        inv = i_nv
    # for l_p in license_plate:
    #     lp = l_p
    #     for a_mt in amount_due:
    #         amt = a_mt
    #         print(lp,amt)
    lpcount  =0
    nameCount  = 0
    prevLp = ''
    for line in page_data.split("\n"):

        lp = re.match(grabUnitRgx, line)
        name  =  re.findall(grabTollFee,line)
    
        if lp  and nameCount>0 :
            lpNameArry.append([prevLp,nameCount])
            nameCount =0
            prevLp = lp.group(1)
        elif lp:
            prevLp = lp.group(1)
    
        if name:
            nameCount =  nameCount+1
         
        
    lpNameArry.append([prevLp,nameCount])
    prevIndex = 0
  
    print(len(amount_due))
    print(len(agency_exit_time))
    print(len(trxn_date_time))
    for val in lpNameArry:
        
    
        for amt in range(prevIndex,prevIndex+ val[1]) :
            output_list = []
            
            stored_data["TOLL AGENCY"] = str(agency_exit_time[amt]).split(',')[1]
            stored_data["LP"] = val[0]
            stored_data["STATE"] = str(agency_exit_time[amt]).split(',')[2]
            stored_data["TRXN DATE & TIME"] = trxn_date_time[amt]
            stored_data["EXITLANE/LOCATION"] = trxn_date_time[amt]
            stored_data['REFERENCE # OR INVOICE #'] = inv
            stored_data['AMOUNT DUE'] = amount_due[amt]
            # print(val[0])
            # row_dict["Amount"] = amount_due[amt]
            # row_dict["LP"] = val[0]
            # row_dict["Exit Date Time"] = trxn_date_time[amt]
            # row_dict["Agency"] = str(agency_exit_time[amt]).split(',')[1]
            # row_dict["Loc"] = str(agency_exit_time[amt]).split(',')[3]
            # row_dict["State"] = str(agency_exit_time[amt]).split(',')[2]
            # row_dict["Page"] = i+1
            # output_list.append(row_dict)
            output_list.append(stored_data)
            dff = pd.DataFrame(output_list)
            df = pd.concat([df, dff])
   

        prevIndex = prevIndex+ val[1]
        print(df)
      

    # # print(lpNameArry)
    # if i>10:

print("writing out")
df.to_excel("out675.xlsx", index=False)