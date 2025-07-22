#!/usr/bin/env python3
"""
High-Quality Logo Embedding Script for Energy Dashboard

This script embeds logos with higher quality sizing and better positioning
for professional chart exports.

Usage:
    python embed_logo_hq.py --logo logo.jpg --all
    python embed_logo_hq.py --size 120 --logo logo.jpg --all  # Custom size
"""

import os
import sys
import argparse
import base64
import re
from pathlib import Path

class HighQualityLogoEmbedder:
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
                # Check if it's a JPEG
                if f.read(2) == b'\xff\xd8':
                    f.seek(0)
                    while True:
                        chunk = f.read(2)
                        if not chunk or chunk == b'\xff\xd9':
                            break
                        if chunk[0] == 0xff and chunk[1] in [0xc0, 0xc2]:
                            f.read(3)
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
                    f.seek(16)
                    width = int.from_bytes(f.read(4), 'big')
                    height = int.from_bytes(f.read(4), 'big')
                    return width, height
                    
                return 300, 200  # Default
                
        except Exception as e:
            print(f"⚠️  Could not determine image dimensions: {e}")
            return 300, 200
    
    def image_to_base64(self, image_path):
        """Convert image file to base64 data URI"""
        try:
            with open(image_path, 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            
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
            return f"data:{mime_type};base64,{encoded_string}"
            
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
    
    def create_high_quality_logo_code(self, logo_width, logo_height, max_logo_size=120):
        """Generate high-quality logo drawing code with better positioning and sizing"""
        
        aspect_ratio = logo_width / logo_height
        
        # Create improved logo code with higher quality and better positioning
        hq_logo_code = f"""
            logo.onload = function() {{
                // High-quality logo rendering with preserved aspect ratio
                const maxLogoSize = {max_logo_size};
                const logoAspectRatio = {aspect_ratio:.3f};
                const logoMargin = 25; // Increased margin for better positioning
                
                let logoWidth, logoHeight;
                if (logoAspectRatio > 1) {{
                    // Wide logo (landscape)
                    logoWidth = maxLogoSize;
                    logoHeight = maxLogoSize / logoAspectRatio;
                }} else {{
                    // Tall logo (portrait)
                    logoHeight = maxLogoSize;
                    logoWidth = maxLogoSize * logoAspectRatio;
                }}
                
                // Enable high-quality rendering
                ctx.imageSmoothingEnabled = true;
                ctx.imageSmoothingQuality = 'high';
                
                // Calculate position (top-right with better spacing)
                const logoX = width - logoWidth - logoMargin;
                const logoY = logoMargin;
                
                // Draw logo with high quality
                ctx.drawImage(logo, logoX, logoY, logoWidth, logoHeight);
                
                // Optional: Add subtle drop shadow for better visibility
                ctx.shadowColor = 'rgba(0, 0, 0, 0.1)';
                ctx.shadowBlur = 2;
                ctx.shadowOffsetX = 1;
                ctx.shadowOffsetY = 1;
                
                // Reset shadow for subsequent drawing
                ctx.shadowColor = 'transparent';
                ctx.shadowBlur = 0;
                ctx.shadowOffsetX = 0;
                ctx.shadowOffsetY = 0;
                
                // Continue with rest of the drawing
                drawChartContent();
            }};"""
        
        return hq_logo_code
    
    def update_logo_code(self, content, logo_width, logo_height, max_logo_size=120):
        """Replace existing logo code with high-quality version"""
        
        # Generate the new high-quality code
        hq_code = self.create_high_quality_logo_code(logo_width, logo_height, max_logo_size)
        
        # Pattern to match existing logo.onload function
        # This matches both old square versions and aspect-fixed versions
        pattern = r"logo\.onload\s*=\s*function\(\)\s*\{[\s\S]*?drawChartContent\(\);[\s\S]*?\};"
        
        # Replace with high-quality version
        modified_content, count = re.subn(pattern, hq_code.strip() + ";", content, flags=re.MULTILINE)
        
        return modified_content, count
    
    def embed_logo_references(self, content, logo_data_uri):
        """Replace external logo file references with embedded data URI"""
        logo_src_pattern = r"logo\.src\s*=\s*['\"][^'\"]*['\"]"
        modified_content = re.sub(logo_src_pattern, f"logo.src = '{logo_data_uri}'", content)
        return modified_content
    
    def embed_high_quality_logo(self, logo_path, max_logo_size=120, target_files=None):
        """Embed logo with high quality settings"""
        print(f"🔄 Embedding HIGH-QUALITY logo from '{logo_path}' (max size: {max_logo_size}px)...")
        
        # Get logo dimensions
        logo_width, logo_height = self.get_image_dimensions(logo_path)
        aspect_ratio = logo_width / logo_height
        print(f"📐 Logo: {logo_width}x{logo_height} (aspect ratio: {aspect_ratio:.3f})")
        
        # Calculate final dimensions
        if aspect_ratio > 1:
            final_width = max_logo_size
            final_height = max_logo_size / aspect_ratio
        else:
            final_height = max_logo_size
            final_width = max_logo_size * aspect_ratio
        
        print(f"📊 Final render size: {final_width:.0f}x{final_height:.0f}px")
        
        # Convert to base64
        logo_data_uri = self.image_to_base64(logo_path)
        if not logo_data_uri:
            return False
        
        print(f"✅ Logo converted to base64 ({len(logo_data_uri)} characters)")
        
        # Determine files to process
        if target_files:
            files_to_process = target_files
        else:
            files_to_process = self.html_files + self.embedded_files
        
        existing_files = [f for f in files_to_process if os.path.exists(f)]
        if not existing_files:
            print("❌ No target HTML files found")
            return False
        
        success_count = 0
        
        for html_file in existing_files:
            print(f"📄 Processing {html_file}...")
            
            content = self.read_file(html_file)
            if not content:
                continue
            
            # Create backup
            backup_file = f"{html_file}.hq_backup"
            if not os.path.exists(backup_file):
                self.write_file(backup_file, content)
                print(f"   📦 Backup: {backup_file}")
            
            # Embed logo data URI
            modified_content = self.embed_logo_references(content, logo_data_uri)
            logo_embeds = 1 if 'logo.src' in content else 0
            
            # Update with high-quality logo code
            modified_content, code_updates = self.update_logo_code(
                modified_content, logo_width, logo_height, max_logo_size
            )
            
            total_changes = logo_embeds + code_updates
            
            if total_changes > 0:
                if self.write_file(html_file, modified_content):
                    print(f"   ✅ Updated: {logo_embeds} embed(s) + {code_updates} HQ code update(s)")
                    success_count += 1
                else:
                    print(f"   ❌ Failed to write file")
            else:
                print(f"   ⚠️  No logo code found")
        
        if success_count > 0:
            print(f"\n🎉 SUCCESS: Updated {success_count} file(s) with HIGH-QUALITY logo")
            print(f"💾 Backups saved with .hq_backup extension")
            print(f"📊 Logo data URI: {len(logo_data_uri)} characters")
            print(f"📐 Render size: {final_width:.0f}x{final_height:.0f}px (max: {max_logo_size}px)")
            print(f"🎨 Features: High-quality smoothing, drop shadow, better positioning")
            return True
        else:
            print(f"\n❌ FAILED: No files were updated")
            return False
    
    def revert_hq_changes(self, target_files=None):
        """Restore files from HQ backup copies"""
        print("🔄 Reverting high-quality changes...")
        
        if target_files:
            files_to_revert = target_files
        else:
            files_to_revert = self.html_files + self.embedded_files
        
        success_count = 0
        
        for html_file in files_to_revert:
            backup_file = f"{html_file}.hq_backup"
            
            if not os.path.exists(backup_file):
                continue
                
            print(f"📄 Reverting {html_file}...")
            
            backup_content = self.read_file(backup_file)
            if backup_content and self.write_file(html_file, backup_content):
                print(f"   ✅ Restored from backup")
                try:
                    os.remove(backup_file)
                    print(f"   🗑️  Removed backup")
                except:
                    print(f"   ⚠️  Could not remove backup")
                success_count += 1
            else:
                print(f"   ❌ Failed to restore")
        
        if success_count > 0:
            print(f"\n🎉 SUCCESS: Reverted {success_count} file(s)")
        else:
            print(f"\n❌ No files were reverted")
    
    def status(self):
        """Show current logo status with quality indicators"""
        print("📊 High-Quality Logo Status")
        print("=" * 35)
        
        # Check available logos
        logo_candidates = ['logo.jpg', 'logo.jpeg', 'logo.png', 'logo.gif', 'logo.svg']
        available_logos = [f for f in logo_candidates if os.path.exists(f)]
        
        print(f"Available logos: {available_logos if available_logos else 'None'}")
        
        if available_logos:
            for logo_file in available_logos:
                width, height = self.get_image_dimensions(logo_file)
                file_size = os.path.getsize(logo_file) / 1024  # KB
                print(f"  {logo_file}: {width}x{height} ({file_size:.1f}KB)")
        
        # Check HTML files
        all_files = self.html_files + self.embedded_files
        existing_files = [f for f in all_files if os.path.exists(f)]
        
        print(f"\nHTML files: {len(existing_files)}/{len(all_files)}")
        
        for html_file in existing_files:
            hq_backup = os.path.exists(f"{html_file}.hq_backup")
            content = self.read_file(html_file)
            
            if content:
                has_embedded = 'data:image' in content
                has_hq_code = 'imageSmoothingQuality' in content
                has_shadow = 'shadowColor' in content
                has_old_code = 'const logoSize = 60' in content
                
                features = []
                if has_embedded:
                    features.append("embedded")
                if has_hq_code:
                    features.append("HQ smoothing")
                if has_shadow:
                    features.append("drop shadow")
                if has_old_code:
                    features.append("old 60px code")
                if hq_backup:
                    features.append("HQ backup")
                
                status = " | ".join(features) if features else "no logo"
                print(f"  {html_file}: {status}")

def main():
    parser = argparse.ArgumentParser(
        description="High-quality logo embedding for energy dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python embed_logo_hq.py --logo logo.jpg --all
  python embed_logo_hq.py --logo logo.png --size 150 --all
  python embed_logo_hq.py --revert
  python embed_logo_hq.py --status
        """
    )
    
    parser.add_argument('--logo', help='Logo image file to embed')
    parser.add_argument('--size', type=int, default=120, help='Maximum logo size in pixels (default: 120)')
    parser.add_argument('--files', nargs='+', help='Specific HTML files to process')
    parser.add_argument('--all', action='store_true', help='Process all dashboard files')
    parser.add_argument('--revert', action='store_true', help='Restore from HQ backups')
    parser.add_argument('--status', action='store_true', help='Show current status')
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    embedder = HighQualityLogoEmbedder()
    
    if args.status:
        embedder.status()
    elif args.revert:
        embedder.revert_hq_changes(args.files)
    elif args.logo:
        if args.all:
            embedder.embed_high_quality_logo(args.logo, args.size)
        elif args.files:
            embedder.embed_high_quality_logo(args.logo, args.size, args.files)
        else:
            print("❌ Error: Specify --all or --files with --logo")
    else:
        print("❌ Error: Specify --logo, --revert, or --status")

if __name__ == "__main__":
    main() 