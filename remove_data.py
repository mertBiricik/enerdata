#!/usr/bin/env python3
"""
Remove Embedded Data - Safety Script
Removes embedded JavaScript data from HTML files to make them safe for editing.
Replaces embedded data with external references.
"""

import os
import re

def remove_embedded_data_from_file(filepath):
    """Remove embedded JavaScript data from a single HTML file"""
    if not os.path.exists(filepath):
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_size = len(content)
        
        # Patterns for different embedded data variables
        patterns = [
            (r'const embeddedYasalData = \[.*?\];', 'embeddedYasalData', 'nitel_data/yasal_data.js'),
            (r'const embeddedStratejiData = \[.*?\];', 'embeddedStratejiData', 'nitel_data/strateji_data.js'),
            (r'const embeddedKalkinmaData = \[.*?\];', 'embeddedKalkinmaData', 'nitel_data/kalkinma_data.js'),
            (r'const embeddedAbData = \[.*?\];', 'embeddedAbData', 'nitel_data/ab_data.js'),
            (r'const embeddedDataA = \[.*?\];', 'embeddedDataA', 'data/a/data_a_embedded.js'),
            (r'const embeddedDataB = \[.*?\];', 'embeddedDataB', 'data/b/data_b_embedded.js'),
            (r'const embeddedRawData = \[.*?\];', 'embeddedRawData', 'data/C/c_embedded_data.js')
        ]
        
        replacements_made = 0
        
        for pattern, var_name, external_file in patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            if matches:
                # Replace with external script reference
                replacement = f'// External data loaded from {external_file}\n// const {var_name} = [...]; // REMOVED FOR SAFE EDITING'
                content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                replacements_made += len(matches)
        
        if replacements_made > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            new_size = len(content)
            size_reduction = original_size - new_size
            
            print(f"✅ {filepath}: Removed {replacements_made} data block(s), saved {size_reduction/1024:.1f} KB")
            return True
        else:
            print(f"ℹ️  {filepath}: No embedded data found")
            return True
            
    except Exception as e:
        print(f"❌ {filepath}: Error - {e}")
        return False

def main():
    """Remove embedded data from all HTML files"""
    
    print("🔧 Removing embedded JavaScript data from HTML files...")
    print("=" * 50)
    
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    
    if not html_files:
        print("No HTML files found")
        return
    
    success_count = 0
    total_savings = 0
    
    for html_file in sorted(html_files):
        original_size = os.path.getsize(html_file) if os.path.exists(html_file) else 0
        
        if remove_embedded_data_from_file(html_file):
            success_count += 1
            new_size = os.path.getsize(html_file)
            total_savings += (original_size - new_size)
    
    print("=" * 50)
    print(f"Processed {success_count}/{len(html_files)} files successfully")
    print(f"💾 Total space saved: {total_savings/1024:.1f} KB")
    print("✅ HTML files are now safe for editing")

if __name__ == "__main__":
    main() 