"""
extracting data from invoice
"""
import re
import pandas as pd
import pdfplumber



with pdfplumber.open('./pdf/scan_45lm_amazon__fdot(11)__september_2_(pm).pdf') as pdf:
    for x, page in enumerate(pdf.pages):
    #for x in range(0, len(pdf.pages)):
        page = pdf.pages[x]
        page_content = page.extract_text()
        # print(page_content)

        pa_lp = re.findall(r'(License Plate\W.\w{2}\W\S*\d{5})',page_content)
        invoice_no_ = re.findall(r'(\wnvoice#\W.\d{9}.*\nINVOICE.SUMMARY)',page_content)
        invoice_no = re.findall(r'\wnvoice#\W.\d{9}.*\d{9}|\wnvoice.#\W.\d{9}.*\d{9}',page_content)
        lane =re.search(r'^\d{2}\W\d{2}\W\d{2}.*\d.\d{2}\W\d{2}\W\d{2}\W\d{2}\W\d{2}\W\d{2}.\wM',page_content)
        
        if pa_lp :
            lp_ = str(pa_lp).split(" ")[2].split("-")[1]
            state_ = str(pa_lp).split(" ")[2].split("-")[0]
        if invoice_no_:
            print(" ")
        elif invoice_no:
            inv_ = str(invoice_no).split("#")[2]
            acc_no = re.findall(r'#\W.(\d{9}).',str(invoice_no))
            acc_ = acc_no[0]
            # print(acc_)
            # print(acc_)
        if lane:
            lane_=lane
            print(lane_)  

#^\d{2}\W\d{2}\W\d{2}.*\d.\d{2}\W\d{2}\W\d{2}\W\d{2}\W\d{2}\W\d{2}.\wM  

