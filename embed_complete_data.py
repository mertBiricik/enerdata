#!/usr/bin/env python3
"""
Script to embed complete datasets into veri_bankasi.html
Reads the three JavaScript data files and embeds them directly into the HTML
"""

import re
import os

def read_js_data_file(file_path):
    """Read a JavaScript data file and extract the data array"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract the variable name and data
        if 'embeddedDataA' in content:
            var_name = 'embeddedDataA'
        elif 'embeddedDataB' in content:
            var_name = 'embeddedDataB'
        elif 'embeddedRawData' in content:
            var_name = 'embeddedRawData'
        else:
            print(f"Warning: Could not identify variable in {file_path}")
            return None, None
        
        # Find the start of the array
        start_pattern = f'const {var_name} = '
        start_index = content.find(start_pattern)
        if start_index == -1:
            print(f"Warning: Could not find '{start_pattern}' in {file_path}")
            return None, None
        
        # Extract everything from the array start to the semicolon
        array_start = start_index + len(start_pattern)
        
        # Find the matching closing bracket and semicolon
        bracket_count = 0
        in_string = False
        escape_next = False
        end_index = array_start
        
        for i, char in enumerate(content[array_start:], array_start):
            if escape_next:
                escape_next = False
                continue
                
            if char == '\\':
                escape_next = True
                continue
                
            if char == '"' and not escape_next:
                in_string = not in_string
                continue
                
            if not in_string:
                if char == '[':
                    bracket_count += 1
                elif char == ']':
                    bracket_count -= 1
                    if bracket_count == 0:
                        end_index = i + 1
                        break
        
        # Extract the array content
        array_content = content[array_start:end_index]
        
        return var_name, array_content
        
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return None, None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None, None

def update_html_with_complete_data():
    """Update the HTML file with complete embedded data"""
    
    # File paths
    data_files = {
        'embeddedDataA': 'data/a/data_a_embedded.js',
        'embeddedDataB': 'data/b/data_b_embedded.js', 
        'embeddedRawData': 'data/C/c_embedded_data.js'
    }
    
    html_file = 'veri_bankasi.html'
    
    # Read all data files
    datasets = {}
    for var_name, file_path in data_files.items():
        print(f"Reading {file_path}...")
        extracted_var, array_content = read_js_data_file(file_path)
        if extracted_var and array_content:
            datasets[var_name] = array_content
            print(f"  ✓ Successfully read {extracted_var} ({len(array_content)} characters)")
        else:
            print(f"  ✗ Failed to read {file_path}")
    
    if not datasets:
        print("Error: No datasets were successfully loaded")
        return False
    
    # Read the HTML file
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        print(f"\nReading {html_file}...")
    except FileNotFoundError:
        print(f"Error: {html_file} not found")
        return False
    
    # Find the embedded data section
    start_marker = '<!-- Embedded data -->'
    end_marker = '</script>'
    
    start_index = html_content.find(start_marker)
    if start_index == -1:
        print("Error: Could not find embedded data section in HTML")
        return False
    
    # Find the end of the script section
    script_start = html_content.find('<script>', start_index)
    script_end = html_content.find('</script>', script_start) + len('</script>')
    
    # Build the new embedded data section
    new_data_section = f"""     <!-- Embedded data -->
     <script>
         // Complete Dataset A (Primary Energy Production and Consumption by Sources)
         const embeddedDataA = {datasets.get('embeddedDataA', '[]')};
         
         // Complete Dataset B (Electricity Installed Capacity and Production by Sources)  
         const embeddedDataB = {datasets.get('embeddedDataB', '[]')};
         
         // Complete Dataset C (Sectoral Electricity Consumption Distribution)
         const embeddedRawData = {datasets.get('embeddedRawData', '[]')};
     </script>"""
    
    # Replace the embedded data section
    new_html_content = html_content[:start_index] + new_data_section + html_content[script_end:]
    
    # Create backup
    backup_file = 'veri_bankasi_backup.html'
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✓ Created backup: {backup_file}")
    
    # Write the updated HTML
    try:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_html_content)
        print(f"✓ Successfully updated {html_file}")
        
        # Print statistics
        print(f"\nDataset Statistics:")
        for var_name, array_content in datasets.items():
            # Count items by counting opening braces
            item_count = array_content.count('{')
            print(f"  {var_name}: ~{item_count} data series")
        
        return True
        
    except Exception as e:
        print(f"Error writing HTML file: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Embedding complete datasets into veri_bankasi.html")
    print("=" * 50)
    
    success = update_html_with_complete_data()
    
    if success:
        print("\n🎉 SUCCESS: All datasets have been embedded!")
        print("📂 You can now open veri_bankasi.html with complete data")
        print("💾 Backup saved as veri_bankasi_backup.html")
    else:
        print("\n❌ FAILED: Could not embed datasets")
        print("🔍 Please check the error messages above") 