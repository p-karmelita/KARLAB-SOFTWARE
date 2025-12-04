#!/usr/bin/env python3
"""
Test script to identify the black letters bleeding issue.
This script checks for semi-transparent elements that could be causing faint text to show through.
"""

import re
import os

def test_black_letters_issue():
    """Test for semi-transparent elements causing black letters to bleed through."""
    
    css_file_path = '/KARLAB-SOFTWARE/static/styles.css'
    
    if not os.path.exists(css_file_path):
        print("❌ CSS file not found!")
        return False
    
    with open(css_file_path, 'r', encoding='utf-8') as file:
        css_content = file.read()
    
    print("🔍 TESTING FOR BLACK LETTERS BLEEDING ISSUE")
    print("=" * 60)
    
    issues_found = 0
    
    # Test 1: Check for conflicting ::before pseudo-elements
    before_create_pattern = r'html\[data-theme="light"\]\s+\.filar-card::before[^}]*opacity:\s*0\.\d+'
    before_disable_pattern = r'\.filar-card::before[^}]*display:\s*none\s*!important'
    
    before_creates = re.findall(before_create_pattern, css_content, re.MULTILINE | re.DOTALL)
    before_disables = re.findall(before_disable_pattern, css_content, re.MULTILINE | re.DOTALL)
    
    if before_creates and before_disables:
        print("🔴 CONFLICT FOUND: ::before pseudo-elements both created AND disabled")
        print(f"  - Rules creating ::before: {len(before_creates)}")
        print(f"  - Rules disabling ::before: {len(before_disables)}")
        print("  This causes semi-transparent overlays to bleed through!")
        issues_found += 1
    
    # Test 2: Check for semi-transparent backgrounds with rgba()
    rgba_low_opacity_pattern = r'background:[^;}]*rgba\([^)]*,\s*0\.[0-2]\d*\)'
    rgba_matches = re.findall(rgba_low_opacity_pattern, css_content)
    
    if rgba_matches:
        print(f"\n🔴 SEMI-TRANSPARENT BACKGROUNDS FOUND: {len(rgba_matches)} rules")
        print("These create faint overlays that appear as 'black letters':")
        for i, match in enumerate(rgba_matches[:3], 1):  # Show first 3
            print(f"  {i}. {match}")
        if len(rgba_matches) > 3:
            print(f"  ... and {len(rgba_matches) - 3} more")
        issues_found += 1
    
    # Test 3: Check for opacity values causing bleeding
    opacity_low_pattern = r'opacity:\s*0\.[0-2]\d*[^0-9]'
    opacity_matches = re.findall(opacity_low_pattern, css_content)
    
    if opacity_matches:
        print(f"\n🔴 LOW OPACITY VALUES FOUND: {len(opacity_matches)} instances")
        print("These could cause text/elements to appear faintly:")
        for i, match in enumerate(opacity_matches[:5], 1):  # Show first 5
            print(f"  {i}. {match.strip()}")
        if len(opacity_matches) > 5:
            print(f"  ... and {len(opacity_matches) - 5} more")
        issues_found += 1
    
    # Test 4: Check for text-shadow that might create ghost text
    text_shadow_pattern = r'text-shadow:[^;}]*rgba\([^)]*,\s*0\.[0-3]'
    shadow_matches = re.findall(text_shadow_pattern, css_content)
    
    if shadow_matches:
        print(f"\n🔴 SEMI-TRANSPARENT TEXT SHADOWS: {len(shadow_matches)} found")
        print("These could create ghost text effects:")
        for match in shadow_matches:
            print(f"  - {match}")
        issues_found += 1
    
    print(f"\n📊 TOTAL ISSUES FOUND: {issues_found}")
    
    if issues_found > 0:
        print("\n💡 ROOT CAUSE IDENTIFIED:")
        print("The 'black letters' are caused by:")
        print("1. Conflicting CSS rules creating semi-transparent overlays")
        print("2. Low opacity values (0.15, 0.22) making elements barely visible")
        print("3. Multiple background layers bleeding through each other")
        return True
    else:
        print("\n✅ No obvious semi-transparent elements found")
        return False

if __name__ == "__main__":
    success = test_black_letters_issue()
    
    if success:
        print("\n🔧 SOLUTION NEEDED:")
        print("Remove or override all semi-transparent rules that conflict with the clean design")
        print("Ensure only solid, opaque backgrounds are used for cards")
    else:
        print("\n🤔 Issue may be caused by other factors - need deeper investigation")