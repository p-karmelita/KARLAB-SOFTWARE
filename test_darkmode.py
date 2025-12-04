#!/usr/bin/env python3
"""
Test script to verify dark mode implementation
"""
import subprocess
import time
import os

def test_flask_app():
    """Test if the Flask app starts correctly"""
    print("Testing Flask app startup...")
    
    # Change to project directory
    os.chdir('/')
    
    try:
        # Start Flask app in background
        process = subprocess.Popen(['python3', 'app.py'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait a moment for startup
        time.sleep(3)
        
        # Check if process is still running
        poll = process.poll()
        if poll is None:
            print("✓ Flask app started successfully")
            
            # Test if we can access the main page
            try:
                import requests
                response = requests.get('http://localhost:5000', timeout=5)
                if response.status_code == 200:
                    print("✓ Main page accessible")
                    
                    # Check if dark mode elements are present
                    if 'dark-mode-toggle' in response.text:
                        print("✓ Dark mode toggle button found in HTML")
                    else:
                        print("✗ Dark mode toggle button NOT found in HTML")
                        
                    if 'darkmode.js' in response.text:
                        print("✓ Dark mode JavaScript file included")
                    else:
                        print("✗ Dark mode JavaScript file NOT included")
                        
                else:
                    print(f"✗ Main page returned status code: {response.status_code}")
            except ImportError:
                print("! requests module not available, skipping HTTP test")
            except Exception as e:
                print(f"✗ Error accessing main page: {e}")
        else:
            stdout, stderr = process.communicate()
            print(f"✗ Flask app failed to start")
            print(f"Error: {stderr.decode()}")
        
        # Terminate the process
        process.terminate()
        
    except Exception as e:
        print(f"✗ Error starting Flask app: {e}")

def check_files():
    """Check if all required files exist"""
    print("\nChecking required files...")
    
    files_to_check = [
        'static/darkmode.js',
        'static/styles.css',
        'templates/base.html',
        'app.py'
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")

def check_dark_mode_implementation():
    """Check if dark mode implementation is complete"""
    print("\nChecking dark mode implementation...")
    
    # Check darkmode.js
    try:
        with open('static/darkmode.js', 'r') as f:
            js_content = f.read()
            if 'dark-mode-toggle' in js_content:
                print("✓ darkmode.js references toggle button")
            if 'data-theme' in js_content:
                print("✓ darkmode.js uses data-theme attribute")
            if 'localStorage' in js_content:
                print("✓ darkmode.js includes persistence")
    except Exception as e:
        print(f"✗ Error checking darkmode.js: {e}")
    
    # Check CSS
    try:
        with open('static/styles.css', 'r') as f:
            css_content = f.read()
            if '[data-theme="dark"]' in css_content:
                print("✓ CSS includes dark theme selectors")
            if 'dark-mode-btn' in css_content:
                print("✓ CSS includes dark mode button styles")
    except Exception as e:
        print(f"✗ Error checking styles.css: {e}")
    
    # Check base.html
    try:
        with open('templates/base.html', 'r') as f:
            html_content = f.read()
            if 'id="dark-mode-toggle"' in html_content:
                print("✓ base.html includes dark mode toggle button")
            if 'darkmode.js' in html_content:
                print("✓ base.html includes darkmode.js script")
    except Exception as e:
        print(f"✗ Error checking base.html: {e}")

if __name__ == "__main__":
    print("=== Dark Mode Implementation Test ===")
    check_files()
    check_dark_mode_implementation()
    test_flask_app()
    print("\n=== Test Complete ===")