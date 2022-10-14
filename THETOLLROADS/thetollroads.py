import pandas as pd
import pdfplumber
import re as reg_ex
df = pd.DataFrame() 
grabRef = "Reference#.*"
grabEsc = "ESCALATION:*"
grabLprgx = "^[0-9]{7}......"
grab = "License Plate*"
grabTrstwo = "/.*(\d{2}:\d{2}.(AM|PM=?))"
rowDict = {"TOLL AGENCY":"THE TOLL ROADS","LP":"","LP STATE":"","TRXN.DATE $ TIME":"","EXIT LANE/LOCATION":"","ACCOUNT#":"", "REFERENCE # OR INVOICE #":"","VIOLATION#":"","AMOUNT DUE":"","DUE DATE":"","PIN NO#":"" }
with pdfplumber.open("scan_455mt__amazon_the_toll_roads_june_29_(jm).pdf") as pdf:
       #Esc=""
       output_list = []
       for page in pdf.pages:
        pageText = page.extract_text()
        for line in pageText.split("\n"):
              
            # print(line,"--------------") 
              matchRef =  reg_ex.search(grabRef,line)  
              if matchRef:
                #print("founhn")
                split_line = line.split()
                reference = split_line[1]
                rowDict["REFERENCE # OR INVOICE #"] = reference.replace(",", "")
              else:
                    pass 
              matchEsc = reg_ex.search(grabEsc,line)
              if matchEsc:
                  split_line = line.split()
                  duedate = split_line[5]
                  rowDict["DUE DATE"] = duedate.replace(":", "")
              else:
                    pass
                    
                    
                    
                     
              matchTrstwo = reg_ex.search(grabTrstwo,line)
              if matchTrstwo:
                #print(line)
                split_line = line.split()
                datetime = split_line[0]+" "+split_line[1]+" "+split_line[2]
                lp = split_line[3]
                amountdue = split_line[12]
                try:
                 violation = split_line[15]
                except:
                      pass
                location = split_line[4]
                rowDict["TRXN.DATE $ TIME"] = datetime
                rowDict["LP"] = lp
                rowDict["AMOUNT DUE"] = amountdue
                rowDict["VIOLATION#"] = violation
                rowDict["EXIT LANE/LOCATION"] = split_line[4]+" "+split_line[5]+" "+split_line[6]+" "+split_line[7]+" "+split_line[8]+" "+split_line[9]
                   
              

                output_list.append(rowDict)
                dff = pd.DataFrame(output_list)
                output_list = []
                df = pd.concat([df, dff])
                             
             
                    

              
print("writing out")
df.to_excel("outpeace.xlsx", index=False)