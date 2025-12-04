#!/usr/bin/env python3
"""
Test script to verify dark mode issue - checking if only navbar changes
"""
import os

def test_dark_mode_css():
    """Test if dark mode CSS is properly implemented for entire page"""
    print("Testing dark mode CSS implementation...")
    
    # Change to project directory
    os.chdir('/')
    
    try:
        with open('static/styles.css', 'r') as f:
            css_content = f.read()
        
        issues_found = []
        
        # Check for CSS variable definitions
        if ':root {' in css_content and '--bg-color: #ffffff' in css_content:
            print("✓ Light mode CSS variables defined")
        else:
            issues_found.append("Light mode CSS variables not properly defined")
            
        if '[data-theme="dark"] {' in css_content and '--bg-color: #663399' in css_content:
            print("✓ Dark mode CSS variables defined")
        else:
            issues_found.append("Dark mode CSS variables not properly defined")
        
        # Check for body background application
        body_dark_selectors = []
        if 'html[data-theme="dark"] body {' in css_content:
            body_dark_selectors.append('html[data-theme="dark"] body')
        # More precise check for the problematic selector
        lines = css_content.split('\n')
        for line in lines:
            if line.strip().startswith('[data-theme="dark"] body {'):
                body_dark_selectors.append('[data-theme="dark"] body')
            
        if body_dark_selectors:
            print(f"✓ Found body dark mode selectors: {', '.join(body_dark_selectors)}")
        else:
            issues_found.append("No body dark mode selectors found")
        
        # Check for conflicting or duplicate rules
        if len(body_dark_selectors) > 1:
            issues_found.append(f"Multiple conflicting body selectors found: {body_dark_selectors}")
        
        # Check if background-color uses CSS variables
        if 'background-color: var(--bg-color)' in css_content:
            print("✓ Body uses CSS variables for background")
        else:
            issues_found.append("Body doesn't use CSS variables for background")
        
        # Check nav styling
        if '[data-theme="dark"] nav' in css_content or 'html[data-theme="dark"] body > nav' in css_content:
            print("✓ Navigation dark mode styling found")
        else:
            issues_found.append("Navigation dark mode styling not found")
        
        if issues_found:
            print("\n=== ISSUES FOUND ===")
            for i, issue in enumerate(issues_found, 1):
                print(f"{i}. {issue}")
        else:
            print("\n=== All CSS rules appear correct ===")
        
        return len(issues_found) == 0
        
    except Exception as e:
        print(f"✗ Error checking CSS file: {e}")
        return False

def check_html_structure():
    """Check if HTML properly includes dark mode elements"""
    print("\nChecking HTML structure...")
    
    try:
        with open('templates/base.html', 'r') as f:
            html_content = f.read()
        
        if 'id="dark-mode-toggle"' in html_content:
            print("✓ Dark mode toggle button found")
        else:
            print("✗ Dark mode toggle button NOT found")
            return False
            
        if 'darkmode.js' in html_content:
            print("✓ Dark mode JavaScript included")
        else:
            print("✗ Dark mode JavaScript NOT included")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ Error checking HTML file: {e}")
        return False

def check_javascript():
    """Check dark mode JavaScript implementation"""
    print("\nChecking JavaScript implementation...")
    
    try:
        with open('static/darkmode.js', 'r') as f:
            js_content = f.read()
        
        if 'data-theme' in js_content and 'setAttribute' in js_content:
            print("✓ JavaScript sets data-theme attribute")
        else:
            print("✗ JavaScript doesn't properly set data-theme")
            return False
            
        if 'documentElement' in js_content or 'html =' in js_content:
            print("✓ JavaScript targets HTML element")
        else:
            print("✗ JavaScript might not target HTML element correctly")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ Error checking JavaScript file: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Dark Mode Issue ===")
    css_ok = test_dark_mode_css()
    html_ok = check_html_structure()
    js_ok = check_javascript()
    
    if css_ok and html_ok and js_ok:
        print("\n=== All components appear correctly implemented ===")
        print("Issue might be with CSS selector specificity or conflicts")
    else:
        print("\n=== Issues found that need fixing ===")