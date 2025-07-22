#!/usr/bin/env python3
"""
Logo Embedding Script with Aspect Ratio Fix for Energy Dashboard

This script embeds logo images as base64 data URIs AND fixes the chart export
functions to preserve the original logo aspect ratio instead of forcing a square.

Usage:
    python embed_logo_aspect_fix.py --logo logo.jpg --all
    python embed_logo_aspect_fix.py --revert
"""

import os
import sys
import argparse
import base64
import re
from pathlib import Path

class LogoEmbedderWithAspectFix:
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
        
    def get_image_dimensions(self, image_path):
        """Get image dimensions without requiring PIL"""
        try:
            with open(image_path, 'rb') as f:
                # Read basic file headers to get dimensions
                # This is a simplified approach for common formats
                
                # Check if it's a JPEG
                if f.read(2) == b'\xff\xd8':
                    f.seek(0)
                    while True:
                        chunk = f.read(2)
                        if not chunk or chunk == b'\xff\xd9':  # End of image
                            break
                        if chunk[0] == 0xff and chunk[1] in [0xc0, 0xc2]:  # SOF markers
                            f.read(3)  # Skip length and precision
                            height = int.from_bytes(f.read(2), 'big')
                            width = int.from_bytes(f.read(2), 'big')
                            return width, height
                        elif chunk[0] == 0xff:
                            length = int.from_bytes(f.read(2), 'big')
                            f.seek(length - 2, 1)
                        else:
                            break
                            
                # Check if it's a PNG
                f.seek(0)
                if f.read(8) == b'\x89PNG\r\n\x1a\n':
                    f.seek(16)  # Skip to IHDR data
                    width = int.from_bytes(f.read(4), 'big')
                    height = int.from_bytes(f.read(4), 'big')
                    return width, height
                    
                # For other formats, return a reasonable default
                return 300, 200  # Default aspect ratio
                
        except Exception as e:
            print(f"⚠️  Could not determine image dimensions: {e}")
            return 300, 200  # Default fallback
    
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
    
    def fix_aspect_ratio_code(self, content, logo_width, logo_height):
        """Update the logo drawing code to preserve aspect ratio"""
        
        # Calculate aspect ratio
        aspect_ratio = logo_width / logo_height
        
        # Generate the improved logo drawing code
        improved_logo_code = f"""
            logo.onload = function() {{
                // Calculate logo dimensions preserving aspect ratio
                const maxLogoSize = 60;
                const logoAspectRatio = {aspect_ratio:.3f};
                
                let logoWidth, logoHeight;
                if (logoAspectRatio > 1) {{
                    // Wide logo
                    logoWidth = maxLogoSize;
                    logoHeight = maxLogoSize / logoAspectRatio;
                }} else {{
                    // Tall logo
                    logoHeight = maxLogoSize;
                    logoWidth = maxLogoSize * logoAspectRatio;
                }}
                
                // Draw logo in top-right corner with preserved aspect ratio
                ctx.drawImage(logo, width - logoWidth - 20, 20, logoWidth, logoHeight);
                
                // Continue with rest of the drawing
                drawChartContent();
            }};"""
        
        # Replace the fixed-size logo drawing code
        old_pattern = r"logo\.onload\s*=\s*function\(\)\s*\{[^}]*?ctx\.drawImage\(logo,\s*width\s*-\s*logoSize\s*-\s*20,\s*20,\s*logoSize,\s*logoSize\);[^}]*?drawChartContent\(\);[^}]*?\};"
        
        # Use a more flexible pattern to match the logo.onload function
        pattern = r"(logo\.onload\s*=\s*function\(\)\s*\{[\s\S]*?)(\s*const\s+logoSize\s*=\s*60;[\s\S]*?ctx\.drawImage\(logo,\s*width\s*-\s*logoSize\s*-\s*20,\s*20,\s*logoSize,\s*logoSize\);[\s\S]*?)(drawChartContent\(\);[\s\S]*?\})"
        
        def replace_logo_function(match):
            return match.group(1) + improved_logo_code.strip() + "\n            "
        
        modified_content, count = re.subn(pattern, replace_logo_function, content, flags=re.MULTILINE | re.DOTALL)
        
        return modified_content, count
    
    def embed_logo_references(self, content, logo_data_uri):
        """Replace external logo file references with embedded data URI"""
        # Replace logo.src assignments
        logo_src_pattern = r"logo\.src\s*=\s*['\"][^'\"]*['\"]"
        modified_content = re.sub(logo_src_pattern, f"logo.src = '{logo_data_uri}'", content)
        
        return modified_content
    
    def embed_logo_with_aspect_fix(self, logo_path, target_files=None):
        """Embed logo and fix aspect ratio in HTML files"""
        print(f"🔄 Embedding logo with aspect ratio fix from '{logo_path}'...")
        
        # Get logo dimensions
        logo_width, logo_height = self.get_image_dimensions(logo_path)
        print(f"📐 Logo dimensions: {logo_width}x{logo_height} (aspect ratio: {logo_width/logo_height:.3f})")
        
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
            
            # Create backup
            backup_file = f"{html_file}.aspect_backup"
            if not os.path.exists(backup_file):
                self.write_file(backup_file, content)
                print(f"   📦 Backup created: {backup_file}")
            
            # Replace logo source with embedded data URI
            modified_content = self.embed_logo_references(content, logo_data_uri)
            logo_replacements = 1 if 'logo.src' in content else 0
            
            # Fix aspect ratio in logo drawing code
            modified_content, aspect_fixes = self.fix_aspect_ratio_code(modified_content, logo_width, logo_height)
            
            total_changes = logo_replacements + aspect_fixes
            
            if total_changes > 0:
                if self.write_file(html_file, modified_content):
                    print(f"   ✅ Updated with {logo_replacements} logo embed(s) + {aspect_fixes} aspect fix(es)")
                    success_count += 1
                else:
                    print(f"   ❌ Failed to write updated file")
            else:
                print(f"   ⚠️  No logo references or drawing code found")
        
        if success_count > 0:
            print(f"\n🎉 SUCCESS: Updated {success_count} file(s) with aspect ratio preserved logo")
            print(f"💾 Backups saved with .aspect_backup extension") 
            print(f"📊 Logo data URI size: {len(logo_data_uri)} characters")
            print(f"📐 Logo will render with correct {logo_width}x{logo_height} aspect ratio")
            return True
        else:
            print(f"\n❌ FAILED: No files were successfully updated")
            return False
    
    def revert_aspect_fixes(self, target_files=None):
        """Restore files from aspect fix backup copies"""
        print("🔄 Reverting aspect ratio fixes from backups...")
        
        if target_files:
            files_to_revert = target_files
        else:
            files_to_revert = self.html_files + self.embedded_files
        
        success_count = 0
        
        for html_file in files_to_revert:
            backup_file = f"{html_file}.aspect_backup"
            
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
        """Show current logo embedding and aspect ratio status"""
        print("📊 Logo Embedding & Aspect Ratio Status")
        print("=" * 45)
        
        # Check for logo files
        logo_candidates = ['logo.jpg', 'logo.jpeg', 'logo.png', 'logo.gif', 'logo.svg']
        available_logos = [f for f in logo_candidates if os.path.exists(f)]
        
        print(f"Available logo files: {available_logos if available_logos else 'None found'}")
        
        if available_logos:
            for logo_file in available_logos:
                width, height = self.get_image_dimensions(logo_file)
                print(f"  {logo_file}: {width}x{height} (aspect ratio: {width/height:.3f})")
        
        # Check HTML files
        all_files = self.html_files + self.embedded_files
        existing_files = [f for f in all_files if os.path.exists(f)]
        
        print(f"\nHTML files available: {len(existing_files)}/{len(all_files)}")
        
        for html_file in existing_files:
            backup_exists = os.path.exists(f"{html_file}.aspect_backup")
            content = self.read_file(html_file)
            
            if content:
                # Check for embedded logos (data URI)
                has_data_uri = 'data:image' in content
                # Check for fixed aspect ratio code
                has_aspect_fix = 'logoAspectRatio' in content
                # Check for old square logo code
                has_square_code = 'const logoSize = 60' in content
                
                status_parts = []
                if has_data_uri:
                    status_parts.append("embedded logo")
                if has_aspect_fix:
                    status_parts.append("aspect ratio fixed")
                elif has_square_code:
                    status_parts.append("square logo (needs fix)")
                if backup_exists:
                    status_parts.append("backup exists")
                
                status = " | ".join(status_parts) if status_parts else "no logo found"
                print(f"  {html_file}: {status}")

def main():
    parser = argparse.ArgumentParser(
        description="Embed logo with aspect ratio preservation for energy dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python embed_logo_aspect_fix.py --logo logo.jpg --all
  python embed_logo_aspect_fix.py --logo logo.png --files dataset_a_primary_energy.html 
  python embed_logo_aspect_fix.py --revert
  python embed_logo_aspect_fix.py --status
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
    embedder = LogoEmbedderWithAspectFix()
    
    if args.status:
        embedder.status()
    elif args.revert:
        embedder.revert_aspect_fixes(args.files)
    elif args.logo:
        if args.all:
            embedder.embed_logo_with_aspect_fix(args.logo)
        elif args.files:
            embedder.embed_logo_with_aspect_fix(args.logo, args.files)
        else:
            print("❌ Error: Specify --all or --files when providing --logo")
            parser.print_help()
    else:
        print("❌ Error: Specify --logo, --revert, or --status")
        parser.print_help()

if __name__ == "__main__":
    main() 