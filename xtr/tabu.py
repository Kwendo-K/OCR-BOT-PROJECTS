'''
python xtra ocr bot
'''
import re
import pandas as pd
import PyPDF2

with open('./SCAN_675_AMAZON_RENTAL_XTRA_TOLLS_SEPTEMBER_26_(SN).pdf', 'rb') as pdf:
    read_pdf = PyPDF2.PdfFileReader(pdf)
    pdf_pages = read_pdf.getNumPages()
    page = read_pdf.pages[0]
    page_data = page.extractText()
    # print(page_data)

    invoice = re.findall(r'^Invoice\s*No\W*(\d*)\nInvoice\s*\Date\s*\d{2}\W*\d{2}\W*\d{4}', page_data)
    print(invoice)