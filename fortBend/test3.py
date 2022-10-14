"""
a script extracting data from fortbend agency
"""
import re
import pandas as pd
import pdfplumber

stored_data = {'Toll Agency':'Fort Bend County Toll Road Authority',
                'Lp':None,
                'Lp State':None,
                'Trxn date & time':None,
                'Exit lane/Location':None,
                'Account #':None,
                'Reference # or Invoice #':None,
                'Violation #':None,
                'Amount Due':None,
                'Due Date':None,
                'Pin #':None
            }
df = pd.DataFrame()

with pdfplumber.open("./scan_153mt_amazon_fbctra___(7)__august_8_(nko).pdf") as pdf:
    for x, text in enumerate(pdf.pages):
        page = pdf.pages[x]
        page_content = page.extract_text()
        # print(page_content)

        all_table = re.findall(r'S\d*..\W\d*.\w*\W\d*.\w*.\w*.\D*\d.\w*.\D*\d*\W\d*\W\d*\W\d*\W\d*\W\d*\W\d*\s\W\d\W\d*', page_content)
        due_date = re.findall(r'Date\WDue\W\W(\d*\W\d*\W\d*)', page_content)
        print('due date', due_date)
        for i in all_table:
            # print(i)
            license_plate = re.findall(r'S\d*\W*\d*\W\D\w*\W(\d*)\W\w*\W\w*\W*\D*\d*\W\d*\W\d*\W\d*\W\d*\W\d*\W\d*\W\W\d*\W\d*', i)
            state = re.findall(r'S\d*..\W\d*.(.\w*)\W\d*.\w*.\w*.\D*\d.\w*.\D*\d*\W\d*\W\d*\W\d*\W\d*\W\d*\W\d*\s\W\d\W\d*', i)
            trxn_date_time = re.findall(r'S\d*\W\d*.\w*\W\d*.\w*.\w*.\D*\d.\w*.\D*\d*\W(\d*\W\d*\W\d*\W\d*\W\d*\W\d*)\s\W\d\W\d*', i)
            exit_lane = re.findall(r'S\d*\W*\d*\W\D\w*\W\d*\W(\w*\W\w*\W*\D*\d*)\W\d*\W\d*\W\d*\W\d*\W\d*\W\d*\W\W\d*\W\d*', i)
            invoice = re.findall(r'(S\d*..\W\d*).\w*\W\d*.\w*.\w*.\D*\d.\w*.\D*\d*\W\d*\W\d*\W\d*\W\d*\W\d*\W\d*\s\W\d\W\d*', i)
            amount_due = re.findall(r'S\d*\W\d*.\w*\W\d*.\w*.\w*.\D*\d.\w*.\D*\d*\W\d*\W\d*\W\d*\W\d*\W\d*\W\d*\s(\W\d\W\d*)', i)
            
            print('due date', due_date)
            for lp in license_plate:
                print(lp)
                stored_data['Lp'] = lp
            for st in state:
                print(st)
                stored_data['Lp State'] = st
            for trxn in trxn_date_time:
                print(trxn)
                stored_data['Trxn date & time'] = trxn
            for el in exit_lane:
                print(el)
                stored_data['Exit lane/Location'] = el
            for inv in invoice:
                print(inv)
                stored_data['Reference # or Invoice #'] = inv
            for amt in amount_due:
                print(amt)
                stored_data['Amount Due'] = amt
            for dd in due_date:
                print(dd)
                stored_data['Due Date'] = dd

            df = df.append(stored_data, ignore_index=True)
            print(df)
            df.to_excel('fortbend153.xlsx', index=False)
