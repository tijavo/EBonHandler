import pdfplumber
import sys
import json

def parse_rewe_bon(pdf_path):
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
        
        lines = text.split('\n')
        for line in lines:
            parts = line.split()
            
            if len(parts) > 1:
                if parts[-1] in ['B', 'A','*', '']:
                    if(parts[-1] == '*'):
                        parts.pop()
                        if len(parts) > 1:
                            if not parts[-1] in ['B', 'A', '']:
                                continue
                        
                    product = ' '.join(parts[:-2])
                    price = parts[-2]
                    category = parts[-1]
                    data.append([product, price, category])
            

    return data



if __name__ == "__main__":
    pdf_path = 'C:\\Users\\vosst\\Downloads\\REWE-eBon.pdf'
    pdf_path = sys.argv[1]
    data = parse_rewe_bon(pdf_path)
    print(json.dumps(data, indent=2))