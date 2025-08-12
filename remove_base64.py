#!/usr/bin/env python3
"""
Remove Base64 Logo Data - Safety Script
Removes embedded base64 logo data from HTML files to prevent LLM context crashes.
Replaces with placeholder for safe editing.
"""

import os
import re

def remove_base64_from_file(filepath):
    """Remove base64 logo data from a single HTML file"""
    if not os.path.exists(filepath):
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match base64 image data
        base64_pattern = r'data:image/[^;]+;base64,[A-Za-z0-9+/=]+'
        
        # Count matches before removal
        matches = re.findall(base64_pattern, content)
        
        if matches:
            # Replace with placeholder
            content = re.sub(base64_pattern, 'LOGO_BASE64_PLACEHOLDER', content)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {filepath}: Removed {len(matches)} base64 logo(s)")
            return True
        else:
            print(f"ℹ️  {filepath}: No base64 data found")
            return True
            
    except Exception as e:
        print(f"❌ {filepath}: Error - {e}")
        return False

def main():
    """Remove base64 data from all HTML files"""
    
    print("🔧 Removing base64 logo data from HTML files...")
    print("=" * 50)
    
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    
    if not html_files:
        print("No HTML files found")
        return
    
    success_count = 0
    for html_file in sorted(html_files):
        if remove_base64_from_file(html_file):
            success_count += 1
    
    print("=" * 50)
    print(f"Processed {success_count}/{len(html_files)} files successfully")
    print("✅ HTML files are now safe for LLM editing")

if __name__ == "__main__":
    main() 