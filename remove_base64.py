import re
import sys

def remove_base64_from_file(file_path):
    """Remove base64 logo data from HTML file and replace with placeholder"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match the base64 logo assignment
    pattern = r"(logo\.src = ')data:image/jpeg;base64,[^']+(')"
    
    # Replace with placeholder
    modified_content = re.sub(pattern, r"\1__BASE64_LOGO_PLACEHOLDER__\2", content)
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    
    print(f"Removed base64 data from {file_path}")

if __name__ == "__main__":
    files = [
        "dataset_a_primary_energy.html",
        "dataset_b_electricity.html", 
        "dataset_c_sectoral_consumption.html"
    ]
    
    for file_path in files:
        try:
            remove_base64_from_file(file_path)
        except Exception as e:
            print(f"Error processing {file_path}: {e}") 