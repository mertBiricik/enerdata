#!/usr/bin/env python3
"""
Screenshot analyzer for HTML pages 4-7
Takes screenshots and analyzes the visual differences
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from PIL import Image
import subprocess

def setup_firefox_driver():
    """Setup Firefox driver with appropriate options"""
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    firefox_options.add_argument('--width=1920')
    firefox_options.add_argument('--height=1080')
    
    try:
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
        return driver
    except Exception as e:
        print(f"Error setting up Firefox driver: {e}")
        return None

def start_local_server():
    """Start a local HTTP server for serving HTML files"""
    try:
        # Kill any existing server on port 8000
        subprocess.run(['pkill', '-f', 'python.*http.server'], stderr=subprocess.DEVNULL)
        time.sleep(1)
        
        # Start new server
        process = subprocess.Popen(['python3', '-m', 'http.server', '8000'], 
                                 stdout=subprocess.DEVNULL, 
                                 stderr=subprocess.DEVNULL)
        time.sleep(2)  # Give server time to start
        return process
    except Exception as e:
        print(f"Error starting server: {e}")
        return None

def take_screenshot(driver, url, filename, wait_selector=None):
    """Take a screenshot of a webpage"""
    try:
        print(f"Loading {url}...")
        driver.get(url)
        
        # Wait for specific element if provided
        if wait_selector:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, wait_selector))
                )
            except:
                print(f"Warning: Could not find selector {wait_selector}, continuing anyway")
        
        # Additional wait for JavaScript to load data
        time.sleep(3)
        
        # Take screenshot
        driver.save_screenshot(filename)
        print(f"Screenshot saved: {filename}")
        return True
        
    except Exception as e:
        print(f"Error taking screenshot of {url}: {e}")
        return False

def analyze_screenshot(filename):
    """Analyze a screenshot and extract visual information"""
    try:
        if not os.path.exists(filename):
            return f"Screenshot {filename} not found"
            
        img = Image.open(filename)
        width, height = img.size
        
        # Get file size
        file_size = os.path.getsize(filename)
        
        analysis = f"""
Screenshot Analysis: {filename}
- Dimensions: {width} x {height} pixels
- File size: {file_size:,} bytes
- Color mode: {img.mode}
"""
        
        return analysis
        
    except Exception as e:
        return f"Error analyzing {filename}: {e}"

def main():
    """Main function to take screenshots and analyze them"""
    
    # HTML files to screenshot
    html_files = [
        ('4_yasal_duzenlemeler.html', 'Legal Regulations'),
        ('5_strateji_ve_politika_belgeleri.html', 'Strategy & Policy Documents'),
        ('6_kalkinma_planlari.html', 'Development Plans'),
        ('7_ab_ilerleme_raporlari.html', 'EU Progress Reports')
    ]
    
    print("Starting screenshot analysis...")
    
    # Start local server
    server_process = start_local_server()
    if not server_process:
        print("Failed to start local server")
        return
    
    try:
        # Setup Firefox driver
        driver = setup_firefox_driver()
        if not driver:
            print("Failed to setup Firefox driver")
            return
        
        print("\nTaking screenshots of current HTML pages...")
        
        # Take screenshots of current pages
        for html_file, description in html_files:
            url = f"http://localhost:8000/{html_file}"
            screenshot_file = f"current_{html_file.replace('.html', '.png')}"
            
            print(f"\n=== {description} ===")
            success = take_screenshot(driver, url, screenshot_file, '.document-card')
            
            if success:
                analysis = analyze_screenshot(screenshot_file)
                print(analysis)
            else:
                print(f"Failed to screenshot {html_file}")
        
        # Create a simple comparison summary
        print("\n" + "="*60)
        print("CURRENT VERSION SCREENSHOT ANALYSIS SUMMARY")
        print("="*60)
        
        for html_file, description in html_files:
            screenshot_file = f"current_{html_file.replace('.html', '.png')}"
            if os.path.exists(screenshot_file):
                print(f"✓ {description}: Screenshot captured successfully")
                
                # Try to extract some visual insights
                try:
                    img = Image.open(screenshot_file)
                    width, height = img.size
                    print(f"  - Page dimensions: {width}x{height}")
                    print(f"  - File: {screenshot_file}")
                except:
                    print(f"  - Could not analyze image details")
            else:
                print(f"✗ {description}: Screenshot failed")
        
        print(f"\nScreenshots saved in: {os.getcwd()}")
        
    finally:
        # Cleanup
        if 'driver' in locals():
            driver.quit()
        if server_process:
            server_process.terminate()

if __name__ == "__main__":
    main()