#!/usr/bin/env python3
"""
Restore Base64 Logo Data - Safety Script
Restores base64 logo data from logo.jpg file into HTML files.
Replaces LOGO_BASE64_PLACEHOLDER with actual base64 data.
"""

import os
import re
import base64

def get_logo_base64():
    """Get base64 encoded logo from logo.jpg"""
    try:
        with open("logo.jpg", "rb") as f:
            logo_data = base64.b64encode(f.read()).decode()
            return f"data:image/jpeg;base64,{logo_data}"
    except Exception as e:
        print(f"❌ Error reading logo.jpg: {e}")
        return None

def restore_base64_in_file(filepath, logo_base64):
    """Restore base64 logo data in a single HTML file"""
    if not os.path.exists(filepath):
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count placeholder matches
        placeholder_count = len(re.findall(r'LOGO_BASE64_PLACEHOLDER', content))
        
        if placeholder_count > 0:
            # Replace placeholder with actual base64 data
            content = content.replace('LOGO_BASE64_PLACEHOLDER', logo_base64)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {filepath}: Restored {placeholder_count} logo(s)")
            return True
        else:
            print(f"ℹ️  {filepath}: No placeholders found")
            return True
            
    except Exception as e:
        print(f"❌ {filepath}: Error - {e}")
        return False

def main():
    """Restore base64 data in all HTML files"""
    
    print("🔧 Restoring base64 logo data in HTML files...")
    print("=" * 50)
    
    # Get logo base64 data
    logo_base64 = get_logo_base64()
    if not logo_base64:
        print("❌ Cannot proceed without logo.jpg")
        return
    
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    
    if not html_files:
        print("No HTML files found")
        return
    
    success_count = 0
    for html_file in sorted(html_files):
        if restore_base64_in_file(html_file, logo_base64):
            success_count += 1
    
    print("=" * 50)
    print(f"Processed {success_count}/{len(html_files)} files successfully")
    print("✅ Base64 logo data restored")

if __name__ == "__main__":
    main() 