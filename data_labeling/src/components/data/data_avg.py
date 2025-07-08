final_data = "/Users/mayamarkus-malone/Documents/VADMAP/data_labeling/src/components/data/vad_data.csv"

import csv

v_sum = 0
a_sum = 0
d_sum = 0
count = 0

with open(final_data, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            v_sum += float(row['V'])
            a_sum += float(row['A'])
            d_sum += float(row['D'])
            count += 1
        except (ValueError, KeyError):
            continue

if count > 0:
    v_avg = v_sum / count
    a_avg = a_sum / count
    d_avg = d_sum / count
    print(f"Average V: {v_avg:.4f}")
    print(f"Average A: {a_avg:.4f}")
    print(f"Average D: {d_avg:.4f}")
else:
    print("No valid rows found.")