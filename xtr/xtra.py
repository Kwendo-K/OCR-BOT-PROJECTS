"""
A python ocr bot extracting data from XTRA agency
"""
import re
import pandas as pd
import pdfplumber



stored_data = {
    'TOLL AGENCY':None,
    'LP':None,
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

with pdfplumber.open('./SCAN_676_AMAZON_RENTAL_XTRA_TOLLS_SEPTEMBER_26_(SN).pdf') as pdf:
    output_list = []
    for i, text in enumerate(pdf.pages):
        df = pd.DataFrame()
        pages = pdf.pages[i]
        page_data = pages.extract_text()
        # print(page_data)

        invoice = re.findall(r'Invoice No\D+(\w{8})\n', page_data)
        license_plate = re.findall(r'(\w{6})\W+\w{9}\s+\S+\s+\S+\D+\w+\W+\w{3}\n', page_data)
        all_info = re.findall(r'\woll Fee\D+\S+\W+\S+\D+(\d+\D+\d+)\W+\w+\n(\D+)loc:\W+(\D+|\S+)on\W+(\d+\D+\d+\D+\d+\W+\d{2}\D+\d{2})|\woll Fee\W+\S+\W+\S+\D+(\d+\D+\d+)\W+\w+\n(\D+)loc\W+(\S+\s+\S+)\W+(\d+\D+\d+\D+\d+\s+\d{2}\D+\d{2})|\wToll Fee\D+\S+\W+\S+\D+(\d+\D+\d+)\W+(\D+)loc\W+(\S+\W+\D+)\d+\W+\S+\W+(\d+\D+\d+\D+\d+\W+\d+\D+\d{2})|\woll Fee\W+\S+\W+\S+\D+(\d+\D+\d+)\W+\w+\s+(\S+\W+\S+)\W+\S+\W+(\S+\W+\S+\W+\S+)\s+\S+\W+(\S+\W+\d{2}\D+\d{2})|\woll Fee\W+\S+\W+\S+\D+(\d+\D+\d+)\W+\w+\s+(\D+)loc\W+(\S+\W+\S+)\D+(\d+\D+\d{2}\D+\d{2}\W+\d{2}\W+\d{2})|\woll Fee\W+\S+\W+\S+\D+(\d+\D+\d+)\W+\w+\s+(\D+)loc\W+(\S+\W+\S+\D+\d+\W+\S+\W+\S+\W+\S+)\W+\S+\W+(\S+\W+\d{2}\D+\d{2})', page_data)
        for l_p in license_plate:
            lp = l_p
        for i_nv in invoice:
            inv = i_nv
        for a_l in all_info:
            al = a_l
            amt = al[0]
            print(inv,amt, pages)