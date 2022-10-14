'''
A python script extracting data from CFEA agency
'''

import re
import pandas as pd
import pdfplumber

df = pd.DataFrame()

stored_data = {
    'TOLL AGENCY':'',
    'LP':None,
    'LP STATE':None,
    'TRXN DATE & TIME':None,
    'EXIT LANE/LOCATION':None,
    'ACCOUNT':None,
    'REFERENCE # OR INVOICE #':None,
    'VIOLATION':None,
    'AMOUNT DUE':None,
    'DUE DATE':None,
}

with pdfplumber.open('./scn_176_cfea(pay_by_plate)-amazon_(3)_october_20_(bm).pdf') as pdf:
    for i, text in enumerate(pdf.pages):
        pages = pdf.pages[i]
        page_data = pages.extract_text()
        # print(page_data)

        