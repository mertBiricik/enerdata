#!/usr/bin/env python3
"""
Logo Embedding Script for Energy Dashboard

This script embeds logo images directly into HTML files as base64 data URIs,
eliminating the need for external logo files in chart export functions.

Usage:
    python embed_logo.py --logo logo.jpg --files dataset_a_primary_energy.html dataset_b_electricity.html dataset_c_sectoral_consumption.html
    python embed_logo.py --logo logo.png --all  # Process all dashboard HTML files
    python embed_logo.py --revert               # Restore external logo references
"""

import os
import sys
import argparse
import base64
import re
from pathlib import Path

class LogoEmbedder:
    def __init__(self):
        self.html_files = [
            'dataset_a_primary_energy.html',
            'dataset_b_electricity.html', 
            'dataset_c_sectoral_consumption.html',
            'veri_bankasi.html'
        ]
        
        self.embedded_files = [
            'dataset_a_primary_energy_embedded.html',
            'dataset_b_electricity_embedded.html', 
            'dataset_c_sectoral_consumption_embedded.html'
        ]
        
        # Common logo file patterns to look for
        self.logo_patterns = [
            r"logo\.src\s*=\s*['\"]([^'\"]+)['\"]",
            r"<img[^>]*src\s*=\s*['\"]([^'\"]*logo[^'\"]*)['\"]",
        ]
        
    def image_to_base64(self, image_path):
        """Convert image file to base64 data URI"""
        try:
            with open(image_path, 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Determine MIME type from file extension
            ext = Path(image_path).suffix.lower()
            mime_types = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg', 
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.svg': 'image/svg+xml',
                '.bmp': 'image/bmp',
                '.webp': 'image/webp'
            }
            
            mime_type = mime_types.get(ext, 'image/jpeg')
            data_uri = f"data:{mime_type};base64,{encoded_string}"
            
            return data_uri
            
        except FileNotFoundError:
            print(f"❌ Error: Logo file '{image_path}' not found")
            return None
        except Exception as e:
            print(f"❌ Error converting {image_path} to base64: {e}")
            return None
    
    def read_file(self, filepath):
        """Read file content with UTF-8 encoding"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"❌ Error reading {filepath}: {e}")
            return None
    
    def write_file(self, filepath, content):
        """Write file content with UTF-8 encoding"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"❌ Error writing {filepath}: {e}")
            return False
    
    def find_logo_references(self, content):
        """Find all logo file references in HTML content"""
        references = []
        
        for pattern in self.logo_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                references.append({
                    'full_match': match.group(0),
                    'logo_path': match.group(1),
                    'start': match.start(),
                    'end': match.end()
                })
        
        return references
    
    def embed_logo_in_content(self, content, logo_data_uri):
        """Replace logo file references with embedded data URI"""
        modified_content = content
        replacements_made = 0
        
        # Replace logo.src = 'logo.jpg' patterns
        logo_src_pattern = r"logo\.src\s*=\s*['\"]([^'\"]+)['\"]"
        def replace_logo_src(match):
            return f"logo.src = '{logo_data_uri}'"
        
        modified_content, count = re.subn(logo_src_pattern, replace_logo_src, modified_content, flags=re.IGNORECASE)
        replacements_made += count
        
        # Replace img src with logo in filename
        img_logo_pattern = r"(<img[^>]*src\s*=\s*['\"])([^'\"]*logo[^'\"]*)['\"]"
        def replace_img_logo(match):
            return f"{match.group(1)}{logo_data_uri}\""
        
        modified_content, count = re.subn(img_logo_pattern, replace_img_logo, modified_content, flags=re.IGNORECASE)
        replacements_made += count
        
        return modified_content, replacements_made
    
    def embed_logo(self, logo_path, target_files=None):
        """Embed logo into specified HTML files"""
        print(f"🔄 Embedding logo from '{logo_path}' into HTML files...")
        
        # Convert logo to base64
        logo_data_uri = self.image_to_base64(logo_path)
        if not logo_data_uri:
            return False
        
        print(f"✅ Logo converted to base64 data URI ({len(logo_data_uri)} characters)")
        
        # Determine which files to process
        if target_files:
            files_to_process = target_files
        else:
            files_to_process = self.html_files + self.embedded_files
        
        # Filter to only existing files
        existing_files = [f for f in files_to_process if os.path.exists(f)]
        if not existing_files:
            print("❌ No target HTML files found")
            return False
        
        success_count = 0
        
        for html_file in existing_files:
            print(f"📄 Processing {html_file}...")
            
            # Read current content
            content = self.read_file(html_file)
            if not content:
                continue
            
            # Find existing logo references
            references = self.find_logo_references(content)
            if not references:
                print(f"⚠️  No logo references found in {html_file}")
                continue
            
            print(f"   Found {len(references)} logo reference(s)")
            
            # Create backup
            backup_file = f"{html_file}.logo_backup"
            if not os.path.exists(backup_file):
                self.write_file(backup_file, content)
                print(f"   📦 Backup created: {backup_file}")
            
            # Embed logo
            modified_content, replacements = self.embed_logo_in_content(content, logo_data_uri)
            
            if replacements > 0:
                if self.write_file(html_file, modified_content):
                    print(f"   ✅ Embedded logo with {replacements} replacement(s)")
                    success_count += 1
                else:
                    print(f"   ❌ Failed to write updated file")
            else:
                print(f"   ⚠️  No replacements made")
        
        if success_count > 0:
            print(f"\n🎉 SUCCESS: Logo embedded in {success_count} file(s)")
            print(f"💾 Backups saved with .logo_backup extension")
            print(f"📊 Logo data URI size: {len(logo_data_uri)} characters")
            return True
        else:
            print(f"\n❌ FAILED: No files were successfully updated")
            return False
    
    def revert_logo_embedding(self, target_files=None):
        """Restore files from logo backup copies"""
        print("🔄 Reverting logo embedding from backups...")
        
        if target_files:
            files_to_revert = target_files
        else:
            files_to_revert = self.html_files + self.embedded_files
        
        success_count = 0
        
        for html_file in files_to_revert:
            backup_file = f"{html_file}.logo_backup"
            
            if not os.path.exists(backup_file):
                continue
                
            print(f"📄 Reverting {html_file}...")
            
            # Restore from backup
            backup_content = self.read_file(backup_file)
            if backup_content and self.write_file(html_file, backup_content):
                print(f"   ✅ Restored from {backup_file}")
                
                # Remove backup file
                try:
                    os.remove(backup_file)
                    print(f"   🗑️  Removed backup file")
                except:
                    print(f"   ⚠️  Could not remove backup file")
                
                success_count += 1
            else:
                print(f"   ❌ Failed to restore {html_file}")
        
        if success_count > 0:
            print(f"\n🎉 SUCCESS: Reverted {success_count} file(s)")
            return True
        else:
            print(f"\n❌ No files were reverted")
            return False
    
    def status(self):
        """Show current logo embedding status"""
        print("📊 Logo Embedding Status")
        print("=" * 40)
        
        # Check for logo files
        logo_candidates = ['logo.jpg', 'logo.jpeg', 'logo.png', 'logo.gif', 'logo.svg']
        available_logos = [f for f in logo_candidates if os.path.exists(f)]
        
        print(f"Available logo files: {available_logos if available_logos else 'None found'}")
        
        # Check HTML files
        all_files = self.html_files + self.embedded_files
        existing_files = [f for f in all_files if os.path.exists(f)]
        
        print(f"\nHTML files available: {len(existing_files)}/{len(all_files)}")
        
        for html_file in existing_files:
            backup_exists = os.path.exists(f"{html_file}.logo_backup")
            content = self.read_file(html_file)
            
            if content:
                # Check for embedded logos (data URI)
                has_data_uri = 'data:image' in content
                # Check for external logo references
                references = self.find_logo_references(content)
                
                status_parts = []
                if has_data_uri:
                    status_parts.append("embedded logo")
                if references:
                    status_parts.append(f"{len(references)} external ref(s)")
                if backup_exists:
                    status_parts.append("backup exists")
                
                status = " | ".join(status_parts) if status_parts else "no logo found"
                print(f"  {html_file}: {status}")

def main():
    parser = argparse.ArgumentParser(
        description="Embed logo images into HTML files for energy dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python embed_logo.py --logo logo.jpg --all
  python embed_logo.py --logo logo.png --files dataset_a_primary_energy.html 
  python embed_logo.py --revert
  python embed_logo.py --status
        """
    )
    
    parser.add_argument('--logo', help='Path to logo image file to embed')
    parser.add_argument('--files', nargs='+', help='Specific HTML files to process')
    parser.add_argument('--all', action='store_true', help='Process all dashboard HTML files')
    parser.add_argument('--revert', action='store_true', help='Restore from backup files')
    parser.add_argument('--status', action='store_true', help='Show current embedding status')
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    embedder = LogoEmbedder()
    
    if args.status:
        embedder.status()
    elif args.revert:
        embedder.revert_logo_embedding(args.files)
    elif args.logo:
        if args.all:
            embedder.embed_logo(args.logo)
        elif args.files:
            embedder.embed_logo(args.logo, args.files)
        else:
            print("❌ Error: Specify --all or --files when providing --logo")
            parser.print_help()
    else:
        print("❌ Error: Specify --logo, --revert, or --status")
        parser.print_help()

if __name__ == "__main__":
    main() 