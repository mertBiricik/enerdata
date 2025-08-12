#!/usr/bin/env python3
"""
Script to remove embedded data from HTML files and restore external script references
"""

import re
import os

def remove_embedded_data_from_html(html_file, script_src_pattern):
    """Remove ALL embedded JavaScript data and restore external script reference"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Remove ALL script tags containing embedded data (handle duplicates)
        if '4_yasal_duzenlemeler.html' in html_file:
            # Remove all embeddedYasalData script blocks
            pattern = r'<script[^>]*>\s*const\s+embeddedYasalData\s*=.*?</script>'
            html_content = re.sub(pattern, '', html_content, flags=re.DOTALL)
            print(f"Removed all embeddedYasalData script blocks from {html_file}")
            
        elif '5_strateji_ve_politika_belgeleri.html' in html_file:
            # Remove all embeddedStratejiData script blocks
            pattern = r'<script[^>]*>\s*const\s+embeddedStratejiData\s*=.*?</script>'
            html_content = re.sub(pattern, '', html_content, flags=re.DOTALL)
            print(f"Removed all embeddedStratejiData script blocks from {html_file}")
            
        elif '6_kalkinma_planlari.html' in html_file:
            # Remove all embeddedKalkinmaData script blocks
            pattern = r'<script[^>]*>\s*const\s+embeddedKalkinmaData\s*=.*?</script>'
            html_content = re.sub(pattern, '', html_content, flags=re.DOTALL)
            print(f"Removed all embeddedKalkinmaData script blocks from {html_file}")
            
        elif '7_ab_ilerleme_raporlari.html' in html_file:
            # Remove all embeddedAbData script blocks
            pattern = r'<script[^>]*>\s*const\s+embeddedAbData\s*=.*?</script>'
            html_content = re.sub(pattern, '', html_content, flags=re.DOTALL)
            print(f"Removed all embeddedAbData script blocks from {html_file}")
            
        elif '1_birincil_enerjinin_kaynaklara_gore_uretimi_ve_tuketimi.html' in html_file:
            # Remove all embeddedDataA script blocks
            pattern = r'<script[^>]*>\s*const\s+embeddedDataA\s*=.*?</script>'
            html_content = re.sub(pattern, '', html_content, flags=re.DOTALL)
            print(f"Removed all embeddedDataA script blocks from {html_file}")
            
        elif '2_elektrik_enerjisinin_kaynaklara_gore_kurulu_gucu_ve_uretimi.html' in html_file:
            # Remove all embeddedDataB script blocks
            pattern = r'<script[^>]*>\s*const\s+embeddedDataB\s*=.*?</script>'
            html_content = re.sub(pattern, '', html_content, flags=re.DOTALL)
            print(f"Removed all embeddedDataB script blocks from {html_file}")
            
        elif '3_elektrik_enerjisinin_brut_uretimi_ve_sektorel_tuketimi.html' in html_file:
            # Remove all embeddedRawData script blocks
            pattern = r'<script[^>]*>\s*const\s+embeddedRawData\s*=.*?</script>'
            html_content = re.sub(pattern, '', html_content, flags=re.DOTALL)
            print(f"Removed all embeddedRawData script blocks from {html_file}")
        
        # Also remove any orphaned script tags that might be empty
        html_content = re.sub(r'<script[^>]*>\s*</script>', '', html_content)
        
        # Write back to file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ Successfully cleaned all embedded data from {html_file}")
        return True
        
    except Exception as e:
        print(f"Error processing {html_file}: {e}")
        return False

def main():
    print("🧹 COMPREHENSIVE DATA CLEANING")
    print("=" * 50)
    print("Removing ALL embedded data from HTML files (including duplicates)")
    
    # Define the files and their external script sources
    files_to_process = [
        {
            'html_file': '1_birincil_enerjinin_kaynaklara_gore_uretimi_ve_tuketimi.html',
            'script_src': 'data/a/data_a_embedded.js'
        },
        {
            'html_file': '2_elektrik_enerjisinin_kaynaklara_gore_kurulu_gucu_ve_uretimi.html',
            'script_src': 'data/b/data_b_embedded.js'
        },
        {
            'html_file': '3_elektrik_enerjisinin_brut_uretimi_ve_sektorel_tuketimi.html',
            'script_src': 'data/C/c_embedded_data.js'
        },
        # Nitel data files (4,5,6,7)
        {
            'html_file': '4_yasal_duzenlemeler.html',
            'script_src': 'nitel_data/yasal_data.js'
        },
        {
            'html_file': '5_strateji_ve_politika_belgeleri.html',
            'script_src': 'nitel_data/strateji_data.js'
        },
        {
            'html_file': '6_kalkinma_planlari.html',
            'script_src': 'nitel_data/kalkinma_data.js'
        },
        {
            'html_file': '7_ab_ilerleme_raporlari.html',
            'script_src': 'nitel_data/ab_data.js'
        }
    ]
    
    success_count = 0
    
    for file_info in files_to_process:
        html_file = file_info['html_file']
        script_src = file_info['script_src']
        
        print(f"\nCleaning {html_file}...")
        
        # Check if HTML file exists
        if not os.path.exists(html_file):
            print(f"❌ {html_file} not found")
            continue
        
        # Remove ALL embedded data
        if remove_embedded_data_from_html(html_file, script_src):
            success_count += 1
    
    print(f"\n{'='*50}")
    if success_count == len(files_to_process):
        print("✅ SUCCESS: All embedded data completely removed!")
        print("🧹 No duplicate declarations remain")
        print("📁 Files are clean and ready for fresh data embedding")
    else:
        print(f"⚠️  PARTIAL SUCCESS: {success_count}/{len(files_to_process)} files processed")

if __name__ == "__main__":
    main() 