import pandas as pd
import json
import re
from pathlib import Path

def get_html_data(html_path):
    with open(html_path, 'r') as f:
        content = f.read()
    
    # Try different variable names
    patterns = [
        r'const embeddedDataA = (\[[\s\S]*?\]);',
        r'const embeddedDataB = (\[[\s\S]*?\]);', 
        r'const embeddedData = (\[[\s\S]*?\]);',
        r'const allDocuments = (\[[\s\S]*?\]);'
    ]
    
    # Special external file check for File 1
    if '1_birincil' in str(html_path):
        ext_path = Path(html_path).parent / 'data/a/data_a_embedded.js'
        if ext_path.exists():
            with open(ext_path, 'r') as f:
                content = f.read()
                match = re.search(r'embeddedDataA = (\[[\s\S]*?\]);', content)
                if match: return json.loads(match.group(1))

    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return json.loads(match.group(1))
    return None

def check_file_1():
    print("\n--- Checking File 1 (Primary Energy) ---")
    excel_path = '1_birincil_enerjinin_kaynaklara_gore_uretimi_ve_tuketimi.xlsx'
    html_path = '1_birincil_enerjinin_kaynaklara_gore_uretimi_ve_tuketimi.html'
    
    # Read Excel: Sheet "1971", Row "Taşkömürü" (just guessing structure, let's look at first row)
    df = pd.read_excel(excel_path, sheet_name='1971')
    # Assuming first col is category
    first_row = df.iloc[0]
    category = first_row.iloc[0] # e.g. "Taşkömürü"
    val_excel = first_row.iloc[-1] # Total usually at end
    
    print(f"Excel (1971): Category='{category}', Value={val_excel}")
    
    data = get_html_data(html_path)
    # Find item in JSON
    item = next((x for x in data if x.get('Kategori') == category), None)
    
    if item:
        val_html = item.get('1971')
        # specific handling for object values (red cells)
        if isinstance(val_html, dict) and 'value' in val_html:
             val_html = val_html['value']
             
        print(f"HTML (1971): Category='{category}', Value={val_html}")
        
        if abs(float(val_excel) - float(val_html)) < 0.001:
            print("✅ MATCH")
        else:
            print("❌ MISMATCH")
    else:
        print(f"❌ Category '{category}' not found in HTML")

def check_file_4():
    print("\n--- Checking File 4 (Laws) ---")
    excel_path = '4_yasal_duzenlemeler.xlsx'
    html_path = '4_yasal_duzenlemeler.html'
    
    df = pd.read_excel(excel_path)
    # First row
    row = df.iloc[0]
    # Find title column - usually 'Başlık' or similar. Let's print headers
    # from previous exploration we saw 'Başlık'
    title_excel = row['Başlık']
    no_excel = row['No']
    
    print(f"Excel: No={no_excel}, Title='{title_excel}'")
    
    data = get_html_data(html_path)
    item = next((x for x in data if str(x.get('No')) == str(no_excel)), None)
    
    if item:
        title_html = item.get('Başlık')
        print(f"HTML: No={item.get('No')}, Title='{title_html}'")
        
        if title_excel.strip() == title_html.strip():
            print("✅ MATCH")
        else:
            print("❌ MISMATCH")
    else:
         print(f"❌ Document No={no_excel} not found in HTML")

if __name__ == "__main__":
    try:
        check_file_1()
        check_file_4()
    except Exception as e:
        print(f"Error: {e}")
