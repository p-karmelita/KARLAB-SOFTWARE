#!/usr/bin/env python3
"""
Test script to verify the hover background fix for .filar-card elements.
This script checks if the CSS changes properly resolve the background layering issue.
"""

import re
import os

def test_hover_background_fix():
    """Test that the hover background is now opaque instead of semi-transparent."""
    
    css_file_path = '/KARLAB-SOFTWARE/static/styles.css'
    
    if not os.path.exists(css_file_path):
        print("❌ CSS file not found!")
        return False
    
    with open(css_file_path, 'r', encoding='utf-8') as file:
        css_content = file.read()
    
    # Look for the .filar-card:hover rule
    hover_pattern = r'\.filar-card:hover\s*\{([^}]*)\}'
    hover_match = re.search(hover_pattern, css_content)
    
    if not hover_match:
        print("❌ .filar-card:hover rule not found!")
        return False
    
    hover_rules = hover_match.group(1)
    print("Found .filar-card:hover rules:")
    print(hover_rules)
    
    # Check if background uses rgba (semi-transparent) - this should NOT be present
    rgba_pattern = r'background:[^;]*rgba\([^)]*,\s*0\.\d+\)'
    if re.search(rgba_pattern, hover_rules):
        print("❌ Semi-transparent background still present - layering issue not fixed!")
        return False
    
    # Check if background uses solid/opaque colors
    solid_bg_pattern = r'background:[^;]*linear-gradient\([^;]*#[a-fA-F0-9]{6}[^;]*\)'
    if re.search(solid_bg_pattern, hover_rules):
        print("✅ Opaque gradient background found - layering issue should be fixed!")
        return True
    
    print("⚠️  Background property found but format unclear")
    return False

def test_transition_property():
    """Test that transition property includes background for smooth hover effect."""
    
    css_file_path = '/KARLAB-SOFTWARE/static/styles.css'
    
    with open(css_file_path, 'r', encoding='utf-8') as file:
        css_content = file.read()
    
    # Look for the .filar-card base rule
    card_pattern = r'\.filar-card\s*\{([^}]*)\}'
    card_match = re.search(card_pattern, css_content)
    
    if not card_match:
        print("❌ .filar-card base rule not found!")
        return False
    
    card_rules = card_match.group(1)
    
    # Check if transition includes background
    if 'background' in card_rules and 'transition' in card_rules:
        print("✅ Transition and background properties found in base rule")
        return True
    elif 'transition' in card_rules:
        print("⚠️  Transition found but doesn't include background - might cause abrupt changes")
        return False
    else:
        print("⚠️  No transition property found - changes might be abrupt")
        return False

if __name__ == "__main__":
    print("Testing hover background fix...")
    print("=" * 50)
    
    background_test = test_hover_background_fix()
    transition_test = test_transition_property()
    
    print("\n" + "=" * 50)
    print("TEST RESULTS:")
    print(f"Background layering fix: {'✅ PASS' if background_test else '❌ FAIL'}")
    print(f"Transition smoothness: {'✅ PASS' if transition_test else '⚠️  WARNING'}")
    
    if background_test:
        print("\n🎉 The hover background layering issue should be resolved!")
        print("The card will now show a clean hover effect without old background showing through.")
    else:
        print("\n❌ Issue not resolved - may need further investigation.")