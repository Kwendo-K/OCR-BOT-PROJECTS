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
        
#         notice_date = re.findall(r'Notice\W\w*\W(\d{2}\W\d{2}\W\d{4})|Notice\W\w*\W\W\d{2}\W\d{2}\W\d{4}', page_content)
#         date_due = re.findall(r'Due\W\w*\W\W(\d{2}\W\d*\W\d{4})', page_content)
#         notice_number = re.findall(r'\wotice\W\w*\W\W(\w\d{12})', page_content)
#         l_plate = re.findall(r'\wlate\W(\w*\d)', page_content)
#         lp_state = re.findall(r'License\WPlate\WState\W(.\w*)', page_content)
#         total_due = re.findall(r'Total\W\Due\W(\W\d*\W\d*...)', page_content)
        
#         # # all_table variable stores the specific needed data captured from page_content variable
#         all_table = re.findall(r'S\d*..\W\d*.\w*\W\d*.\w*.\w*.\D*\d.\w*.\D*\d*\W\d*\W\d*\W\d*\W\d*\W\d*\W\d*\s\W\d\W\d*', page_content)
#         due_date = re.findall(r'Date\WDue\W\W(\d*\W\d*\W\d*)', page_content)
        
#         if len(all_table) > 0:
#             for i in all_table:
#                 print(i)
#                 license_plate = re.findall(r'S\d*\W*\d*\W\D\w*\W(\d*)\W\w*\W\w*\W*\D*\d*\W\d*\W\d*\W\d*\W\d*\W\d*\W\d*\W\W\d*\W\d*|S\d*..\W\d*.(\w*\W\d*.\w*).\w*.\D*\d.\w*.\D*\d*\W\d*\W\d*\W\d*\W\d*\W\d*\W\d*\s\W\d\W\d*', i)
#                 state = re.findall(r'S\d*..\W\d*.(.\w*)\W\d*.\w*.\w*.\D*\d.\w*.\D*\d*\W\d*\W\d*\W\d*\W\d*\W\d*\W\d*\s\W\d\W\d*', i)
#                 trxn_date_time = re.findall(r'S\d*\W\d*.\w*\W\d*.\w*.\w*.\D*\d.\w*.\D*\d*\W(\d*\W\d*\W\d*\W\d*\W\d*\W\d*)\s\W\d\W\d*', i)
#                 exit_lane = re.findall(r'S\d*\W*\d*\W\D\w*\W\d*\W(\w*\W\w*\W*\D*\d*)\W\d*\W\d*\W\d*\W\d*\W\d*\W\d*\W\W\d*\W\d*|S\d*..\W\d*.\w*\W\d*.\w*.(\w*.\D*\d.\w*.\D*\d*)\W\d*\W\d*\W\d*\W\d*\W\d*\W\d*\s\W\d\W\d*', i)
#                 invoice = re.findall(r'(S\d*..\W\d*).\w*\W\d*.\w*.\w*.\D*\d.\w*.\D*\d*\W\d*\W\d*\W\d*\W\d*\W\d*\W\d*\s\W\d\W\d*', i)
#                 amount_due = re.findall(r'S\d*\W\d*.\w*\W\d*.\w*.\w*.\D*\d.\w*.\D*\d*\W\d*\W\d*\W\d*\W\d*\W\d*\W\d*\s(\W\d\W\d*)', i)
                
                
#                 print('due date', due_date)
#                 for lp in license_plate:
#                     # print(lp)
#                     stored_data['Lp'] = lp
#                 for st in state:
#                     # print(st)
#                     stored_data['Lp State'] = st
#                 for trxn in trxn_date_time:
#                     # print(trxn)
#                     stored_data['Trxn date & time'] = trxn
#                 for el in exit_lane:
#                     # print(el)
#                     stored_data['Exit lane/Location'] = el
#                 for inv in invoice:
#                     # print(inv)
#                     stored_data['Reference # or Invoice #'] = inv
#                 for amt in amount_due:
#                     # print(amt)
#                     stored_data['Amount Due'] = amt
#                 for dd in due_date:
#                     print(dd)
#                     stored_data['Due Date'] = dd

#                 df = df.append(stored_data, ignore_index=True)
#                 df.drop_duplicates(inplace = True)
#                 print(df.duplicated())
#                 # df.to_excel('fortbend281.xlsx', index=False)
#         else:
#             #This else statement executes when no table is found on a page
#             notice_date = re.findall(r'Notice\W\w*\W(\d{2}\W\d{2}\W\d{4})|Notice\W\w*\W\W\d{2}\W\d{2}\W\d{4}', page_content)
#             date_due = re.findall(r'Due\W\w*\W\W(\d{2}\W\d*\W\d{4})', page_content)
#             notice_number = re.findall(r'\wotice\W\w*\W\W(\w\d{12})', page_content)
#             l_plate = re.findall(r'\wlate\W(\w*\d)', page_content)
#             lp_state = re.findall(r'License\WPlate\WState\W(.\w*)', page_content)
#             total_due = re.findall(r'Total\W\Due\W(\W\d*\W\d*...)', page_content)

#             for n_d in notice_date:
#                 print(n_d)
#                 stored_data['Notice Date'] = n_d
#             for d_due in date_due:
#                 print(d_due)
#                 stored_data['Due Date'] = d_due
#             for n_m in notice_number:
#                 print(n_m)
#                 stored_data['Notice #'] = n_m
#             for l_p in l_plate:
#                 print(l_p)
#                 stored_data['Lp'] = l_p
#             for l_s in lp_state:
#                 print(l_s)
#                 stored_data['Lp State'] = l_s
#             for t_d in total_due:
#                 print(t_d)
#                 stored_data['Total Amount Due'] = t_d 
#             df = df.append(stored_data, ignore_index=True)
#             df.drop_duplicates(inplace = True)
#             print(df.duplicated())
# df.to_excel('fortbend281.xlsx', index=False)
