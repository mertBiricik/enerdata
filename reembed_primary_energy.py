#!/usr/bin/env python3
"""
Re-embed dataset for file 1 by inlining embeddedDataA into the HTML.
Sources the data from the Excel (authoritative) rather than the external JS.
"""

import json
import re
from pathlib import Path
from excel_to_html_converter import excel_to_js_data

HTML_PATH = Path('1_birincil_enerjinin_kaynaklara_gore_uretimi_ve_tuketimi.html')
EXCEL_PATH = Path('1_birincil_enerjinin_kaynaklara_gore_uretimi_ve_tuketimi.xlsx')
BACKUP_PATH = Path('1_birincil_enerjinin_kaynaklara_gore_uretimi_ve_tuketimi_backup.html')

def inline_data(html_text: str, js_data_str: str) -> str:
    """
    Replace any embeddedDataA assignment with the new data and remove external loader if present.
    Handles:
      - let embeddedDataA = [...] ;
      - const embeddedDataA = [...] ;
      - placeholder let embeddedDataA = [];
    Also removes <script src="data/a/data_a_embedded.js"></script> if present.
    """
    # Remove external loader tag if present
    html_text = re.sub(
        r'\s*<script\s+src="data/a/data_a_embedded\.js"></script>\s*',
        '\n',
        html_text,
        flags=re.IGNORECASE
    )

    # Replacement function that keeps the original 'let' or 'const'
    def _repl(m):
        decl = m.group(1)  # let|const
        return f'{decl} embeddedDataA = {js_data_str};'

    # Try to replace an existing array assignment first
    patterns = [
        r'(let|const)\s+embeddedDataA\s*=\s*\[[\s\S]*?\];',  # any current value
    ]
    replaced = False
    for pat in patterns:
        new_html = re.sub(pat, _repl, html_text, count=1)
        if new_html != html_text:
            html_text = new_html
            replaced = True
            break

    # If nothing matched, insert right after the embedded data comment block if it exists
    if not replaced:
        insert_pat = r'(<!-- Embedded data -->\s*<script>\s*)(?:let|const)\s+embeddedDataA\s*=\s*\[\s*\]\s*;\s*(</script>)'
        new_html = re.sub(insert_pat, rf'\1let embeddedDataA = {js_data_str};\2', html_text, count=1)
        if new_html != html_text:
            html_text = new_html
            replaced = True

    # If still not replaced, append a new script before </body>
    if not replaced:
        html_text = re.sub(
            r'</body>',
            f'<script>let embeddedDataA = {js_data_str};</script>\n</body>',
            html_text,
            count=1
        )

    return html_text

def main():
    if not HTML_PATH.exists():
        raise SystemExit(f'HTML not found: {HTML_PATH}')
    if not EXCEL_PATH.exists():
        raise SystemExit(f'Excel not found: {EXCEL_PATH}')

    # Read authoritative data from Excel
    js_data = excel_to_js_data(str(EXCEL_PATH))
    js_data_str = json.dumps(js_data, ensure_ascii=False, indent=2, default=str)

    # Backup current HTML
    BACKUP_PATH.write_text(HTML_PATH.read_text(encoding='utf-8'), encoding='utf-8')

    # Inline
    html_text = HTML_PATH.read_text(encoding='utf-8')
    new_html = inline_data(html_text, js_data_str)
    HTML_PATH.write_text(new_html, encoding='utf-8')

    print(f'Embedded {len(js_data)} records into {HTML_PATH.name}. Backup saved to {BACKUP_PATH.name}.')

if __name__ == '__main__':
    main()


