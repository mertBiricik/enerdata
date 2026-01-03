import pandas as pd

def inspect_columns():
    # File 1
    print("\n--- File 1 (Sheet 1971) Columns ---")
    df1 = pd.read_excel('1_birincil_enerjinin_kaynaklara_gore_uretimi_ve_tuketimi.xlsx', sheet_name='1971')
    print(list(df1.columns))
    # Print the row for 'Yerli Üretim (+)'
    row = df1[df1.iloc[:, 0] == 'Yerli Üretim (+)']
    print("\nRow 'Yerli Üretim (+)':")
    print(row.to_string())

    # File 4
    print("\n--- File 4 Columns ---")
    df4 = pd.read_excel('4_yasal_duzenlemeler.xlsx')
    # Find header row like the converter does
    header_row = None
    for idx, row in df4.iterrows():
        if not row.isnull().all():
            header_row = idx
            break
            
    if header_row is not None:
        headers = df4.iloc[header_row].fillna('').astype(str).tolist()
        print(f"Detected Headers at row {header_row}: {headers}")
    else:
        print("No header row found")
        print("Raw Columns:", list(df4.columns))

if __name__ == "__main__":
    inspect_columns()
