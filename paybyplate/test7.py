'''
ocr bot extracting data from pay by plate agencny
'''
import re
import pandas as pd
import pdfplumber

#creating a dictionary to append data extracted from the pdf
stored_data = {
    'Toll Agency':'PAY BY PLATE MA',
    'license plate':None,
    'State':None,
    'Transaction date & time':None,
    'Exit Lane':None,
    'Account':None,
    'Invoice # Ref #':None,
    'Amount due':None,
    'Due Date':None,
}

df = pd.DataFrame()

#opening the pdf to extract data from
with pdfplumber.open('./angie/scan_2mt_amazon_pay_by_plate_ma_(23)_oct_3_(nko).pdf') as pdf:
    #creating a loop to loop through the entire pdf opened
    for x, text in enumerate(pdf.pages):
        print(f"Page {x}")
        page = pdf.pages[x]
        page_data = page.extract_text()
        # print(page_data)

        # all_data = re.findall(r'(\wR|\wN)\D*(\w{7}|...\w{5})\D*(\d*\/\d*\/\d{4}\D*\d*\:\d*\:\d*).(\D*.)\d.(\D*\d*\D*\d*\n)', page_data)
        all_data = re.findall(r'(\wR|\wN)\D*(\w{7}|...\w{5})\D*(\d*\/\d*\/\d{4}\D*\d*\:\d*\:\d*).(\D*.)\d.\D*(\d*\D*\d*\n)', page_data)
        invoice_number = re.findall(r'\woice\WNumber\W*(\d*)', page_data)
        prev_balance = re.findall(r'\$(\d*\W*\d*)\s*\$(\d*\W*\d*)\s*\$(\d*\W*\d*)\s*\$(\d*\W*\d*)\s*\$(\d*\W*\d*)\s*(\d{2}\W*\d*\W*\d*)', page_data)
        non_ma_fee = re.findall(r'Non\s+MA\s+Fee\s+\d{2}\W+\d{2}\W+\d{4}\s+\d{2}\W+\d{2}\W+\d+\s+\W+(\d+\W+\d+)', page_data)
        invoice_fee = re.findall(r'Invoice\W*Fee\W*\d{2}\W*\d{2}\W*\d{4}\W*\d{2}\W*\d{2}\W*\d{2}\W*(\d\W*\d*)', page_data)

        extra_fee = 0
        for n_fee in non_ma_fee:
            print(n_fee)
            if "." in n_fee:
                extra_fee += float(n_fee)

        print(all_data)
        # for inv in invoice_number:
        for inv in invoice_number:
            pass
        for prev_bal in prev_balance:
            prev_b = prev_bal[0]
        for fee in invoice_fee:
            print(fee)
        if len(prev_balance) > 0:
            stored_data['State'] = ""
            stored_data['license plate'] = ""
            stored_data['Transaction date & time'] = ""
            stored_data['Exit Lane'] = ""
            stored_data['Invoice # Ref #'] = ""
            stored_data['Amount due'] = prev_b
            df = df.append(stored_data, ignore_index = True)
        
        final_trans_index = len(all_data) - 1
        trans_index = 0
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
            final_amt_due = float(amt_due) if trans_index != final_trans_index else float(amt_due) + float(fee) + extra_fee
            stored_data['Amount due'] = final_amt_due
            # stored_data['Previous Balance'] = prev_bal[0]

            # df = df.astype({'Amount due':'float64'})
            df = pd.concat([df, pd.DataFrame([stored_data])])
            df.drop_duplicates(inplace = True)
            trans_index += 1
        print(df)
df.to_excel('paybyplate23.xlsx', index=False)
