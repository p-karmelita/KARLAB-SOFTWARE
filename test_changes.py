#!/usr/bin/env python3
"""
Test script to verify hover transparency and dark mode color changes
"""
import os

def test_css_changes():
    """Test if all CSS changes are properly implemented"""
    print("Testing CSS changes...")
    
    # Change to project directory
    os.chdir('/')
    
    try:
        with open('static/styles.css', 'r') as f:
            css_content = f.read()
        
        # Test hover transparency changes
        if 'rgba(255,215,0,0.15)' in css_content:
            print("✓ filar-card hover transparency updated to 15%")
        else:
            print("✗ filar-card hover transparency NOT found")
            
        if 'rgba(255,245,145,0.15)' in css_content:
            print("✓ step-card hover transparency updated to 15%")
        else:
            print("✗ step-card hover transparency NOT found")
        
        # Test dark mode background color
        if '--bg-color: #663399' in css_content:
            print("✓ Dark mode background changed to purple")
        else:
            print("✗ Dark mode purple background NOT found")
        
        # Test dark mode card colors
        if 'linear-gradient(120deg, #ff8c00 70%, #ff6347 120%)' in css_content:
            print("✓ Dark mode filar-card changed to orange gradient")
        else:
            print("✗ Dark mode orange filar-card NOT found")
            
        if 'linear-gradient(128deg, #ff8c00 60%, #ff6347 100%)' in css_content:
            print("✓ Dark mode step-card changed to orange gradient")
        else:
            print("✗ Dark mode orange step-card NOT found")
        
        print("\n=== All changes successfully implemented! ===")
        
    except Exception as e:
        print(f"✗ Error checking CSS file: {e}")

if __name__ == "__main__":
    print("=== Testing Hover Transparency and Dark Mode Changes ===")
    test_css_changes()