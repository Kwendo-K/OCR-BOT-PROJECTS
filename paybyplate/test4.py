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
        
        for i in page_data:
            stored_data['license plate'] = i
            stored_data['Transaction date & time'] = i
            stored_data['State'] = i
            stored_data['Invoice #'] = i
            stored_data['Amount due'] = i
            stored_data['Exit Lane'] = i
        df = df.append(stored_data, ignore_index = True)
        df.drop_duplicates(inplace = True)
        print(df)
    df.to_excel('paybyplate.xlsx', index=False)