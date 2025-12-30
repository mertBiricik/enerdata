#!/usr/bin/env python3
"""
Screenshot analyzer for chart pages (files 1-3)
"""

import os
from screenshot_analyzer import setup_firefox_driver, start_local_server, take_screenshot, analyze_screenshot

def main():
    html_files = [
        ('1_birincil_enerjinin_kaynaklara_gore_uretimi_ve_tuketimi.html', 'Primary Energy'),
        ('2_elektrik_enerjisinin_kaynaklara_gore kurulu_gucu_ve_uretimi.html', 'Electricity Capacity & Production'),
        ('3_elektrik_enerjisinin_brut_uretimi_ve_sektorel_tuketimi.html', 'Electricity Production & Sectoral Consumption'),
    ]
    
    print("Starting chart pages screenshot analysis...")
    
    server_process = start_local_server()
    if not server_process:
        print("Failed to start local server")
        return
    
    try:
        driver = setup_firefox_driver()
        if not driver:
            print("Failed to setup Firefox driver")
            return
        
        print("\nTaking screenshots of current chart pages...")
        
        for html_file, description in html_files:
            url = f"http://localhost:8000/{html_file}"
            screenshot_file = f"current_{html_file.replace('.html', '').replace(' ', '_')}.png"
            
            print(f"\n=== {description} ===")
            # Use '.main-container' which exists on chart pages
            success = take_screenshot(driver, url, screenshot_file, '.main-container')
            if success:
                analysis = analyze_screenshot(screenshot_file)
                print(analysis)
            else:
                print(f"Failed to screenshot {html_file}")
        
        print("\n" + "="*60)
        print("CHART PAGES SCREENSHOT ANALYSIS SUMMARY")
        print("="*60)
        for html_file, description in html_files:
            screenshot_file = f"current_{html_file.replace('.html', '').replace(' ', '_')}.png"
            if os.path.exists(screenshot_file):
                print(f"✓ {description}: {screenshot_file}")
            else:
                print(f"✗ {description}: screenshot missing")
    finally:
        if 'driver' in locals():
            driver.quit()
        if server_process:
            server_process.terminate()

if __name__ == "__main__":
    main()

