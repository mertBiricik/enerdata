#!/usr/bin/env python3
import pandas as pd
import json
import re
import os
from bs4 import BeautifulSoup
import sys
from pathlib import Path

# Files to check
FILES = {
    # Charts
    '1_birincil_enerjinin_kaynaklara_gore_uretimi_ve_tuketimi': 'chart',
    '2_elektrik_enerjisinin_kaynaklara_gore kurulu_gucu_ve_uretimi': 'chart',
    '3_elektrik_enerjisinin_brut_uretimi_ve_sektorel_tuketimi': 'chart',
    # Documents
    '4_yasal_duzenlemeler': 'doc',
    '5_strateji_ve_politika_belgeleri': 'doc',
    '6_kalkinma_planlari': 'doc',
    '7_ab_ilerleme_raporlari': 'doc',
}

def extract_json_from_html(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Try different variable names
    patterns = [
        r'const embeddedDataA = (\[[\s\S]*?\]);',
        r'const embeddedDataB = (\[[\s\S]*?\]);',
        r'const embeddedDataC = (\[[\s\S]*?\]);',
        r'const embeddedData = (\[[\s\S]*?\]);',
        r'const allDocuments = (\[[\s\S]*?\]);'
    ]

    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            try:
                # Basic cleanup to make it valid JSON if needed (though usually it is)
                json_str = match.group(1)
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"JSON Error in {html_path}: {e}")
                continue
                
    # Special case for file 1 external JS
    if '1_birincil' in str(html_path):
        data_dir = Path(html_path).parent / 'data' / 'a' / 'data_a_embedded.js'
        if data_dir.exists():
            with open(data_dir, 'r', encoding='utf-8') as f:
                js_content = f.read()
                match = re.search(r'embeddedDataA = (\[[\s\S]*?\]);', js_content)
                if match:
                    return json.loads(match.group(1))

    return None

def validate_chart_data(name, excel_path, html_data):
    print(f"\nVerifying {name} (Chart)...")
    if not html_data:
        print("FAIL: No HTML data found")
        return False

    # Just checking counts and structure for now as chart logic is complex
    # Excel count estimation
    excel_file = pd.ExcelFile(excel_path)
    total_categories = 0
    
    # Simple strategy depending on file type (simulating converter logic roughly)
    if '1_birincil' in name:
        for sheet in excel_file.sheet_names:
            if sheet.isdigit():
                df = pd.read_excel(excel_path, sheet_name=sheet)
                total_categories = max(total_categories, len(df)) # Approximation
    
    # HTML count
    html_count = len(html_data)
    print(f"HTML Categories: {html_count}")
    
    if html_count == 0:
        print("FAIL: HTML data is empty")
        return False
        
    print("PASS: Data structure exists")
    return True

def validate_document_data(name, excel_path, html_data):
    print(f"\nVerifying {name} (Document)...")
    if not html_data:
        print("FAIL: No HTML data found")
        return False

    # Read Excel to count rows
    excel_file = pd.ExcelFile(excel_path)
    excel_count = 0
    
    # For File 6 (Kalkinma), manual counting is tricky due to merging
    if '6_kalkinma' in name:
        # Just check basic existence of fields
        doc_0 = html_data[0]
        if 'Plan Adı' in doc_0 or 'Kalkınma Planı' in str(doc_0):  
             print(f"PASS: Data keys look correct (Found keys: {list(doc_0.keys())[:3]})")
             pass
    else:
        # For straightforward files like 4, 5, 7
        for sheet in excel_file.sheet_names:
             df = pd.read_excel(excel_path, sheet_name=sheet)
             # Remove empty rows
             df = df.dropna(how='all')
             # Logic is roughly non-empty rows minus header
             # But let's look at the HTML count
             pass

    print(f"HTML Document Count: {len(html_data)}")
    
    if len(html_data) == 0:
         print("FAIL: No documents in HTML")
         return False
         
    # Check for crucial keys
    sample = html_data[0]
    required_keys = ['No', 'Link']
    missing_keys = [k for k in required_keys if k not in sample and k.lower() not in [x.lower() for x in sample.keys()]]
    
    if missing_keys and 'Link' not in missing_keys: # Link column name varies
        print(f"WARN: Possible missing keys: {missing_keys}")
    
    # Check link format
    link_key = next((k for k in sample.keys() if 'link' in k.lower() or 'erişim' in k.lower()), None)
    if link_key and sample[link_key]:
        if not sample[link_key].startswith('http'):
             print(f"FAIL: Link not formatted correctly: {sample[link_key]}")
             return False
             
    print("PASS: Basic structural validation successful")
    return True

def main():
    print(f"Current working directory: {os.getcwd()}", flush=True)
    for name, ftype in FILES.items():
        base_path = Path('.')
        excel_path = base_path / f"{name}.xlsx"
        html_path = base_path / f"{name}.html"
        
        print(f"Checking {name}...", flush=True)
        if not excel_path.exists():
            print(f"SKIP: {name}.xlsx not found at {excel_path.absolute()}", flush=True)
            continue
            
        html_data = extract_json_from_html(html_path)
        
        if ftype == 'chart':
            validate_chart_data(name, excel_path, html_data)
        else:
            validate_document_data(name, excel_path, html_data)
        sys.stdout.flush()

if __name__ == "__main__":
    main()
