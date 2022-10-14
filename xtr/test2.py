'''
python script
'''
import re
import PyPDF2
import pandas as pd

df = pd.DataFrame()

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

pdf_File_Object = open('./SCAN_675_AMAZON_RENTAL_XTRA_TOLLS_SEPTEMBER_26_(SN).pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdf_File_Object)
print(pdfReader.numPages)

for page in range(pdfReader.numPages):
    pages = pdfReader.getPage(page)
    pageData = pages.extract_text()

    invoice = re.findall(r'^Invoice\s*No\W*(\d*)\nInvoice\s*\Date\s*\d{2}\W*\d{2}\W*\d{4}', pageData)
    license_plate = re.findall(r'(\w{6})\s*\d{9}\s*\w*\s*\w*\W*\d*', pageData)
    amt_agency_ext = re.findall(r'Toll\s*\w*\s*\d{2}\W*\d{2}\W*\d{4}\s*\d{2}\W*\d{2}\W*\d{4}\W*(\d*\W*\d*)\W*\w*\n(\w*\W*\w*\W*\w*\W*\w*\W*\w*\s*\D*)loc:\s*(\D*\d*)', pageData)
    trxn_date_time = re.findall(r'on:\s*(\d{4}\W*\d{2}\W*\d{2}\s*\d{2}\W*\d{2})', pageData)
    
    for al in amt_agency_ext:
        print(al)