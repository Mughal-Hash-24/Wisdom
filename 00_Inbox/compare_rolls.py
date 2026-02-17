import csv
import os

def read_csv_simple(path):
    rolls = set()
    if not os.path.exists(path):
        return rolls
    with open(path, mode='r') as f:
        # Check if there's a header or if it's raw
        first_line = f.readline().strip()
        f.seek(0)
        
        # If the first line is "Roll Number", use DictReader, else read line by line
        if first_line.lower() == 'roll number':
            reader = csv.DictReader(f)
            for row in reader:
                rolls.add(row['Roll Number'].strip().lower())
        else:
            # Raw list or different header
            for line in f:
                val = line.strip().lower()
                if val and val != 'roll number': # Basic sanitization
                    rolls.add(val)
    return rolls

def compare():
    flagged_path = '00_Inbox/flagged_rolls.csv'
    test_path = '00_Inbox/test.csv'
    
    flagged = read_csv_simple(flagged_path)
    test = read_csv_simple(test_path)
    
    both = flagged.intersection(test)
    only_flagged = flagged - test
    watchlist = test - flagged # In test but not flagged
    
    # Generate Report
    print("--- Comparison Report ---")
    print(f"Total in Flagged: {len(flagged)}")
    print(f"Total in Test: {len(test)}")
    print(f"Common to Both: {len(both)}")
    print(f"Exclusive to Flagged: {len(only_flagged)}")
    print(f"WATCHLIST (In Test, not in Flagged): {len(watchlist)}")
    
    # Create the CSV Report
    output_path = '00_Inbox/comparison_report.csv'
    
    # We want columns: Both, Exclusive_Flagged, WATCHLIST
    # To write to CSV, we need the longest list length to iterate
    max_len = max(len(both), len(only_flagged), len(watchlist))
    
    both_list = sorted(list(both))
    only_flagged_list = sorted(list(only_flagged))
    watchlist_list = sorted(list(watchlist))
    
    with open(output_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['In Both', 'Exclusive to Flagged', 'WATCHLIST'])
        for i in range(max_len):
            row = [
                both_list[i] if i < len(both_list) else '',
                only_flagged_list[i] if i < len(only_flagged_list) else '',
                watchlist_list[i] if i < len(watchlist_list) else ''
            ]
            writer.writerow(row)
            
    print(f"\nDetailed report saved to {output_path}")

if __name__ == "__main__":
    compare()
