import pandas as pd
import json

def clean_value(val):
    """Clean and convert values to appropriate numeric format"""
    if pd.isna(val) or val == '' or val == 'null':
        return None
    
    # Handle string values
    if isinstance(val, str):
        val = val.strip()
        if val == '' or val.lower() == 'null':
            return None
        
        # Remove quotes and other formatting
        val = val.replace('"', '').replace(',', '').replace("'", '').replace('"', '').replace('"', '')
        
        # Handle parentheses (negative values in accounting format)
        if val.startswith('(') and val.endswith(')'):
            try:
                return float(val[1:-1])  # Keep positive for capacity data
            except ValueError:
                return None
    
    # Try to convert to number
    try:
        if isinstance(val, (int, float)):
            return val
        if '.' in str(val):
            return float(val)
        return int(val)
    except (ValueError, TypeError):
        return None

# Read both electricity datasets
production_df = pd.read_csv('data/b/cleaned_elektrik_üretimi.csv')
capacity_df = pd.read_csv('data/b/cleaned_kurulu_güç.csv')

# Process Production Data
production_data = []
if 'Yıllar' in production_df.columns:
    years_col = 'Yıllar'
else:
    years_col = production_df.columns[0]  # Assume first column is years

years = sorted(production_df[years_col].unique())

# Get energy source columns (exclude years and metadata columns)
source_columns = [col for col in production_df.columns if col not in [years_col, 'Column_19'] and not pd.isna(col)]

for source in source_columns:
    if source in [years_col, 'Column_19']:
        continue
        
    source_data = {'Kategori': f"Elektrik Üretimi - {source}"}
    
    for year in years:
        year_data = production_df[production_df[years_col] == year]
        if len(year_data) > 0 and source in year_data.columns:
            value = year_data[source].iloc[0]
            cleaned_value = clean_value(value)
            source_data[str(year)] = cleaned_value
        else:
            source_data[str(year)] = None
    
    # Only add if there's some data
    if any(v is not None for k, v in source_data.items() if k != 'Kategori'):
        production_data.append(source_data)

# Process Capacity Data
capacity_data = []
if 'Yıllar' in capacity_df.columns:
    years_col = 'Yıllar'
else:
    years_col = capacity_df.columns[0]  # Assume first column is years

years = sorted(capacity_df[years_col].unique())

# Get energy source columns (exclude years and metadata columns)
source_columns = [col for col in capacity_df.columns if col not in [years_col, 'Column_19'] and not pd.isna(col)]

for source in source_columns:
    if source in [years_col, 'Column_19']:
        continue
        
    source_data = {'Kategori': f"Kurulu Güç - {source}"}
    
    for year in years:
        year_data = capacity_df[capacity_df[years_col] == year]
        if len(year_data) > 0 and source in year_data.columns:
            value = year_data[source].iloc[0]
            cleaned_value = clean_value(value)
            source_data[str(year)] = cleaned_value
        else:
            source_data[str(year)] = None
    
    # Only add if there's some data
    if any(v is not None for k, v in source_data.items() if k != 'Kategori'):
        capacity_data.append(source_data)

# Combine both datasets
electricity_data = production_data + capacity_data

# Write to JavaScript file
with open('data_b_embedded.js', 'w', encoding='utf-8') as f:
    f.write('const embeddedDataB = ')
    json.dump(electricity_data, f, ensure_ascii=False, indent=2)
    f.write(';')

print(f"Converted {len(production_data)} production categories and {len(capacity_data)} capacity categories to JavaScript format.")
print("File saved as 'data_b_embedded.js'")

# Print first few categories for verification
print("\nFirst few categories:")
for i, item in enumerate(electricity_data[:5]):
    print(f"{i+1}. {item['Kategori']}")
    sample_years = [k for k in item.keys() if k != 'Kategori'][:3]
    for year in sample_years:
        print(f"   {year}: {item[year]}") 