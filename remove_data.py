#!/usr/bin/env python3
"""
Script to remove embedded data from HTML files and restore external script references
"""

import re
import os

def remove_embedded_data_from_html(html_file, script_src_pattern):
    """Remove embedded JavaScript data and restore external script reference"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Pattern to find embedded script with data
        embedded_pattern = r'<script>\s*const\s+(embeddedData[AB]|embeddedRawData)\s*=.*?</script>'
        
        if not re.search(embedded_pattern, html_content, re.DOTALL):
            print(f"Warning: Could not find embedded data in {html_file}")
            return False
        
        # Replace embedded script with external script reference
        external_script = f'<script src="{script_src_pattern}"></script>'
        new_content = re.sub(embedded_pattern, external_script, html_content, flags=re.DOTALL)
        
        # Write back to file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ Successfully removed embedded data from {html_file}")
        return True
        
    except Exception as e:
        print(f"Error processing {html_file}: {e}")
        return False

def main():
    print("🔄 Removing embedded data from HTML files")
    print("=" * 50)
    
    # Define the files and their external script sources
    files_to_process = [
        {
            'html_file': 'dataset_a_primary_energy.html',
            'script_src': 'data/a/data_a_embedded.js'
        },
        {
            'html_file': 'dataset_b_electricity.html',
            'script_src': 'data/b/data_b_embedded.js'
        },
        {
            'html_file': 'dataset_c_sectoral_consumption.html',
            'script_src': 'data/C/c_embedded_data.js'
        }
    ]
    
    success_count = 0
    
    for file_info in files_to_process:
        html_file = file_info['html_file']
        script_src = file_info['script_src']
        
        print(f"\nProcessing {html_file}...")
        
        # Check if HTML file exists
        if not os.path.exists(html_file):
            print(f"❌ {html_file} not found")
            continue
        
        # Remove embedded data
        if remove_embedded_data_from_html(html_file, script_src):
            success_count += 1
    
    print(f"\n{'='*50}")
    if success_count == len(files_to_process):
        print("✅ SUCCESS: All embedded data removed successfully!")
        print("📁 Files now reference external data files")
    else:
        print(f"⚠️  PARTIAL SUCCESS: {success_count}/{len(files_to_process)} files processed")

if __name__ == "__main__":
    main() 