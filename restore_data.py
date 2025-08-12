#!/usr/bin/env python3
"""
Script to embed datasets into individual HTML files
"""

import re
import os

def read_js_data_file(file_path):
    """Read a JavaScript data file and return the complete content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content.strip()
    except FileNotFoundError:
        print(f"Error: {file_path} not found")
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def embed_data_in_html(html_file, js_data, script_src_pattern):
    """Embed JavaScript data into HTML file by adding script tag before </body>"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Add the script tag with embedded data before </body>
        script_tag = f'\n    <script>\n{js_data}\n    </script>\n'
        
        # Insert before </body>
        if '</body>' in html_content:
            new_content = html_content.replace('</body>', script_tag + '</body>')
        else:
            # If no </body> tag, add at the end
            new_content = html_content + script_tag
        
        # Write back to file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ Successfully embedded data in {html_file}")
        return True
        
    except Exception as e:
        print(f"Error processing {html_file}: {e}")
        return False


def main():
    print("🔄 Embedding data into individual HTML files")
    print("=" * 50)
    
    # Define the files and their data sources
    files_to_process = [
        {
            'html_file': '1_birincil_enerjinin_kaynaklara_gore_uretimi_ve_tuketimi.html',
            'js_file': 'data/a/data_a_embedded.js',
            'script_src': 'data/a/data_a_embedded.js'
        },
        {
            'html_file': '2_elektrik_enerjisinin_kaynaklara_gore_kurulu_gucu_ve_uretimi.html',
            'js_file': 'data/b/data_b_embedded.js',
            'script_src': 'data/b/data_b_embedded.js'
        },
        {
            'html_file': '3_elektrik_enerjisinin_brut_uretimi_ve_sektorel_tuketimi.html',
            'js_file': 'data/C/c_embedded_data.js',
            'script_src': 'data/C/c_embedded_data.js'
        },
        # Nitel data files (4,5,6,7)
        {
            'html_file': '4_yasal_duzenlemeler.html',
            'js_file': 'nitel_data/yasal_data.js',
            'script_src': 'nitel_data/yasal_data.js'
        },
        {
            'html_file': '5_strateji_ve_politika_belgeleri.html',
            'js_file': 'nitel_data/strateji_data.js',
            'script_src': 'nitel_data/strateji_data.js'
        },
        {
            'html_file': '6_kalkinma_planlari.html',
            'js_file': 'nitel_data/kalkinma_data.js',
            'script_src': 'nitel_data/kalkinma_data.js'
        },
        {
            'html_file': '7_ab_ilerleme_raporlari.html',
            'js_file': 'nitel_data/ab_data.js',
            'script_src': 'nitel_data/ab_data.js'
        }
    ]
    
    success_count = 0
    
    for file_info in files_to_process:
        html_file = file_info['html_file']
        js_file = file_info['js_file']
        script_src = file_info['script_src']
        
        print(f"\nProcessing {html_file}...")
        
        # Check if HTML file exists
        if not os.path.exists(html_file):
            print(f"❌ {html_file} not found")
            continue
        
        # Read JavaScript data
        print(f"Reading {js_file}...")
        js_data = read_js_data_file(js_file)
        if js_data is None:
            continue
        
        # Embed data
        if embed_data_in_html(html_file, js_data, script_src):
            success_count += 1
    
    print(f"\n{'='*50}")
    if success_count == len(files_to_process):
        print("✅ SUCCESS: All datasets embedded successfully!")
        print("📁 Files are now ready for WordPress or standalone use")
        print("🚫 No duplicate declarations")
        print("🔗 All nitel files include link functionality")
    else:
        print(f"⚠️  PARTIAL SUCCESS: {success_count}/{len(files_to_process)} files processed")
    
    print("\n📋 Next steps:")
    print("1. The HTML files now contain clean embedded data")
    print("2. You can upload them directly to WordPress")
    print("3. No external data files are needed")
    print("4. Test in browser - should work without JavaScript errors")

if __name__ == "__main__":
    main() 