'''
extracting data from pdf using pdf2image
'''
import os
import pdf2image

doc = pdf2image.convert_from_path('./scn_19_port_authority_ny__nj-amazon_(15)_october_7_(bm).pdf')

folder = "doc"
if folder not in os.listdir():
    os.makedirs(folder)
p = 1
for page in doc:
    image_name = "page_"+str(p)+".jpg"  
    page.save(os.path.join(folder, image_name), "JPEG")
    p = p+1
