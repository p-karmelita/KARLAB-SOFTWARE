#!/usr/bin/env python3
"""
Test script to verify that the profile section background changes are applied correctly.
This script checks the CSS file for the correct background colors in both light and dark modes.
"""

import os
import re

def test_profile_section_styles():
    css_file_path = '/KARLAB-SOFTWARE/static/styles.css'
    
    if not os.path.exists(css_file_path):
        print("❌ CSS file not found!")
        return False
    
    with open(css_file_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Check for profile-section background in light mode
    light_mode_pattern = r'\.profile-section\s*{[^}]*background:\s*#372e56\s*!important'
    light_mode_found = re.search(light_mode_pattern, css_content, re.DOTALL | re.IGNORECASE)
    
    # Check for dark mode card background variable
    dark_mode_pattern = r'--card-bg:\s*#372e56'
    dark_mode_found = re.search(dark_mode_pattern, css_content)
    
    # Check for text color changes
    white_text_pattern = r'\.profile-content\s+h1\s*{[^}]*color:\s*#ffffff\s*!important'
    white_text_found = re.search(white_text_pattern, css_content, re.DOTALL | re.IGNORECASE)
    
    gray_text_pattern = r'\.profile-content\s+h2\s*{[^}]*color:\s*#cccccc'
    gray_text_found = re.search(gray_text_pattern, css_content, re.DOTALL | re.IGNORECASE)
    
    light_gray_text_pattern = r'\.profile-description\s+p\s*{[^}]*color:\s*#e0e0e0'
    light_gray_text_found = re.search(light_gray_text_pattern, css_content, re.DOTALL | re.IGNORECASE)
    
    print("=== CSS Profile Section Background Test ===")
    print(f"✓ Light mode profile-section background (#372e56): {'Found' if light_mode_found else '❌ Not found'}")
    print(f"✓ Dark mode --card-bg variable (#372e56): {'Found' if dark_mode_found else '❌ Not found'}")
    print(f"✓ Profile h1 white text color: {'Found' if white_text_found else '❌ Not found'}")
    print(f"✓ Profile h2 light gray text color: {'Found' if gray_text_found else '❌ Not found'}")
    print(f"✓ Profile paragraph light gray text color: {'Found' if light_gray_text_found else '❌ Not found'}")
    
    all_found = all([light_mode_found, dark_mode_found, white_text_found, gray_text_found, light_gray_text_found])
    
    if all_found:
        print("\n🎉 All CSS changes are correctly applied!")
        print("The profile section should now have a dark blue background (#372e56) matching the footer.")
        print("Text colors have been updated for proper readability on the dark background.")
        return True
    else:
        print("\n❌ Some CSS changes are missing or incorrect.")
        return False

if __name__ == "__main__":
    success = test_profile_section_styles()
    exit(0 if success else 1)