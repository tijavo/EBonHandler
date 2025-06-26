import pdfplumber
import sys
import json

def parse_edeka_bon(pdf_path):
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
        
        lines = text.split('\n')
        for line in lines:
            parts = line.split()
            
            if len(parts) > 1:
                if parts[1] == "Stk":
                    if len(data) > 0:
                        data[-1][3] = parts[0]
                elif parts[-1][-1] in ['B', 'A']:
                    if len(parts[-1]) > 1 and parts[-1][-2] == '*':
                        subparts = parts[-1].split('*')
                        parts.pop()
                        parts = parts + subparts
                        
                    product = ' '.join(parts[:-2])
                    price = parts[-2]
                    category = parts[-1]
                    data.append([product, price, category,"1"])
    return data

if __name__ == "__main__":
    pdf_path = 'C:\\Users\\vosst\\Downloads\\Kassenbon_2025-06-26_10.09.pdf'
    #pdf_path = sys.argv[1]
    data = parse_edeka_bon(pdf_path)
    print(json.dumps(data, indent=2))