import csv
import json

def clean_value(val):
    if val is None or val.strip() == '':
        return None
    val = val.replace('"', '').replace(',', '').replace('’', '').replace('“', '').replace('”', '')
    try:
        # Try integer first, then float
        if '.' in val:
            return float(val)
        return int(val)
    except ValueError:
        return None

input_csv = '1923-2023.csv'
output_js = 'embedded_data.js'

with open(input_csv, encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

# The first row is the header (years)
header = rows[0]
years = [int(y) for y in header[1:] if y.strip() != '']

embedded_data = []
for row in rows[1:]:
    if not row or not row[0].strip():
        continue  # skip empty or separator rows
    category = row[0].strip().replace('"', '').replace("“", "").replace("”", "")
    if not category:
        continue
    obj = {'category': category}
    for i, year in enumerate(years):
        val = row[i+1] if i+1 < len(row) else ''
        obj[year] = clean_value(val)
    embedded_data.append(obj)

# Output as JS array
with open(output_js, 'w', encoding='utf-8') as f:
    f.write('const embeddedRawData = ')
    json.dump(embedded_data, f, ensure_ascii=False, indent=2)
    f.write(';')

print(f"Done! JS array written to {output_js}. Copy its contents into your index.html.")