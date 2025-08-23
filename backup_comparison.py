#!/usr/bin/env python3
"""
Take screenshot of backup version for comparison
"""

import os
import subprocess
import time
from screenshot_analyzer import setup_firefox_driver, take_screenshot

def compare_with_backup():
    """Take screenshot of backup version"""
    
    # Start server for backup files
    os.chdir('backup_html')
    backup_server = subprocess.Popen(['python3', '-m', 'http.server', '8002'], 
                                   stdout=subprocess.DEVNULL, 
                                   stderr=subprocess.DEVNULL)
    time.sleep(2)
    
    try:
        driver = setup_firefox_driver()
        if not driver:
            print("Failed to setup driver")
            return
        
        # Take screenshot of backup version
        backup_url = "http://localhost:8002/6_kalkinma_planlari.html"
        backup_screenshot = "../backup_6_kalkinma_planlari.png"
        success = take_screenshot(driver, backup_url, backup_screenshot, '.document-card')
        
        if success:
            print("Backup screenshot taken successfully")
        else:
            print("Failed to take backup screenshot")
            
    finally:
        if 'driver' in locals():
            driver.quit()
        if backup_server:
            backup_server.terminate()
        os.chdir('..')

if __name__ == "__main__":
    compare_with_backup()