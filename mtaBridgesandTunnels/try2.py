import re
import pandas as pd
import fitz

pdf = fitz.open('./scan_437lm_amazon__mta_tolls_by_mail_(ny)_(14)__august_30.pdf')

for pageno in range(0, len(pdf)-1):
    page = pdf[pageno]
    page_data = page.get_text('page_data')

    print(page_data)