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
                'Notice Date':None,
                'Notice #':None,
                'Total Amount Due':None
            }
df = pd.DataFrame()
#importing the pdf to extract data from
with pdfplumber.open("./scan_281lm_amazon_fbctra_(9)__september_19_(ag).pdf") as pdf:
    for x, text in enumerate(pdf.pages):
        page = pdf.pages[x]
        page_content = page.extract_text()
        # print(page_content)
        
        # # all_table variable stores the specific needed data captured from page_content variable
        all_table = re.findall(r'(\w{13}-\w{5})\W*(\w{2})\W*(\d*)\W*(\w*\s\w*\s*\D*\d*)\W*(\d*\D*\d*\D*\d*\D*\d*\D*\d*\D*\d*)\W*(\W*\d*\W*\d*)|S\d*..\W\d*.\w*\W\d*.\w*.\w*.\D*\d.\w*.\D*\d*\W\d*\W\d*\W\d*\W\d*\W\d*\W\d*\s\W\d\W\d*', page_content)
        due_date = re.findall(r'Date\WDue\W\W(\d*\W\d*\W\d*)', page_content)
        for al in all_table:
            print(al)
        
        if len(all_table) > 0:
            for al in all_table:
                # print(al)
                invoice = al[0]
                license_state = al[1]
                license_plate = al[2]
                exit_lane = al[3]
                trxn_date_time = al[4]
                amount_due = al[5]

                stored_data['Reference # or Invoice #'] = invoice
                stored_data['Lp State'] = license_state
                stored_data['Lp'] = license_plate
                stored_data['Exit lane/Location'] = exit_lane
                stored_data['Trxn date & time'] = trxn_date_time
                stored_data['Amount Due'] = amount_due
                # print(invoice)
                # print(license_state)
                # print(license_plate)
                # print(exit_lane)
                # print(trxn_date_time)
                # print(amount_due)
            df = df.append(stored_data, ignore_index=True)
            print(df) 
            df.to_excel('fortbend281.xlsx', index=False)
            print('Data appended to excel...')
        elif len(all_table) <= 0:
            # for mi in page_content:
            notice_date = re.findall(r'Notice\W\w*\W(\d{2}\W\d{2}\W\d{4})|Notice\W\w*\W\W\d{2}\W\d{2}\W\d{4}', page_content)
            date_due = re.findall(r'Due\W\w*\W\W(\d{2}\W\d*\W\d{4})', page_content)
            notice_number = re.findall(r'\wotice\W\w*\W\W(\w\d{12})', page_content)
            l_plate = re.findall(r'\wlate\W(\w*\d)', page_content)
            lp_state = re.findall(r'License\WPlate\WState\W(.\w*)', page_content)
            total_due = re.findall(r'Total\W\Due\W(\W\d*\W\d*...)', page_content)

            stored_data['Notice Date'] = notice_date
            stored_data['Due Date'] = date_due
            stored_data['Notice #'] = notice_number
            stored_data['Lp'] = l_plate
            stored_data['Lp State'] = lp_state
            stored_data['Total Amount Due'] = total_due
            df = df.append(stored_data, ignore_index=True)
            print(df)
            df.drop_duplicates(inplace = True)
            df.to_excel('fortbend281.xlsx', index=False)
            print('Data appended to excel...')
        else:
            print("No data found!")
        #             df = df.append(stored_data, ignore_index=True)
        #             df.drop_duplicates(inplace = True)
        #             print(df.duplicated())
        #             # print(df)
        #     df.to_excel('fortbend109.xlsx', index=False)
