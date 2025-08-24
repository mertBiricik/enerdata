#!/usr/bin/env python3
"""
Excel to HTML Converter for Energy Data
Converts multi-sheet Excel files to HTML dashboards with interactive charts
"""

import pandas as pd
import json
import os
import sys
from pathlib import Path
import re


def excel_to_js_data(excel_path):
    """Convert Excel file to JavaScript data format, handling different structures"""
    
    try:
        excel_file = pd.ExcelFile(excel_path)
        print(f"Processing {excel_path}")
        print(f"Found {len(excel_file.sheet_names)} sheets")
        
        # Try different conversion strategies based on file structure
        
        # Check if it's a document catalog (files 4-7)
        excel_name = str(excel_path).lower()
        if any(keyword in excel_name for keyword in ['yasal', 'strateji', 'kalkinma', 'ab_ilerleme', 'politika']):
            return convert_document_excel(excel_path)
        
        # Strategy 1: Year-based sheets (like file 1)
        elif any(sheet.strip().isdigit() for sheet in excel_file.sheet_names):
            return convert_year_sheets(excel_file, excel_path)
        
        # Strategy 2: Years as columns (like file 3)
        elif any('unnamed' in str(col).lower() for df in [pd.read_excel(excel_path, sheet_name=sheet) for sheet in excel_file.sheet_names[:1]] for col in df.columns):
            return convert_years_as_columns(excel_file, excel_path)
        
        # Strategy 3: Years as rows (like file 2)  
        else:
            return convert_years_as_rows(excel_file, excel_path)
            
    except Exception as e:
        print(f"Error processing Excel file {excel_path}: {e}")
        return []


def convert_year_sheets(excel_file, excel_path):
    """Convert Excel with year-based sheets"""
    category_data = {}
    
    # Process each sheet (year)
    for sheet_name in excel_file.sheet_names:
        year = sheet_name.strip()
        if not year.isdigit():
            print(f"Skipping non-year sheet: {sheet_name}")
            continue
            
        try:
            df = pd.read_excel(excel_path, sheet_name=sheet_name)
            
            # Process each row (category)
            for index, row in df.iterrows():
                category = row.iloc[0]  # First column is the category
                
                if pd.isna(category) or category == '':
                    continue
                    
                category = str(category).strip()
                
                # Initialize category if not exists
                if category not in category_data:
                    category_data[category] = {'Kategori': category}
                
                # Find the "Toplam" (Total) column for this row
                total_value = None
                for col_name in df.columns:
                    col_name_lower = str(col_name).lower()
                    if 'toplam' in col_name_lower or col_name == 'Toplam':
                        total_value = row[col_name]
                        break
                
                # If no total column found, use the last column
                if total_value is None:
                    total_value = row.iloc[-1]
                
                # Store the value for this year
                if pd.isna(total_value):
                    category_data[category][year] = None
                else:
                    try:
                        category_data[category][year] = float(total_value)
                    except (ValueError, TypeError):
                        category_data[category][year] = None
                        
        except Exception as e:
            print(f"Error processing sheet {sheet_name}: {e}")
            continue
    
    return list(category_data.values())


def convert_years_as_columns(excel_file, excel_path):
    """Convert Excel where years are columns and categories are rows"""
    category_data = {}
    
    for sheet_name in excel_file.sheet_names:
        if 'tüketim' in sheet_name.lower():
            continue  # Skip consumption sheets that don't have year structure
            
        try:
            df = pd.read_excel(excel_path, sheet_name=sheet_name)
            
            # First column is categories, rest are years
            category_col = df.columns[0]
            year_cols = [col for col in df.columns[1:] if str(col).isdigit() or (isinstance(col, (int, float)) and not pd.isna(col))]
            
            for index, row in df.iterrows():
                category = row[category_col]
                
                if pd.isna(category) or category == '':
                    continue
                    
                category = str(category).strip()
                
                if category not in category_data:
                    category_data[category] = {'Kategori': category}
                
                # Add data for each year
                for year_col in year_cols:
                    year = str(int(year_col))
                    value = row[year_col]
                    
                    if pd.isna(value):
                        category_data[category][year] = None
                    else:
                        try:
                            category_data[category][year] = float(value)
                        except (ValueError, TypeError):
                            category_data[category][year] = None
                            
        except Exception as e:
            print(f"Error processing sheet {sheet_name}: {e}")
            continue
    
    return list(category_data.values())


def convert_years_as_rows(excel_file, excel_path):
    """Convert Excel where years are rows and energy types are columns"""
    # For each sheet, transpose the data
    all_data = []
    
    for sheet_name in excel_file.sheet_names:
        try:
            df = pd.read_excel(excel_path, sheet_name=sheet_name)
            
            if 'Yıllar' not in df.columns:
                continue
                
            # Set years as index
            df = df.set_index('Yıllar')
            
            # For each energy type (column), create a category
            for col_name in df.columns:
                if col_name == 'Yıllar':
                    continue
                    
                category = f"{sheet_name} - {col_name}".strip()
                category_data = {'Kategori': category}
                
                # Add data for each year
                for year in df.index:
                    if pd.isna(year):
                        continue
                    year_str = str(int(year))
                    value = df.loc[year, col_name]
                    
                    if pd.isna(value):
                        category_data[year_str] = None
                    else:
                        try:
                            category_data[year_str] = float(value)
                        except (ValueError, TypeError):
                            category_data[year_str] = None
                
                all_data.append(category_data)
                
        except Exception as e:
            print(f"Error processing sheet {sheet_name}: {e}")
            continue
    
    return all_data


def fix_link_format(link):
    """Fix link format by adding https:// if missing"""
    if not link or pd.isna(link):
        return link
    
    link_str = str(link).strip()
    if link_str.startswith('www.'):
        return 'https://' + link_str
    return link_str


def clean_text_for_json(text):
    """Clean text to prevent JSON syntax errors"""
    if not text or pd.isna(text):
        return text
    
    text_str = str(text)
    # Replace all types of line breaks and control characters
    text_str = text_str.replace('\n', ' ')  # Line feeds
    text_str = text_str.replace('\r', ' ')  # Carriage returns
    text_str = text_str.replace('\t', ' ')  # Tabs
    text_str = text_str.replace('\v', ' ')  # Vertical tabs
    text_str = text_str.replace('\f', ' ')  # Form feeds
    text_str = text_str.replace('\x00', '')  # Null characters
    
    # Remove or replace other problematic Unicode characters
    import re
    # Replace any remaining control characters (except space)
    text_str = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', text_str)
    
    # Clean up multiple spaces
    text_str = re.sub(r'\s+', ' ', text_str).strip()
    
    return text_str


def convert_document_excel(excel_path):
    """Convert document catalog Excel to JavaScript data format"""
    all_docs = []
    
    try:
        excel_file = pd.ExcelFile(excel_path)
        
        # Determine file type based on filename for specific mapping
        filename = str(excel_path).lower()
        
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(excel_path, sheet_name=sheet_name)
            
            # Skip empty sheets
            if df.empty:
                continue
            
            # Find the first non-empty row as headers
            header_row = None
            for idx, row in df.iterrows():
                if not row.isnull().all():
                    header_row = idx
                    break
            
            if header_row is None:
                continue
                
            # Use the first non-empty row as column names
            headers = df.iloc[header_row].fillna('').astype(str).tolist()
            
            # Special handling for file 6 (Kalkınma Planları) with multi-row structure
            if 'kalkinma' in filename:
                all_docs = process_kalkinma_planlari_excel(df, headers, header_row)
            else:
                # Standard processing for other files
                for idx in range(header_row + 1, len(df)):
                    row = df.iloc[idx]
                    if row.isnull().all():
                        continue
                        
                    doc = {}
                    for i, header in enumerate(headers):
                        if header and i < len(row):
                            value = row.iloc[i]
                            if not pd.isna(value):
                                # Keep original header names exactly as they are in Excel
                                clean_header = header.strip()
                                value_str = clean_text_for_json(str(value).strip())
                                
                                # Fix link format if it's a link column
                                if 'link' in clean_header.lower() or 'erişim' in clean_header.lower():
                                    value_str = fix_link_format(value_str)
                                
                                # Store with original Excel column name
                                doc[clean_header] = value_str
                    
                    if doc:  # Only add if document has data
                        all_docs.append(doc)
    
    except Exception as e:
        print(f"Error processing document Excel {excel_path}: {e}")
    
    return all_docs

def process_kalkinma_planlari_excel(df, headers, header_row):
    """Special processing for Kalkınma Planları with multi-row data structure"""
    all_docs = []
    
    # Get the actual column headers from header_row (row 0)
    actual_headers = []
    for i in range(len(df.columns)):
        header_value = df.iloc[header_row, i]
        if pd.notna(header_value) and str(header_value).strip():
            actual_headers.append(str(header_value).strip())
        else:
            actual_headers.append(f"Col_{i}")  # Fallback for empty headers
    
    print(f"Actual headers: {actual_headers}")
    
    # Process each document by looking for rows with document numbers
    current_doc = None
    
    for idx in range(header_row + 1, len(df)):
        row = df.iloc[idx]
        
        # Find first non-empty cell
        first_data_col = None
        first_value = None
        for i in range(len(row)):
            if not pd.isna(row.iloc[i]):
                first_data_col = i
                first_value = row.iloc[i]
                break
        
        if first_data_col is not None:
            # If this looks like a document number, start new document
            if str(first_value).strip().isdigit():
                # Save previous document if it exists
                if current_doc and any(v for v in current_doc.values() if v):
                    all_docs.append(current_doc)
                
                # Start new document
                current_doc = {}
                
                # Process all columns for this document
                for i in range(len(row)):
                    value = row.iloc[i]
                    if not pd.isna(value):
                        header = actual_headers[i] if i < len(actual_headers) else f"Col_{i}"
                        value_str = clean_text_for_json(str(value).strip())
                        
                        # Fix link format if it's a link column
                        if 'link' in header.lower():
                            value_str = fix_link_format(value_str)
                        
                        current_doc[header] = value_str
            
            # If current document exists, this might be additional content
            elif current_doc is not None:
                # Add additional content to existing fields
                for i in range(len(row)):
                    value = row.iloc[i]
                    if not pd.isna(value):
                        header = actual_headers[i] if i < len(actual_headers) else f"Col_{i}"
                        value_str = clean_text_for_json(str(value).strip())
                        
                        # Append to existing content or create new
                        if header in current_doc:
                            # Add as additional content with space separator
                            current_doc[header] += " " + value_str
                        else:
                            current_doc[header] = value_str
    
    # Don't forget to add the last document
    if current_doc and any(v for v in current_doc.values() if v):
        all_docs.append(current_doc)
    
    return all_docs


def create_html_from_template(template_path, js_data, output_path, title):
    """Create HTML file by replacing data in template"""
    
    try:
        # Check if it's a document template
        is_document_template = 'document_template.html' in str(template_path) or 'unified_document_template.html' in str(template_path)
        
        if is_document_template:
            return create_document_html(js_data, output_path, title, template_path)
        
        # Regular chart-based template processing
        with open(template_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Convert data to JavaScript format
        js_data_str = json.dumps(js_data, indent=2, ensure_ascii=False, default=str)
        
        # Replace the embedded data - check for different variable names
        patterns = [
            (r'const embeddedDataA = \[[\s\S]*?\];', lambda: f'const embeddedDataA = {js_data_str};'),
            (r'const embeddedDataB = \[[\s\S]*?\];', lambda: f'const embeddedDataB = {js_data_str};'),
            (r'const embeddedDataC = \[[\s\S]*?\];', lambda: f'const embeddedDataC = {js_data_str};'),
            (r'const embeddedData = \[[\s\S]*?\];', lambda: f'const embeddedData = {js_data_str};'),
            (r'const embeddedYasalData = \[[\s\S]*?\];', lambda: f'const embeddedYasalData = {js_data_str};'),
        ]
        
        new_html_content = html_content
        data_replaced = False
        
        for pattern, replacement_func in patterns:
            if re.search(pattern, new_html_content):
                new_html_content = re.sub(pattern, replacement_func(), new_html_content, count=1)
                data_replaced = True
                break
        
        if not data_replaced:
            print(f"Warning: No embedded data pattern found in template for {output_path}")
            # Try to add data at the end of script section
            script_end = r'</script>'
            if re.search(script_end, new_html_content):
                data_addition = f'\n        const embeddedDataA = {js_data_str};\n'
                new_html_content = re.sub(r'(\s*</script>)', data_addition + r'\1', new_html_content, count=1)
                data_replaced = True
        
        if not data_replaced:
            print(f"Error: Could not embed data in {output_path}")
            return False
        
        # Update the title if different
        title_pattern = r'<title>.*?</title>'
        title_replacement = f'<title>{title}</title>'
        new_html_content = re.sub(title_pattern, title_replacement, new_html_content)
        
        # Update h1 title in header
        h1_pattern = r'<h1[^>]*>.*?</h1>'
        h1_replacement = f'<h1>{title}</h1>'
        new_html_content = re.sub(h1_pattern, h1_replacement, new_html_content, flags=re.DOTALL)
        
        # Write the new HTML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_html_content)
        
        print(f"Created {output_path}")
        return True
        
    except Exception as e:
        print(f"Error creating HTML file {output_path}: {e}")
        return False


def create_document_html(js_data, output_path, title, template_path=None):
    """Create document HTML from template"""
    
    try:
        # Use provided template path or fallback to default
        if template_path and os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            print(f"Using {os.path.basename(template_path)} for {output_path}")
        else:
            # Fallback to unified template
            try:
                with open('unified_document_template.html', 'r', encoding='utf-8') as f:
                    template_content = f.read()
                print(f"Using unified_document_template.html for {output_path}")
            except FileNotFoundError:
                print(f"No document template found for {output_path}")
                return False
        
        # Convert data to JavaScript format
        js_data_str = json.dumps(js_data, indent=4, ensure_ascii=False, default=str)
        
        # Replace placeholders
        html_content = template_content.replace('{{DOCUMENT_TITLE}}', title)
        html_content = html_content.replace('{{DOCUMENT_DESCRIPTION}}', f'Türkiye enerji sektörüne dair {len(js_data)} döküman')
        
        # Set Excel URL based on output file
        excel_url = ''
        output_filename = os.path.basename(output_path)
        if '4_yasal' in output_filename:
            excel_url = 'http://enerjiveri.khas.edu.tr/wp-content/uploads/2025/08/4_yasal_duzenlemeler.xlsx'
        elif '5_strateji' in output_filename:
            excel_url = 'http://enerjiveri.khas.edu.tr/wp-content/uploads/2025/08/5_strateji_ve_politika_belgeleri.xlsx'
        elif '6_kalkinma' in output_filename:
            excel_url = 'http://enerjiveri.khas.edu.tr/wp-content/uploads/2025/08/6_kalkinma_planlari.xlsx'
        elif '7_ab' in output_filename:
            excel_url = 'http://enerjiveri.khas.edu.tr/wp-content/uploads/2025/08/7_ab_ilerleme_raporlari.xlsx'
        
        html_content = html_content.replace('{{EXCEL_URL}}', excel_url)
        
        # Replace the embedded data - try different patterns
        data_patterns = [
            (r'const allDocuments = \[\s*// Data will be replaced here\s*\];', f'const allDocuments = {js_data_str};'),
            (r'const embeddedData = \[\s*// Data will be replaced here\s*\];', f'const embeddedData = {js_data_str};'),
        ]
        
        data_replaced = False
        for pattern, replacement in data_patterns:
            if re.search(pattern, html_content):
                html_content = re.sub(pattern, replacement, html_content)
                data_replaced = True
                break
        
        if not data_replaced:
            print(f"Warning: Could not find data pattern to replace in {output_path}")
            # Try to add data before closing script tag
            script_pattern = r'(\s*</script>)'
            data_addition = f'\n        const allDocuments = {js_data_str};\n'
            html_content = re.sub(script_pattern, data_addition + r'\1', html_content, count=1)
        
        # Write the new HTML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Created document HTML {output_path}")
        return True
        
    except Exception as e:
        print(f"Error creating document HTML {output_path}: {e}")
        return False


def get_title_from_filename(filename):
    """Extract a readable title from filename"""
    
    # Remove file extension
    name = filename.replace('.xlsx', '').replace('.html', '')
    
    # Define proper Turkish titles for all files (without numbers)
    title_map = {
        '1_birincil_enerjinin_kaynaklara_gore_uretimi_ve_tuketimi': 'Birincil Enerjinin Kaynaklara Göre Üretimi ve Tüketimi',
        '2_elektrik_enerjisinin_kaynaklara_gore kurulu_gucu_ve_uretimi': 'Elektrik Enerjisinin Kaynaklara Göre Kurulu Gücü ve Üretimi',
        '3_elektrik_enerjisinin_brut_uretimi_ve_sektorel_tuketimi': 'Elektrik Enerjisinin Brüt Üretimi ve Sektörel Tüketimi',
        '4_yasal_duzenlemeler': 'Yasal Düzenlemeler',
        '5_strateji_ve_politika_belgeleri': 'Strateji ve Politika Belgeleri',
        '6_kalkinma_planlari': 'Kalkınma Planları',
        '7_ab_ilerleme_raporlari': 'AB İlerleme Raporları'
    }
    
    # Check if it's one of the special files
    if name in title_map:
        return title_map[name]
    
    # Split by underscore and create title for other files
    parts = name.split('_')
    if len(parts) >= 2:
        number = parts[0]
        rest = ' '.join(parts[1:])
        return f"{number}. {rest.replace('_', ' ').title()}"
    
    return name.replace('_', ' ').title()


def process_all_files():
    """Process all Excel files in the current directory"""
    
    current_dir = Path('.')
    excel_files = list(current_dir.glob('*.xlsx'))
    
    if not excel_files:
        print("No Excel files found in current directory")
        return
    
    # Process each Excel file
    for excel_path in excel_files:
        print(f"\n--- Processing {excel_path.name} ---")
        
        # Convert Excel to JavaScript data
        js_data = excel_to_js_data(excel_path)
        
        if not js_data:
            print(f"No data extracted from {excel_path.name}")
            continue
        
        # Create corresponding HTML file
        html_filename = excel_path.name.replace('.xlsx', '.html')
        html_path = current_dir / html_filename
        
        # Choose appropriate template
        template_path = choose_template(excel_path, current_dir)
        if not template_path:
            print(f"No suitable template found for {excel_path.name}")
            continue
            
        print(f"Using {template_path} as template")
        
        # Generate title
        title = get_title_from_filename(excel_path.name)
        
        # Create HTML file
        success = create_html_from_template(template_path, js_data, html_path, title)
        
        if success:
            print(f"✓ Successfully created {html_filename}")
        else:
            print(f"✗ Failed to create {html_filename}")


def choose_template(excel_path, current_dir):
    """Choose appropriate template for each Excel file"""
    
    excel_name = excel_path.name
    
    # For file 4, use unified template to avoid corrupted backup data
    if '4_yasal_duzenlemeler' in excel_name:
        unified_template = current_dir / 'unified_document_template.html'
        if unified_template.exists():
            return unified_template
    
    # For files 5-7 (document catalogs), use the unified document template
    if any(keyword in excel_name for keyword in ['strateji', 'kalkinma', 'ab_ilerleme', 'politika']):
        unified_template = current_dir / 'unified_document_template.html'
        if unified_template.exists():
            return unified_template
    
    # First, try to use corresponding backup template
    backup_dir = current_dir / 'backup_html'
    if backup_dir.exists():
        backup_template = backup_dir / excel_name.replace('.xlsx', '.html')
        if backup_template.exists():
            return backup_template
    
    # Then try current directory
    current_template = current_dir / excel_name.replace('.xlsx', '.html') 
    if current_template.exists():
        return current_template
    
    # Fall back to first available chart-based template for data files
    chart_templates = [
        'backup_html/1_birincil_enerjinin_kaynaklara_gore_uretimi_ve_tuketimi.html',
        'backup_html/2_elektrik_enerjisinin_kaynaklara_gore kurulu_gucu_ve_uretimi.html',
        'backup_html/3_elektrik_enerjisinin_brut_uretimi_ve_sektorel_tuketimi.html',
        '1_birincil_enerjinin_kaynaklara_gore_uretimi_ve_tuketimi.html'
    ]
    for template in chart_templates:
        template_path = current_dir / template
        if template_path.exists():
            return template_path
    
    return None


def main():
    """Main function"""
    
    if len(sys.argv) > 1:
        excel_path = sys.argv[1]
        if not os.path.exists(excel_path):
            print(f"Excel file not found: {excel_path}")
            return
        
        # Process single file
        js_data = excel_to_js_data(excel_path)
        print(f"Extracted {len(js_data)} categories")
        
        # Print sample data
        if js_data:
            print("\nSample data:")
            for item in js_data[:3]:
                print(json.dumps(item, indent=2, ensure_ascii=False, default=str))
    else:
        # Process all files
        process_all_files()


if __name__ == '__main__':
    main()