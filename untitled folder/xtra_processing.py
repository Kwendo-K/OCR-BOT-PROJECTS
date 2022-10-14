import pdfplumber
import pandas as pd
import os, re, time

def get_details(row):
    def break_down_details(details):
        op = {"agency":None,"location":None,"exit_dt":None}
        op['agency'] = str(re.findall('(?<=Toll Fee).+(?=,)', details)[0]).strip()
        op['location'] = str(re.findall('(?<=loc:).+(?=on:)', details)[0]).strip()
        op['exit_dt'] = str(re.findall('(?<=on:).+', details)[0]).replace(" ", "")

        return op
        
    state = row[-1:][0]
    amount = str(row[-2:-1][0]).replace("$", " ").strip()
    details = str(row[-5:-4][0]).replace("\n", " ")
    ret_details = break_down_details(details)
    agency, location, exit_dt = ret_details['agency'], ret_details['location'], ret_details['exit_dt']
    exit_dt = exit_dt[:10] + " " + exit_dt[10:]
    return [state, agency, location, exit_dt, amount]

def get_toll_transactions(page):
    page_tolls = []
    table = page.extract_table()
    invoice = page.extract_words()[2]['text']
    lp = None
    aggrement = None

    for row in table:
      # try:
      
        if row[0] == None:
            record = [lp]+get_details(row)+[aggrement, invoice]
            page_tolls.append(record)
        elif "Unit" in row[0]:
            pass
        else:
            lp = re.findall('\S+', row[0])[0]
            aggrement = re.findall('\S+', row[0])[1]
            if row[5] != None:
                record = [lp]+get_details(row)+[aggrement, invoice]
                page_tolls.append(record)
    
    return page_tolls

start = time.time()  
processed = 0
#for filename in os.listdir('../raw_files/xtra_lease'):
# for filename in os.listdir('raw_files/xtra_lease'):

#     if filename.endswith('.pdf'):
#         justname = filename.split(".")[0]
#         if os.path.exists("../output_files/"+justname+".csv"):
#             print(f'Skipped {filename} :Previously done')
#             continue
#         else:
#             processed += 1
#             headers_full = ['unit', 'state', 'agency', 'location', 'date time', 'amount', 'reference', 'invoice', 'page']
#             headers = ['unit', 'state', 'agency', 'location', 'date time', 'amount', 'reference', 'invoice']
#             with pdfplumber.open(os.path.join("../raw_files/xtra_lease/", filename)) as pdf:
#                 tot_pages = len(pdf.pages)
#                 print(f'Now on {processed}. {filename} with {tot_pages} pages')
#                 tolls = pd.DataFrame(columns=headers_full)
processed += 1
headers_full = ['unit', 'state', 'agency', 'location', 'date time', 'amount', 'reference', 'invoice', 'page']
headers = ['unit', 'state', 'agency', 'location', 'date time', 'amount', 'reference', 'invoice']
justname = "name"
with pdfplumber.open("./SCAN_675_AMAZON_RENTAL_XTRA_TOLLS_SEPTEMBER_26_(SN).pdf") as pdf:
    tolls = pd.DataFrame(columns=headers_full)
    for i in list(range(len(pdf.pages))):
        page = pdf.pages[i]
        try:
             df = pd.DataFrame(get_toll_transactions(page), columns=headers)
        #df = pd.DataFrame(get_toll_transactions(page))
        except TypeError:
            pass
        # df['page']= i+1
        tolls = tolls.append(df)
        #justname = filename.split(".")[0]
        print(tolls)
        #tolls.to_csv()


    stop = time.time()
    print(f'DONE PROCESSING {processed} Files IN {stop-start}')
    tolls.to_csv(os.path.join("./output_files/", f'{justname}.csv'), index=False)
