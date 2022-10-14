import re
import pandas as pd
import pdfplumber

df = pd.DataFrame()
lp_= ""
final_dict = {"TOLL AGENCY":None,"LP":None,"LP STATE":None,"EXIT LANE/LOCATION":None,"ACCOUNT#":None,"REFERENCE # OR INVOICE#":None,"VIOLATION":None,"AMOUNT":None,"DUE DATE":None,"PIN NO":None}

with pdfplumber.open("./pdf/scan_45lm_amazon__fdot(11)__september_2_(pm).pdf") as pdf:
    for x, page in enumerate(pdf.pages):
    #for x in range(0, len(pdf.pages)):
        page = pdf.pages[x]
        page_content = page.extract_text()
        # print(page_content)

        pa_lp = re.findall(r"License Plate\W.\w{2}\W\S*\d{5}",page_content)
        invoice_no_ = re.findall(r"(\wnvoice#\W.\d{9}.*\nINVOICE.SUMMARY)",page_content)
        invoice_no = re.findall(r"\wnvoice#\W.\d{9}.*\d{9}|\wnvoice.#\W.\d{9}.*\d{9}",page_content)
        lane =re.search(r"^\d{2}\W\d{2}\W\d{2}(.*)\d.\d{2}\W\d{2}\W\d{2}\W\d{2}\W\d{2}\W\d{2}.\wM",page_content,re.M)        
        

        if lane:
            lane_ = str(lane)
            final_dict["EXIT LANE/LOCATION"] = lane_
            # print(lane_)
        if pa_lp :
            lp_ = pa_lp[0][18:25]
            final_dict["LP"] = lp_
            
            state_ = str(pa_lp).split(' ')[2].split('-')[0]
            final_dict["LP STATE"] = state_
                
        if invoice_no_:
            print(' ')
        elif invoice_no:
            inv_ = invoice_no[0][29:]
            
            final_dict["ACCOUNT#"] = inv_ 
            acc_no = re.findall(r"#\W.(\d{9}).",str(invoice_no))            
            acc_ = acc_no[0]
            # final_dict["REFERENCE # OR INVOICE #"] = acc_
              
            

            # print(acc_)
        df = df.append(final_dict, ignore_index=True)
df.to_excel('fdot2_828output.xlsx', index= False)        
        