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
                'Notice #':None,
                'Total Amount Due':None
            }
df = pd.DataFrame()
#importing the pdf to extract data from
with pdfplumber.open("./scn_109_(p2)_fort_bend_county_-amazon_(6)_july_2_(bm).pdf") as pdf:
    for x, text in enumerate(pdf.pages):
        page = pdf.pages[x]
        page_content = page.extract_text()
        # print(page_content)
        
        notice_date = re.findall(r'Notice\W\w*\W(\d{2}\W\d{2}\W\d{4})|Notice\W\w*\W\W\d{2}\W\d{2}\W\d{4}', page_content)
        date_due = re.findall(r'Due\W\w*\W\W(\d{2}\W\d*\W\d{4})', page_content)
        notice_number = re.findall(r'\wotice\W\w*\W\W(\w\d{12})', page_content)
        l_plate = re.findall(r'\wlate\W(\w*\d)', page_content)
        lp_state = re.findall(r'License\WPlate\WState\W(.\w*)', page_content)
        total_due = re.findall(r'Total\W\Due\W(\W\d*\W\d*...)', page_content)
        
        # # all_table variable stores the specific needed data captured from page_content variable
        all_table = re.findall(r'(.*[-]\d{5})\D+\w+\W+(\w{7})\W+(\w{2})\W+(\w+\W+\D+\w+)\W+(\S+\W+\d+\D+\d+\D+\d+)\W+(\d+\D+\d+)|(\w{13}\D+\d{5})\D+\w+\W+(\w{7})\W+(\w{2})\W+(\S+\D+\d+)\D+(\S+\W+\d+\D+\d+\D+\d+)\W+(\d+\D+\d+)', page_content)
        due_date = re.findall(r'Date\WDue\W\W(\d*\W\d*\W\d*)', page_content)
        
        if len(all_table) >= 1:
            for a_l in all_table:
                al = list(filter(None, a_l))
                # print(al)
                violation = al[0]
                lp = al[1]
                state = al[2]
                exit_lane = al[3]
                trxn_date = al[4]
                amount = al[5]
                # print(amount)
                
                stored_data['Lp'] = lp
                stored_data['Lp State'] = state
                stored_data['Exit lane/Location'] = exit_lane
                stored_data['Violation #'] = violation
                stored_data['Trxn date & time'] = trxn_date
                stored_data['Amount Due'] = amount

                df = df.append(stored_data, ignore_index=True)
                df.drop_duplicates(inplace = True)
                print(df)
        if len(all_table) <= 0:
            #This else statement executes when no table is found on a page
            date_due = re.findall(r'Date Due\W+(\d+\D+\d+\D+\d+)', page_content)
            violation = re.findall(r'Notice Number\W+(\w{13})', page_content)
            l_plate = re.findall(r'License Plate\W+(\w{7})', page_content)
            lp_state = re.findall(r'License Plate State\W+(\w{2})', page_content)
            total_due = re.findall(r'Total Due\W+(\d+\D+\d+)', page_content)

            for d_due in date_due:
                print(d_due)
                stored_data['Trxn date & time'] = d_due
            for n_m in notice_number:
                print(n_m)
                stored_data['Violation #'] = n_m
            for l_p in l_plate:
                print(l_p)
                stored_data['Lp'] = l_p
            for l_s in lp_state:
                print(l_s)
                stored_data['Lp State'] = l_s
            for t_d in total_due:
                print(t_d)
                stored_data['Amount Due'] = t_d
                # stored_data['Trxn date & time'] = ''
            df = df.append(stored_data, ignore_index=True)
            df.drop_duplicates(inplace = True)
            print(df)
df.to_excel('fortbend109.xlsx', index=False)
