import re
import pandas as pd
import pdfplumber


df = pd.DataFrame()
final_dict = { "TOLL AGENCY":None, "LP":None,"LP STATE":None,"EXIT LANE/LOCATION":None,"ACCOUNT #":None,"REFERENCE # OR INVOICE #":None,"VIOLATION":None,"AMOUNT":None,"DATE & TIME":None,"PIN NO":None}
lane = ""

with pdfplumber.open("./amazonPdf/scan_147mt_amazon_fbctra___(7)__august_8_(nko).pdf") as pdf:
    for x, page in enumerate(pdf.pages):
    #for x in range(0, len(pdf.pages)):
        page = pdf.pages[x]
        page_content = page.extract_text()
        print(page_content)

        pa_lp = re.findall(r"License Plate\W.\w{2}\W\S*\d{5}",page_content)
        invoice_no_ = re.findall(r"(\wnvoice#\W.\d{9}.*\nINVOICE.SUMMARY)",page_content)
        invoice_no = re.findall(r"\wnvoice#\W.\d{9}.*\d{9}|\wnvoice.#\W.\d{9}.*\d{9}",page_content)
        lane =re.search(r"^\d{2}\W\d{2}\W\d{2}(.*)\d.(\d{2}\W\d{2}\W\d{2}\W\d{2}\W\d{2}\W\d{2}.\wM)",page_content,re.M)        
        

#         if lane:
#             exit=lane.group(1)
#             final_dict["EXIT LANE/LOCATION"] = exit
#             date_=lane.group(2)
#             print(date_)
#             final_dict["DATE & TIME"] = date_
        
#             # lane_ = str(lane).strip()
#             # final_dict["location"]=lane_
        
#         if pa_lp :
#             lp_ = pa_lp[0][18:25]  
#             final_dict["LP"]=lp_   
#             lp_= " "
#             state_ = str(pa_lp).split(" ")[2].split("-")[0]  
#             final_dict["LP STATE"] = state_
#         if invoice_no_:
#             print(' ')
#         elif invoice_no:
#             inv_ = invoice_no[0][29:]
#             final_dict["ACCOUNT #"] = inv_
            
#             acc_no = re.findall(r"#\W.(\d{9}).",str(invoice_no))            
#             acc_ = acc_no[0]
#             final_dict["REFERENCE # OR INVOICE #"] = acc_
            
#             df = df.append(final_dict, ignore_index=True)     
# df.to_excel('fdot1_828output.xlsx', index= False)

