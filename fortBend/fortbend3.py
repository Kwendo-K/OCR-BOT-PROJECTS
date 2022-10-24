"""
a script extracting data from fortbend agency
"""
import re
import pandas as pd
import pdfplumber
#creating a dictionary to append the extracted data
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
                'Pin #':None,
                # 'Notice Date':None,
                # 'Notice #':None,
                'Total Amount Due':None
            }
df = pd.DataFrame()
#importing the pdf to extract data from
with pdfplumber.open("./scan_281lm_amazon_fbctra_(9)__september_19_(ag).pdf") as pdf:
    for x, text in enumerate(pdf.pages):
        page = pdf.pages[x]
        page_content = page.extract_text()
        # print(page_content)
        
        # all_table variable stores the specific needed data captured from page_content variable
        all_table = re.findall(r'(\w{13}\D*\w{5})\s*(\w{2})\-(\w{6}.)\s*(\w*\W*\w*\W*\D*\d*)\W*(\d*\W*\d*\W*\d*\W*\d*\W*\d*\W*\d*)\s*(\W*\d*\W*\d*)', page_content)
        date_due = re.findall(r'Date Due\W+(\d*\W+\d*\W+\d*)', page_content)
        notice_no = re.findall(r'Notice Number\W+(\w{13})', page_content)
        license_plate = re.findall(r'License Plate\W+(\w{7})', page_content)
        all_table = re.findall(r'(\w{13}\W+\w{5})\W+(\w{2})\W+(\S+)\W+(\S+\D+\d+)\W+(\S+\W+\S+)\W+(\d+\W+\d+)', page_content)

        for dd in date_due:
            print('Missing table', page)
            stored_data['Due Date'] = dd
        #checking if table exists in a page
        if all_table:
            for a_l in all_table:
                al = list(filter(None, a_l))
                # print(a_l)
                violation = al[0]
                state = al[1]
                lp = al[2]
                exit_lane = al[3]
                trxn_date = al[4]
                amount = al[5]
                #storing the data in the dictionary
                stored_data['Lp'] = lp
                stored_data['Lp State'] = state
                stored_data['Trxn date & time'] = trxn_date
                stored_data['Exit lane/Location'] = exit_lane
                stored_data['Amount Due'] = amount
                stored_data['Violation #'] = violation
                

                df = df.append(stored_data, ignore_index=True)
                # print(df)
        elif not all_table:
        # elif len(all_table) <= 0:
            # for dd in date_due:
            #     print('Missing table', page)
            #     stored_data['Due Date'] = dd
            # print('Missing table')
            for nn in notice_no:
                print('Missing table', page)
                stored_data['Violation #'] = nn
            for lp in license_plate:
                print('Missing table')
                print(lp)
                stored_data['Lp'] = lp
                stored_data['Trxn date & time'] = ''
                stored_data['Exit lane/Location'] = ''
                df = df.append(stored_data, ignore_index=True)
        print(df)
df.to_excel('Fbctra281.xlsx', index=False)
