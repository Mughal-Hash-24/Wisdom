#!/usr/bin/env python3
import os
import sys
import json
import time
import argparse
import re

def parse_args():
    parser = argparse.ArgumentParser(description="Fiqh Programmatic Validator")
    parser.add_argument("--dir", required=True, help="Absolute path to the generated Fiqh folder")
    parser.add_argument("--slug", required=True, help="Slug of the question")
    parser.add_argument("--concept", required=True, help="Concept tag of the question")
    parser.add_argument("--start-time", type=float, help="Unix start time of the execution for timing stats")
    parser.add_argument("--out-dir", required=True, help="Directory to save timing.json and grading.json")
    return parser.parse_args()

def check_file_structure(file_path, expected_headings):
    if not os.path.exists(file_path):
        return False, f"File {os.path.basename(file_path)} does not exist."
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    missing = []
    for heading in expected_headings:
        if heading not in content:
            missing.append(heading)
            
    if missing:
        return False, f"Missing headings in {os.path.basename(file_path)}: {', '.join(missing)}"
    return True, "All expected headings present."

def check_frontmatter(file_path, expected_tags):
    if not os.path.exists(file_path):
        return False, "File does not exist."
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Extract YAML frontmatter
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not fm_match:
        return False, "Missing YAML frontmatter delimiters (---)."
        
    fm_content = fm_match.group(1)
    missing_tags = []
    for tag in expected_tags:
        if tag not in fm_content:
            missing_tags.append(tag)
            
    if missing_tags:
        return False, f"Missing tags in frontmatter: {', '.join(missing_tags)}"
    return True, "Frontmatter tags validated."

def check_links(file_path, expected_links):
    if not os.path.exists(file_path):
        return False, "File does not exist."
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    missing_links = []
    for link in expected_links:
        if link not in content:
            missing_links.append(link)
            
    if missing_links:
        return False, f"Missing cross-links: {', '.join(missing_links)}"
    return True, "Cross-links validated."

def check_citations(file_path):
    if not os.path.exists(file_path):
        return False, "File does not exist."
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Standard citation pattern search: check if references/citations are present and have verification markers
    # Every school file must have a classical reference with (VERIFIED) or (UNCERTAIN)
    ref_section_match = re.search(r'##\s+Ruling.*?\*\*Classical Reference:\*\*.*?\n', content, re.DOTALL | re.IGNORECASE)
    if not ref_section_match:
        return False, "Missing Classical Reference citation block in Ruling section."
        
    ref_block = ref_section_match.group(0)
    if "(VERIFIED)" not in ref_block and "(UNCERTAIN)" not in ref_block:
        return False, "Classical Reference is missing verification marker '(VERIFIED)' or '(UNCERTAIN)'."
        
    return True, "Citations format validated."

def main():
    args = parse_args()
    
    # Initialize timing
    end_time = time.time()
    start_time = args.start_time if args.start_time else end_time
    duration_ms = int((end_time - start_time) * 1000)
    
    # Define files to check
    files = {
        "synthesis": os.path.join(args.dir, f"Synthesis - {args.slug}.md"),
        "hanafi": os.path.join(args.dir, f"Hanafi - {args.slug}.md"),
        "maliki": os.path.join(args.dir, f"Maliki - {args.slug}.md"),
        "shafii": os.path.join(args.dir, f"Shafii - {args.slug}.md"),
        "hanbali": os.path.join(args.dir, f"Hanbali - {args.slug}.md")
    }
    
    assertions = []
    
    # 1. Check folder existence
    folder_exists = os.path.exists(args.dir)
    assertions.append({
        "text": f"Fiqh output folder exists: {args.dir}",
        "passed": folder_exists,
        "evidence": f"Folder exists: {folder_exists}"
    })
    
    if not folder_exists:
        # Save grading and timing files and exit
        write_results(assertions, duration_ms, args.out_dir)
        sys.exit(1)
        
    # 2. Check all 5 files exist
    for role, path in files.items():
        exists = os.path.exists(path)
        assertions.append({
            "text": f"File '{os.path.basename(path)}' exists",
            "passed": exists,
            "evidence": f"File existence: {exists}"
        })
        
    # 3. Check structural headings
    school_headings = ["## Ruling", "## Usul al-Fiqh", "## Internal Dissent"]
    synthesis_headings = ["## Executive Summary", "## Consensus & Points of Agreement", "## Primary Areas of Divergence", "## Comparative Synthesis Matrix"]
    
    for role, path in files.items():
        if not os.path.exists(path):
            continue
        headings = school_headings if role != "synthesis" else synthesis_headings
        passed, msg = check_file_structure(path, headings)
        assertions.append({
            "text": f"Structure of '{os.path.basename(path)}' contains all required sections",
            "passed": passed,
            "evidence": msg
        })
        
    # 4. Check frontmatter tags
    expected_tags = ["field/humanities", "subject/fiqh", f"concept/{args.concept}"]
    for role, path in files.items():
        if not os.path.exists(path):
            continue
        passed, msg = check_frontmatter(path, expected_tags)
        assertions.append({
            "text": f"Frontmatter tags in '{os.path.basename(path)}' are correct",
            "passed": passed,
            "evidence": msg
        })
        
    # 5. Check cross-links
    # Madhab files must link to synthesis and T.O.C (Fiqh)
    # Synthesis file must link to T.O.C (Fiqh)
    for role, path in files.items():
        if not os.path.exists(path):
            continue
        if role == "synthesis":
            links = ["[[T.O.C (Fiqh)|Up to Fiqh]]"]
        else:
            links = ["[[T.O.C (Fiqh)|Up to Fiqh]]", f"[[Synthesis - {args.slug}|View Synthesis]]"]
        passed, msg = check_links(path, links)
        assertions.append({
            "text": f"Cross-links in '{os.path.basename(path)}' are correct",
            "passed": passed,
            "evidence": msg
        })
        
    # 6. Check citations verification markers in school files
    for role, path in files.items():
        if role == "synthesis" or not os.path.exists(path):
            continue
        passed, msg = check_citations(path)
        assertions.append({
            "text": f"Citations in '{os.path.basename(path)}' conform to format rules",
            "passed": passed,
            "evidence": msg
        })
        
    # 7. Check word count (> 0)
    for role, path in files.items():
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            words = len(f.read().split())
        assertions.append({
            "text": f"Word count of '{os.path.basename(path)}' is non-zero",
            "passed": words > 0,
            "evidence": f"Word count: {words} words"
        })

    # Write output reports
    write_results(assertions, duration_ms, args.out_dir)

def write_results(assertions, duration_ms, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    
    passed_count = sum(1 for a in assertions if a["passed"])
    total_count = len(assertions)
    pass_rate = passed_count / total_count if total_count > 0 else 0.0
    
    grading_data = {
        "expectations": assertions,
        "summary": {
            "passed": passed_count,
            "failed": total_count - passed_count,
            "total": total_count,
            "pass_rate": round(pass_rate, 2)
        }
    }
    
    timing_data = {
        "total_tokens": 0,  # Tokens not easily measurable here, populated by agent if needed
        "duration_ms": duration_ms,
        "total_duration_seconds": round(duration_ms / 1000.0, 2)
    }
    
    with open(os.path.join(out_dir, "grading_programmatic.json"), "w", encoding="utf-8") as f:
        json.dump(grading_data, f, indent=2)
        
    with open(os.path.join(out_dir, "timing.json"), "w", encoding="utf-8") as f:
        json.dump(timing_data, f, indent=2)
        
    print(f"Programmatic validation completed. Pass rate: {pass_rate:.2f}. Duration: {duration_ms/1000.0:.2f}s")

if __name__ == "__main__":
    main()
