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
                return -float(val[1:-1])
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

# Read the consolidated energy data
df = pd.read_csv('data/a/consolidated_energy_data_20250618_125053.csv')

# Group by year and category to create proper structure
energy_data = []

# Get all unique years and sort them
years = sorted(df['year'].unique())

# Get all unique categories
categories = df['category'].unique()

# For each category, create a data object
for category in categories:
    if pd.isna(category) or category.strip() == '':
        continue
        
    category_data = {'Kategori': category.strip()}
    
    # Get data for this category across all years
    category_df = df[df['category'] == category]
    
    for year in years:
        year_data = category_df[category_df['year'] == year]
        
        if len(year_data) > 0:
            # For now, let's use 'Toplam' column if it exists, otherwise sum relevant columns
            if 'Toplam' in year_data.columns:
                value = year_data['Toplam'].iloc[0]
            else:
                # Try to find a reasonable total column or use a key energy source
                # Look for common energy total columns
                total_cols = [col for col in year_data.columns if 'toplam' in col.lower() or 'total' in col.lower()]
                if total_cols:
                    value = year_data[total_cols[0]].iloc[0]
                else:
                    # Use sum of major energy sources if available
                    energy_cols = ['Taş Kömürü', 'Linyit', 'Doğal Gaz', 'Hidrolik']
                    available_cols = [col for col in energy_cols if col in year_data.columns]
                    if available_cols:
                        value = year_data[available_cols].sum(axis=1).iloc[0]
                    else:
                        # Use the first numeric column after year, category, source_row
                        numeric_cols = year_data.select_dtypes(include=[int, float]).columns
                        non_meta_cols = [col for col in numeric_cols if col not in ['year', 'source_row']]
                        if non_meta_cols:
                            value = year_data[non_meta_cols[0]].iloc[0]
                        else:
                            value = None
        else:
            value = None
        
        # Clean the value
        cleaned_value = clean_value(value)
        category_data[str(year)] = cleaned_value

    energy_data.append(category_data)

# Remove categories with all null values
energy_data = [item for item in energy_data if any(v is not None for k, v in item.items() if k != 'Kategori')]

# Write to JavaScript file
with open('data_a_embedded.js', 'w', encoding='utf-8') as f:
    f.write('const embeddedDataA = ')
    json.dump(energy_data, f, ensure_ascii=False, indent=2)
    f.write(';')

print(f"Converted {len(energy_data)} categories to JavaScript format.")
print("File saved as 'data_a_embedded.js'")

# Print first few categories for verification
print("\nFirst few categories:")
for i, item in enumerate(energy_data[:3]):
    print(f"{i+1}. {item['Kategori']}")
    sample_years = [k for k in item.keys() if k != 'Kategori'][:5]
    for year in sample_years:
        print(f"   {year}: {item[year]}") 