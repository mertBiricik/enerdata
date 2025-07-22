import re
import base64
import sys

def generate_base64_from_logo():
    """Generate base64 string from logo.jpg file"""
    try:
        with open('logo.jpg', 'rb') as f:
            logo_data = f.read()
        base64_string = base64.b64encode(logo_data).decode('utf-8')
        return f"data:image/jpeg;base64,{base64_string}"
    except FileNotFoundError:
        print("Warning: logo.jpg not found. Using placeholder.")
        return "__BASE64_LOGO_PLACEHOLDER__"

def restore_base64_to_file(file_path):
    """Restore base64 logo data to HTML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Generate base64 data from logo.jpg
    base64_data = generate_base64_from_logo()
    
    # Pattern to match the placeholder
    pattern = r"(logo\.src = ')__BASE64_LOGO_PLACEHOLDER__(')"
    
    # Replace placeholder with actual base64 data
    modified_content = re.sub(pattern, f"\\1{base64_data}\\2", content)
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    
    print(f"Restored base64 data to {file_path}")

if __name__ == "__main__":
    files = [
        "dataset_a_primary_energy.html",
        "dataset_b_electricity.html", 
        "dataset_c_sectoral_consumption.html"
    ]
    
    for file_path in files:
        try:
            restore_base64_to_file(file_path)
        except Exception as e:
            print(f"Error processing {file_path}: {e}") 