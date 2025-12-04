#!/usr/bin/env python3
"""
Test script to reproduce the current hover background layering issue.
This script identifies all conflicting CSS rules that cause old and new backgrounds
to appear together on hover.
"""

import re
import os

def analyze_filar_card_rules():
    """Analyze all .filar-card rules to identify conflicts."""
    
    css_file_path = '/KARLAB-SOFTWARE/static/styles.css'
    
    if not os.path.exists(css_file_path):
        print("❌ CSS file not found!")
        return False
    
    with open(css_file_path, 'r', encoding='utf-8') as file:
        css_content = file.read()
    
    print("🔍 ANALYZING .filar-card RULES:")
    print("=" * 50)
    
    # Find all .filar-card rules
    patterns = [
        (r'\.filar-card\s*\{[^}]*\}', "Base .filar-card rule"),
        (r'\.filar-card:hover\s*\{[^}]*\}', ".filar-card:hover rules"),
        (r'\.filar-card:hover\s+\.card-overlay[^}]*\}', "Card overlay on hover"),
        (r'html\[data-theme="light"\]\s+\.filar-card[^}]*\}', "Light theme filar-card rules"),
        (r'html\[data-theme="light"\]\s+\.filar-card:hover[^}]*\}', "Light theme hover rules"),
        (r'html\[data-theme="light"\]\s+\.filar-card::before[^}]*\}', "Light theme ::before rules"),
        (r'html\[data-theme="light"\]\s+\.filar-card:hover::before[^}]*\}', "Light theme hover ::before rules"),
    ]
    
    for pattern, description in patterns:
        matches = re.findall(pattern, css_content, re.MULTILINE | re.DOTALL)
        if matches:
            print(f"\n📋 {description}:")
            for i, match in enumerate(matches, 1):
                print(f"  Rule #{i}: {match[:100]}...")
        else:
            print(f"\n❌ {description}: Not found")
    
    return True

def check_overlay_rules():
    """Check for overlay-related rules that might cause dark bars."""
    
    css_file_path = '/KARLAB-SOFTWARE/static/styles.css'
    
    with open(css_file_path, 'r', encoding='utf-8') as file:
        css_content = file.read()
    
    print("\n🔍 ANALYZING OVERLAY RULES:")
    print("=" * 50)
    
    # Check for card-overlay
    overlay_pattern = r'\.card-overlay\s*\{[^}]*\}'
    overlay_match = re.search(overlay_pattern, css_content, re.MULTILINE | re.DOTALL)
    
    if overlay_match:
        print("📋 Found .card-overlay rule:")
        print(overlay_match.group(0))
        
        # Check if it's used with filar-card
        hover_overlay_pattern = r'\.filar-card:hover\s+\.card-overlay[^}]*\}'
        hover_overlay_match = re.search(hover_overlay_pattern, css_content, re.MULTILINE | re.DOTALL)
        
        if hover_overlay_match:
            print("\n⚠️  ISSUE FOUND: .card-overlay is activated on .filar-card:hover")
            print("This creates a dark semi-transparent layer over the card!")
            print(hover_overlay_match.group(0))
            return True
    
    # Check for ::before pseudo-elements
    before_pattern = r'\.filar-card::before[^}]*\}'
    before_matches = re.findall(before_pattern, css_content, re.MULTILINE | re.DOTALL)
    
    if before_matches:
        print(f"\n📋 Found {len(before_matches)} .filar-card::before rules:")
        for i, match in enumerate(before_matches, 1):
            print(f"  Rule #{i}: {match[:100]}...")
    
    return False

def check_conflicting_backgrounds():
    """Check for conflicting background rules."""
    
    css_file_path = '/KARLAB-SOFTWARE/static/styles.css'
    
    with open(css_file_path, 'r', encoding='utf-8') as file:
        css_content = file.read()
    
    print("\n🔍 ANALYZING BACKGROUND CONFLICTS:")
    print("=" * 50)
    
    # Find all background declarations in filar-card rules
    background_patterns = [
        (r'\.filar-card[^{]*\{[^}]*background:[^;}]*[;}]', "Base background"),
        (r'\.filar-card:hover[^{]*\{[^}]*background:[^;}]*[;}]', "Hover background"),
        (r'html\[data-theme="light"\]\s+\.filar-card:hover[^}]*background:[^;}]*[;}]', "Light theme hover bg"),
    ]
    
    conflicts_found = 0
    
    for pattern, description in background_patterns:
        matches = re.findall(pattern, css_content, re.MULTILINE | re.DOTALL)
        if matches:
            conflicts_found += len(matches)
            print(f"\n📋 {description} ({len(matches)} rules):")
            for i, match in enumerate(matches, 1):
                print(f"  Rule #{i}: {match.strip()[:150]}...")
    
    if conflicts_found > 2:
        print(f"\n⚠️  CONFLICT DETECTED: {conflicts_found} different background rules found!")
        print("This causes multiple backgrounds to layer on top of each other.")
        return True
    
    return False

if __name__ == "__main__":
    print("🔍 TESTING CURRENT HOVER BACKGROUND ISSUE")
    print("=" * 60)
    
    analyze_filar_card_rules()
    overlay_issue = check_overlay_rules()
    bg_conflicts = check_conflicting_backgrounds()
    
    print("\n" + "=" * 60)
    print("📊 ISSUE SUMMARY:")
    
    if overlay_issue:
        print("🔴 OVERLAY ISSUE: Dark .card-overlay creates unwanted dark bar on hover")
    else:
        print("🟢 No overlay issues detected")
    
    if bg_conflicts:
        print("🔴 BACKGROUND CONFLICTS: Multiple conflicting background rules")
    else:
        print("🟢 No background conflicts detected")
    
    if overlay_issue or bg_conflicts:
        print("\n💡 SOLUTION NEEDED:")
        print("1. Remove or disable .card-overlay for .filar-card elements")
        print("2. Consolidate conflicting background rules into single, clean hover effect")
        print("3. Ensure ::before pseudo-elements don't conflict with main backgrounds")
    else:
        print("\n✅ No obvious issues detected - may need deeper investigation")