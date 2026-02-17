import csv
import re
from collections import defaultdict

def extract_roll(path):
    # Extracts roll number (e.g., i250574) from paths like ./i250574/
    match = re.search(r'i\d+', path)
    return match.group() if match else path

def perform_analysis(csv_path):
    stats = defaultdict(lambda: {
        'max_lines': 0,
        'total_cases': 0,
        'all_cases': []
    })

    try:
        with open(csv_path, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                lines = int(row['Lines Matched'])
                r1 = extract_roll(row['File 1'])
                r2 = extract_roll(row['File 2'])
                
                for r in [r1, r2]:
                    stats[r]['max_lines'] = max(stats[r]['max_lines'], lines)
                    stats[r]['total_cases'] += 1
                    stats[r]['all_cases'].append(lines)
    except FileNotFoundError:
        print(f"Error: {csv_path} not found.")
        return

    # Criterion: 130+ lines OR 3 or more separate cases
    flagged = []
    for roll, data in stats.items():
        if data['max_lines'] >= 130 or data['total_cases'] >= 3:
            flagged.append(roll)

    flagged.sort()

    print("--- Plagiarism Analysis Report ---")
    print(f"\n[FLAGGED ROLLS] (130+ lines OR >=3 cases)")
    print(f"Count: {len(flagged)}")
    
    # Save results to CSV
    output_path = '00_Inbox/flagged_rolls.csv'
    with open(output_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Roll Number'])
        for roll in flagged:
            writer.writerow([roll])
            print(roll)
    
    print(f"\nResults saved to {output_path}")

if __name__ == "__main__":
    perform_analysis('00_Inbox/moss_results.csv')
