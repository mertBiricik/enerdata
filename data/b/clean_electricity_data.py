import pandas as pd
import numpy as np
from openpyxl import load_workbook
import json

def clean_excel_data(file_path):
    """
    Clean up the messy Turkish electricity data Excel file
    """
    print(f"🧹 CLEANING EXCEL DATA: {file_path}")
    print("=" * 60)
    
    # Read both sheets
    excel_data = pd.read_excel(file_path, sheet_name=None, header=0)
    
    cleaned_data = {}
    
    for sheet_name, df in excel_data.items():
        print(f"\n📊 Cleaning sheet: '{sheet_name}'")
        print("-" * 40)
        
        # Store original dimensions
        orig_rows, orig_cols = df.shape
        
        # 1. Clean column names
        print("   🏷️  Cleaning column names...")
        new_columns = []
        for i, col in enumerate(df.columns):
            if pd.isna(col) or str(col).strip() == '':
                new_columns.append(f'Column_{i+1}')
            else:
                # Clean up spaces and formatting
                clean_name = str(col).strip()
                clean_name = clean_name.replace('   ', ' ').replace('  ', ' ')
                new_columns.append(clean_name)
        
        df.columns = new_columns
        
        # 2. Remove completely empty columns
        print("   🗑️  Removing empty columns...")
        df = df.dropna(axis=1, how='all')
        
        # 3. Clean the year column (first column)
        print("   📅 Cleaning year column...")
        year_col = df.columns[0]
        df[year_col] = pd.to_numeric(df[year_col], errors='coerce')
        
        # 4. Remove rows with missing years
        df = df.dropna(subset=[year_col])
        
        # 5. Ensure years are integers
        df[year_col] = df[year_col].astype('Int64')
        
        # 6. Clean numeric columns (round excessive precision)
        print("   🔢 Cleaning numeric data...")
        for col in df.columns[1:]:
            # Convert to numeric
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Round to 3 decimal places to remove excessive precision
            if df[col].dtype in ['float64', 'float32']:
                df[col] = df[col].round(3)
        
        # 7. Sort by year
        df = df.sort_values(by=year_col).reset_index(drop=True)
        
        # 8. Remove duplicate years if any
        df = df.drop_duplicates(subset=[year_col], keep='first')
        
        cleaned_data[sheet_name] = df
        
        # Report cleaning results
        new_rows, new_cols = df.shape
        print(f"   ✅ Results:")
        print(f"      • Rows: {orig_rows} → {new_rows} ({new_rows-orig_rows:+d})")
        print(f"      • Columns: {orig_cols} → {new_cols} ({new_cols-orig_cols:+d})")
        print(f"      • Year range: {df[year_col].min()} - {df[year_col].max()}")
        print(f"      • Data density: {((df.notna().sum().sum() / (df.shape[0] * df.shape[1])) * 100):.1f}%")
    
    return cleaned_data

def save_cleaned_data(cleaned_data, output_prefix="cleaned"):
    """
    Save cleaned data in multiple formats
    """
    print(f"\n💾 SAVING CLEANED DATA")
    print("=" * 60)
    
    # 1. Save as Excel
    excel_file = f"{output_prefix}_electricity_data.xlsx"
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        for sheet_name, df in cleaned_data.items():
            # Create a clean sheet name for Excel
            clean_sheet_name = sheet_name.replace('/', '_').replace('\\', '_')[:31]  # Excel limit
            df.to_excel(writer, sheet_name=clean_sheet_name, index=False)
    
    print(f"   ✅ Excel file saved: {excel_file}")
    
    # 2. Save as CSV files
    for sheet_name, df in cleaned_data.items():
        csv_file = f"{output_prefix}_{sheet_name.lower().replace(' ', '_')}.csv"
        df.to_csv(csv_file, index=False, encoding='utf-8')
        print(f"   ✅ CSV file saved: {csv_file}")
    
    # 3. Save as JSON (for web use)
    json_data = {}
    for sheet_name, df in cleaned_data.items():
        # Convert to records format
        json_data[sheet_name] = df.to_dict('records')
    
    json_file = f"{output_prefix}_electricity_data.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    print(f"   ✅ JSON file saved: {json_file}")
    
    return excel_file, json_file

def generate_summary_report(cleaned_data):
    """
    Generate a summary report of the cleaned data
    """
    print(f"\n📋 DATA SUMMARY REPORT")
    print("=" * 60)
    
    for sheet_name, df in cleaned_data.items():
        print(f"\n📊 Sheet: '{sheet_name}'")
        print("-" * 30)
        
        # Basic info
        print(f"   📏 Dimensions: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"   📅 Time period: {df.iloc[0, 0]} - {df.iloc[-1, 0]} ({df.iloc[-1, 0] - df.iloc[0, 0] + 1} years)")
        
        # Column summary
        print(f"   📊 Columns:")
        for i, col in enumerate(df.columns):
            if i == 0:
                print(f"      {i+1:2d}. {col} (Year column)")
            else:
                non_zero = (df[col] > 0).sum()
                total_vals = df[col].notna().sum()
                print(f"      {i+1:2d}. {col} ({non_zero}/{total_vals} non-zero values)")
        
        # Data quality metrics
        missing_data = df.isna().sum().sum()
        total_cells = df.shape[0] * df.shape[1]
        completeness = ((total_cells - missing_data) / total_cells) * 100
        
        print(f"   📈 Data Quality:")
        print(f"      • Completeness: {completeness:.1f}% ({total_cells - missing_data}/{total_cells} cells)")
        print(f"      • Missing values: {missing_data}")
        
        # Sample recent data
        print(f"   🔍 Recent data (last 3 years):")
        for idx in range(max(0, len(df)-3), len(df)):
            year = df.iloc[idx, 0]
            total_col = None
            for col in df.columns:
                if 'toplam' in str(col).lower() and 'termik' not in str(col).lower():
                    total_col = col
                    break
            
            if total_col:
                total_val = df.iloc[idx][total_col]
                print(f"      {year}: Total = {total_val}")

def main():
    # Input file
    input_file = "data/b/b elektrik generjisinin kaynaklara göre kurulu gücü ve üretimi.xlsx"
    
    print("🚀 TURKISH ELECTRICITY DATA CLEANUP TOOL")
    print("=" * 80)
    print(f"Input file: {input_file}")
    print()
    
    # Step 1: Clean the data
    cleaned_data = clean_excel_data(input_file)
    
    # Step 2: Save in multiple formats
    excel_file, json_file = save_cleaned_data(cleaned_data)
    
    # Step 3: Generate summary report
    generate_summary_report(cleaned_data)
    
    print(f"\n{'='*80}")
    print("🎉 CLEANUP COMPLETE!")
    print(f"   📁 Clean Excel file: {excel_file}")
    print(f"   📁 JSON file: {json_file}")
    print(f"   📁 CSV files: cleaned_*.csv")
    print()
    print("💡 The data is now:")
    print("   • Properly formatted with consistent precision")
    print("   • Free of empty columns and problematic headers")
    print("   • Sorted chronologically")
    print("   • Available in multiple formats (Excel, CSV, JSON)")

if __name__ == "__main__":
    main() 