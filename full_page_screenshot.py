#!/usr/bin/env python3
"""
Take full-height screenshot to show all content including environment fields
"""

import os
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

def setup_firefox_driver():
    """Setup Firefox driver with full page capture"""
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    firefox_options.add_argument('--width=1920')
    firefox_options.add_argument('--height=2000')  # Taller for full content
    
    try:
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
        return driver
    except Exception as e:
        print(f"Error setting up Firefox driver: {e}")
        return None

def take_full_screenshot():
    """Take full page screenshot showing environment content"""
    
    # Start server
    server = subprocess.Popen(['python3', '-m', 'http.server', '8000'], 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    
    try:
        driver = setup_firefox_driver()
        if not driver:
            print("Failed to setup driver")
            return
        
        # Load page
        url = "http://localhost:8000/6_kalkinma_planlari.html"
        print(f"Loading {url}...")
        driver.get(url)
        time.sleep(3)
        
        # Set window size to capture more content
        driver.set_window_size(1920, 1200)
        
        # Get full page height
        total_height = driver.execute_script("return document.body.scrollHeight")
        print(f"Full page height: {total_height}px")
        
        # Take screenshot
        driver.save_screenshot("full_page_6_kalkinma_planlari.png")
        print("Full page screenshot saved!")
        
        # Also take scrolled screenshot to show environment content
        driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(1)
        driver.save_screenshot("scrolled_6_kalkinma_planlari.png")
        print("Scrolled screenshot saved!")
        
        driver.quit()
        
    finally:
        server.terminate()

if __name__ == "__main__":
    take_full_screenshot()