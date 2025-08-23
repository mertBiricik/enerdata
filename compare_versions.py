#!/usr/bin/env python3
"""
Compare previous vs current versions by taking screenshots
"""

import os
import subprocess
import tempfile
import shutil
from screenshot_analyzer import setup_firefox_driver, start_local_server, take_screenshot
import time
from PIL import Image, ImageDraw, ImageFont
import json

def checkout_previous_version():
    """Checkout previous commit and return temp directory"""
    try:
        # Create temp directory for previous version
        temp_dir = tempfile.mkdtemp(prefix='enerdata_previous_')
        
        # Get the previous commit hash
        result = subprocess.run(['git', 'show', '6a66e39:4_yasal_duzenlemeler.html'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            # Write previous version files
            for file_num in range(4, 8):
                html_file = None
                if file_num == 4:
                    html_file = '4_yasal_duzenlemeler.html'
                elif file_num == 5:
                    html_file = '5_strateji_ve_politika_belgeleri.html'
                elif file_num == 6:
                    html_file = '6_kalkinma_planlari.html'
                elif file_num == 7:
                    html_file = '7_ab_ilerleme_raporlari.html'
                
                if html_file:
                    result = subprocess.run(['git', 'show', f'6a66e39:{html_file}'], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        with open(os.path.join(temp_dir, html_file), 'w', encoding='utf-8') as f:
                            f.write(result.stdout)
            
            return temp_dir
        else:
            shutil.rmtree(temp_dir)
            return None
            
    except Exception as e:
        print(f"Error checking out previous version: {e}")
        return None

def take_comparison_screenshots():
    """Take screenshots of both versions and compare"""
    
    print("=== VISUAL COMPARISON: PREVIOUS vs CURRENT ===\n")
    
    # HTML files to compare
    html_files = [
        ('4_yasal_duzenlemeler.html', 'Legal Regulations'),
        ('5_strateji_ve_politika_belgeleri.html', 'Strategy & Policy Documents'),
        ('6_kalkinma_planlari.html', 'Development Plans'),
        ('7_ab_ilerleme_raporlari.html', 'EU Progress Reports')
    ]
    
    # Checkout previous version
    temp_dir = checkout_previous_version()
    if not temp_dir:
        print("Failed to checkout previous version")
        return
    
    try:
        # Setup drivers and servers
        driver = setup_firefox_driver()
        if not driver:
            print("Failed to setup driver")
            return
        
        # Start server for current version
        current_server = start_local_server()
        time.sleep(2)
        
        # Start server for previous version on different port
        prev_server = None
        try:
            os.chdir(temp_dir)
            prev_server = subprocess.Popen(['python3', '-m', 'http.server', '8001'], 
                                         stdout=subprocess.DEVNULL, 
                                         stderr=subprocess.DEVNULL)
            time.sleep(2)
            os.chdir('..')  # Go back to original directory
        except Exception as e:
            print(f"Error starting previous version server: {e}")
        
        comparisons = []
        
        for html_file, description in html_files:
            print(f"\n--- {description} ---")
            
            # Take screenshot of current version
            current_url = f"http://localhost:8000/{html_file}"
            current_screenshot = f"current_{html_file.replace('.html', '.png')}"
            current_success = take_screenshot(driver, current_url, current_screenshot, '.document-card')
            
            # Take screenshot of previous version
            prev_url = f"http://localhost:8001/{html_file}"
            prev_screenshot = f"previous_{html_file.replace('.html', '.png')}"
            prev_success = take_screenshot(driver, prev_url, prev_screenshot, '.document-card')
            
            if current_success and prev_success:
                comparison = analyze_visual_differences(prev_screenshot, current_screenshot, description)
                comparisons.append(comparison)
                print(comparison)
            else:
                print(f"Failed to capture screenshots for {description}")
        
        # Create summary
        create_comparison_summary(comparisons)
        
    finally:
        # Cleanup
        if 'driver' in locals():
            driver.quit()
        if current_server:
            current_server.terminate()
        if prev_server:
            prev_server.terminate()
        if temp_dir:
            shutil.rmtree(temp_dir)

def analyze_visual_differences(prev_file, current_file, description):
    """Analyze visual differences between two screenshots"""
    
    try:
        prev_img = Image.open(prev_file)
        current_img = Image.open(current_file)
        
        prev_size = os.path.getsize(prev_file)
        current_size = os.path.getsize(current_file)
        
        # Calculate file size difference
        size_diff = current_size - prev_size
        size_change = (size_diff / prev_size) * 100 if prev_size > 0 else 0
        
        analysis = f"""
{description}:
  Previous: {prev_img.size[0]}x{prev_img.size[1]}, {prev_size:,} bytes
  Current:  {current_img.size[0]}x{current_img.size[1]}, {current_size:,} bytes
  Change:   {size_change:+.1f}% file size ({size_diff:+,} bytes)
"""
        
        # Try to detect visual differences (basic comparison)
        if prev_img.size == current_img.size:
            # Convert to same mode for comparison
            if prev_img.mode != current_img.mode:
                prev_img = prev_img.convert('RGBA')
                current_img = current_img.convert('RGBA')
            
            # Simple pixel comparison
            diff_pixels = 0
            total_pixels = prev_img.size[0] * prev_img.size[1]
            
            # Sample pixels for performance (every 10th pixel)
            for y in range(0, prev_img.size[1], 10):
                for x in range(0, prev_img.size[0], 10):
                    if prev_img.getpixel((x, y)) != current_img.getpixel((x, y)):
                        diff_pixels += 1
            
            diff_percentage = (diff_pixels * 100 / (total_pixels / 100)) if total_pixels > 0 else 0
            analysis += f"  Visual:   ~{diff_percentage:.1f}% pixels changed (sampled)"
        else:
            analysis += f"  Visual:   Different dimensions - significant layout changes"
        
        return analysis
        
    except Exception as e:
        return f"{description}: Error analyzing - {e}"

def create_comparison_summary(comparisons):
    """Create a comprehensive comparison summary"""
    
    print("\n" + "="*80)
    print("COMPREHENSIVE VISUAL COMPARISON SUMMARY")
    print("="*80)
    
    print("""
KEY CHANGES DETECTED:
""")
    
    for comparison in comparisons:
        print(comparison)
    
    print("""
EXPECTED IMPROVEMENTS IN CURRENT VERSION:
1. ALL Excel columns now visible (previously many were hidden)
2. Exact Excel column headers displayed (vs simplified names)
3. More comprehensive document metadata shown
4. Export downloads original Excel files (vs generated CSV)

AESTHETIC IMPACT:
- More information-dense layout
- Professional appearance matching Excel structure
- Complete data transparency
- Enhanced user experience with full data access
""")
    
    # List all screenshot files created
    print("\nSCREENSHOT FILES CREATED:")
    for i in range(4, 8):
        current_file = f"current_{i}_*.png"
        prev_file = f"previous_{i}_*.png"
        
        # Find actual filenames
        import glob
        current_files = glob.glob(f"current_{i}_*.png")
        prev_files = glob.glob(f"previous_{i}_*.png")
        
        if current_files:
            print(f"  Current File {i}: {current_files[0]}")
        if prev_files:
            print(f"  Previous File {i}: {prev_files[0]}")

if __name__ == "__main__":
    os.chdir('/home/ottobeeth/courses/enerdata')
    take_comparison_screenshots()