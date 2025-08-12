#!/usr/bin/env python3
"""
Restore Embedded Data - Safety Script
Restores embedded JavaScript data into HTML files from external data files.
Re-embeds data for WordPress deployment.
"""

import os
import re

def restore_embedded_data_in_file(filepath):
    """Restore embedded JavaScript data in a single HTML file"""
    if not os.path.exists(filepath):
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_size = len(content)
        
        # Mapping of files to data variables and external files
        file_mappings = {
            '4_yasal_duzenlemeler.html': ('embeddedYasalData', 'nitel_data/yasal_data.js'),
            '5_strateji_ve_politika_belgeleri.html': ('embeddedStratejiData', 'nitel_data/strateji_data.js'),
            '6_kalkinma_planlari.html': ('embeddedKalkinmaData', 'nitel_data/kalkinma_data.js'),
            '7_ab_ilerleme_raporlari.html': ('embeddedAbData', 'nitel_data/ab_data.js'),
            '1_birincil_enerjinin_kaynaklara_gore_uretimi_ve_tuketimi.html': ('embeddedDataA', 'data/a/data_a_embedded.js'),
            '2_elektrik_enerjisinin_kaynaklara_gore_kurulu_gucu_ve_uretimi.html': ('embeddedDataB', 'data/b/data_b_embedded.js'),
            '3_elektrik_enerjisinin_brut_uretimi_ve_sektorel_tuketimi.html': ('embeddedRawData', 'data/C/c_embedded_data.js')
        }
        
        filename = os.path.basename(filepath)
        
        if filename in file_mappings:
            var_name, external_file = file_mappings[filename]
            
            # Check if external data file exists
            if os.path.exists(external_file):
                try:
                    with open(external_file, 'r', encoding='utf-8') as f:
                        external_data = f.read().strip()
                    
                    # Pattern to find the placeholder comment
                    placeholder_pattern = f'// External data loaded from {re.escape(external_file)}\\s*\\n// const {re.escape(var_name)} = \\[\\.\\.\\.\\]; // REMOVED FOR SAFE EDITING'
                    
                    if re.search(placeholder_pattern, content):
                        # Replace placeholder with actual data
                        content = re.sub(placeholder_pattern, external_data, content)
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        new_size = len(content)
                        size_increase = new_size - original_size
                        
                        print(f"✅ {filepath}: Restored {var_name}, added {size_increase/1024:.1f} KB")
                        return True
                    else:
                        print(f"ℹ️  {filepath}: No placeholder found for {var_name}")
                        return True
                        
                except Exception as e:
                    print(f"❌ {filepath}: Error reading {external_file} - {e}")
                    return False
            else:
                print(f"⚠️  {filepath}: External file {external_file} not found")
                return True
        else:
            print(f"ℹ️  {filepath}: Not a recognized data file")
            return True
            
    except Exception as e:
        print(f"❌ {filepath}: Error - {e}")
        return False

def main():
    """Restore embedded data in all HTML files"""
    
    print("🔧 Restoring embedded JavaScript data in HTML files...")
    print("=" * 50)
    
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    
    if not html_files:
        print("No HTML files found")
        return
    
    success_count = 0
    total_additions = 0
    
    for html_file in sorted(html_files):
        original_size = os.path.getsize(html_file) if os.path.exists(html_file) else 0
        
        if restore_embedded_data_in_file(html_file):
            success_count += 1
            new_size = os.path.getsize(html_file)
            total_additions += (new_size - original_size)
    
    print("=" * 50)
    print(f"Processed {success_count}/{len(html_files)} files successfully")
    print(f"📈 Total data added: {total_additions/1024:.1f} KB")
    print("✅ Embedded data restored - files ready for WordPress")

if __name__ == "__main__":
    main() 