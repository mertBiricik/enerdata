#!/usr/bin/env python3
"""
HTML Data Manager for Energy Dashboard

This script manages embedding and extracting data from HTML files for WordPress deployment.

Usage:
    python html_data_manager.py embed    # Embed external JS data into HTML files
    python html_data_manager.py revert   # Extract embedded data back to external JS files
"""

import os
import re
import sys
import argparse
from pathlib import Path

class HTMLDataManager:
    def __init__(self):
        self.html_files = [
            'dataset_a_primary_energy.html',
            'dataset_b_electricity.html', 
            'dataset_c_sectoral_consumption.html'
        ]
        
        self.data_mappings = {
            'dataset_a_primary_energy.html': {
                'js_file': 'data/a/data_a_embedded.js',
                'variable_name': 'embeddedDataA'
            },
            'dataset_b_electricity.html': {
                'js_file': 'data/b/data_b_embedded.js',
                'variable_name': 'embeddedDataB'
            },
            'dataset_c_sectoral_consumption.html': {
                'js_file': 'data/C/c_embedded_data.js',
                'variable_name': 'embeddedRawData'
            }
        }
        
        # WordPress-safe CSS that won't be overridden
        self.wordpress_safe_styles = """
        /* WordPress-safe styling overrides */
        .energy-dashboard-container * {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            box-sizing: border-box !important;
        }
        
        .energy-dashboard-container {
            margin: 0 !important;
            padding: 20px !important;
            background: white !important;
            color: #333 !important;
            line-height: 1.6 !important;
            font-size: 14px !important;
        }
        
        .energy-dashboard-container .main-container {
            max-width: 1400px !important;
            margin: 0 auto !important;
            background: white !important;
            border-radius: 12px !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1) !important;
            overflow: hidden !important;
        }
        
        .energy-dashboard-container .header {
            background: linear-gradient(135deg, #006400 0%, #228B22 100%) !important;
            color: white !important;
            padding: 2rem !important;
            text-align: center !important;
        }
        
        .energy-dashboard-container .header h1 {
            margin: 0 !important;
            font-size: 2.2rem !important;
            font-weight: 600 !important;
            color: white !important;
        }
        
        .energy-dashboard-container .header p {
            margin: 0.5rem 0 0 0 !important;
            opacity: 0.9 !important;
            font-size: 1.1rem !important;
            color: white !important;
        }
        
        .energy-dashboard-container button {
            background: #006400 !important;
            color: white !important;
            border: none !important;
            border-radius: 6px !important;
            cursor: pointer !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            transition: all 0.3s ease !important;
        }
        
        .energy-dashboard-container button:hover {
            background: #004d00 !important;
            transform: translateY(-1px) !important;
        }
        
        .energy-dashboard-container input, 
        .energy-dashboard-container select {
            border: 1px solid #ddd !important;
            border-radius: 6px !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        }
        
        .energy-dashboard-container canvas {
            max-width: 100% !important;
            height: auto !important;
        }
        
        .energy-dashboard-container .tab-button {
            background: none !important;
            color: #666 !important;
            border: none !important;
            border-bottom: 3px solid transparent !important;
            padding: 1rem 1.5rem !important;
            font-size: 1rem !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
        }
        
        .energy-dashboard-container .tab-button:hover {
            color: #006400 !important;
            background: #f8f9fa !important;
            transform: none !important;
        }
        
        .energy-dashboard-container .tab-button.active {
            color: #006400 !important;
            border-bottom-color: #006400 !important;
            background: #f8f9fa !important;
            transform: none !important;
        }
        """

    def read_file(self, filepath):
        """Read file content with UTF-8 encoding"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return None

    def write_file(self, filepath, content):
        """Write file content with UTF-8 encoding"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return False

    def extract_js_data(self, js_filepath):
        """Extract JavaScript data from external file"""
        content = self.read_file(js_filepath)
        if not content:
            return None
        
        # Remove any comments and clean up
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            # Remove single-line comments but preserve data
            if line.strip() and not line.strip().startswith('//'):
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)

    def embed_data(self):
        """Embed external JS data into HTML files for WordPress"""
        print("🚀 Embedding data into HTML files for WordPress deployment...")
        
        for html_file in self.html_files:
            if not os.path.exists(html_file):
                print(f"❌ HTML file not found: {html_file}")
                continue
                
            mapping = self.data_mappings[html_file]
            js_file = mapping['js_file']
            
            if not os.path.exists(js_file):
                print(f"❌ JS file not found: {js_file}")
                continue
            
            print(f"📄 Processing {html_file}...")
            
            # Read HTML content
            html_content = self.read_file(html_file)
            if not html_content:
                continue
            
            # Read JS data
            js_data = self.extract_js_data(js_file)
            if not js_data:
                continue
            
            # Add WordPress-safe container wrapper
            html_content = html_content.replace(
                '<div class="main-container">',
                '<div class="energy-dashboard-container"><div class="main-container">'
            )
            html_content = html_content.replace(
                '</body>',
                '</div></body>'
            )
            
            # Add WordPress-safe styles to head
            style_insertion_point = '</title>'
            if style_insertion_point in html_content:
                html_content = html_content.replace(
                    style_insertion_point,
                    f'{style_insertion_point}\n    <style>{self.wordpress_safe_styles}</style>'
                )
            
            # Find and replace the script src with embedded data
            script_pattern = f'<script src="{js_file}"></script>'
            embedded_script = f'<script>\n{js_data}\n    </script>'
            
            if script_pattern in html_content:
                html_content = html_content.replace(script_pattern, embedded_script)
                
                # Create backup
                backup_file = f"{html_file}.backup"
                self.write_file(backup_file, self.read_file(html_file))
                
                # Write embedded version
                embedded_file = f"{html_file.replace('.html', '_embedded.html')}"
                if self.write_file(embedded_file, html_content):
                    print(f"✅ Created embedded version: {embedded_file}")
                    print(f"📦 Backup saved as: {backup_file}")
                else:
                    print(f"❌ Failed to create embedded version")
            else:
                print(f"⚠️  Script tag not found in {html_file}")
        
        print("\n🎉 Embedding complete! You can now upload the *_embedded.html files to WordPress.")
        print("💡 Use the embedded files in WordPress Custom HTML blocks.")

    def revert_data(self):
        """Revert embedded HTML files back to external JS structure"""
        print("🔄 Reverting embedded HTML files to external JS structure...")
        
        for html_file in self.html_files:
            embedded_file = f"{html_file.replace('.html', '_embedded.html')}"
            backup_file = f"{html_file}.backup"
            
            if not os.path.exists(embedded_file):
                print(f"⚠️  Embedded file not found: {embedded_file}")
                continue
            
            if not os.path.exists(backup_file):
                print(f"⚠️  Backup file not found: {backup_file}")
                continue
            
            print(f"📄 Reverting {embedded_file}...")
            
            # Restore from backup
            backup_content = self.read_file(backup_file)
            if backup_content and self.write_file(html_file, backup_content):
                print(f"✅ Restored {html_file} from backup")
                
                # Clean up files
                try:
                    os.remove(embedded_file)
                    os.remove(backup_file)
                    print(f"🗑️  Cleaned up {embedded_file} and {backup_file}")
                except Exception as e:
                    print(f"⚠️  Could not remove files: {e}")
            else:
                print(f"❌ Failed to restore {html_file}")
        
        print("\n🎉 Revert complete! Files are back to their original structure.")

    def status(self):
        """Show current status of files"""
        print("📊 File Status:")
        print("=" * 50)
        
        for html_file in self.html_files:
            embedded_file = f"{html_file.replace('.html', '_embedded.html')}"
            backup_file = f"{html_file}.backup"
            
            print(f"\n📄 {html_file}")
            print(f"   Original: {'✅' if os.path.exists(html_file) else '❌'}")
            print(f"   Embedded: {'✅' if os.path.exists(embedded_file) else '❌'}")
            print(f"   Backup:   {'✅' if os.path.exists(backup_file) else '❌'}")
            
            # Check data file
            mapping = self.data_mappings[html_file]
            js_file = mapping['js_file']
            print(f"   Data JS:  {'✅' if os.path.exists(js_file) else '❌'} ({js_file})")

def main():
    parser = argparse.ArgumentParser(
        description="Manage HTML data embedding for WordPress deployment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python html_data_manager.py embed    # Create WordPress-ready embedded files
  python html_data_manager.py revert   # Restore original structure
  python html_data_manager.py status   # Show current file status
        """
    )
    
    parser.add_argument(
        'action',
        choices=['embed', 'revert', 'status'],
        help='Action to perform'
    )
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    manager = HTMLDataManager()
    
    if args.action == 'embed':
        manager.embed_data()
    elif args.action == 'revert':
        manager.revert_data()
    elif args.action == 'status':
        manager.status()

if __name__ == "__main__":
    main() 