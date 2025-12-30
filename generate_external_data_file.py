#!/usr/bin/env python3
import json
from pathlib import Path
from excel_to_html_converter import excel_to_js_data

def main():
    excel_path = '1_birincil_enerjinin_kaynaklara_gore_uretimi_ve_tuketimi.xlsx'
    js_data = excel_to_js_data(excel_path)
    out_dir = Path('data') / 'a'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / 'data_a_embedded.js'
    with out_file.open('w', encoding='utf-8') as f:
        f.write('embeddedDataA = ')
        json.dump(js_data, f, ensure_ascii=False, indent=2, default=str)
        f.write(';\n')
    print(f"Wrote {out_file} with {len(js_data)} records.")

if __name__ == '__main__':
    main()

