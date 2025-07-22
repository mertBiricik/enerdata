# Logo Embedding Script for Energy Dashboard

Python script for embedding logo images directly into HTML files as base64 data URIs, eliminating external file dependencies in chart export functions.

## Purpose

The energy dashboard HTML files contain chart export functionality that loads an external logo file (`logo.jpg`) and draws it on exported chart images. This script:

- Converts logo images to base64 data URIs
- Embeds logos directly into HTML files
- Eliminates external logo file dependencies
- Ensures logos work in offline/restricted environments
- Maintains chart export functionality without file loading issues

## Requirements

- Python 3.6 or higher
- No additional packages required (uses only standard library)

## Usage

### Check Current Status
```bash
python embed_logo.py --status
```

Shows which HTML files exist, whether they have embedded or external logo references, and available logo files.

### Embed Logo in All Files
```bash
python embed_logo.py --logo logo.jpg --all
```

Embeds the specified logo into all dashboard HTML files.

### Embed Logo in Specific Files
```bash
python embed_logo.py --logo logo.png --files dataset_a_primary_energy.html dataset_b_electricity.html
```

Embeds logo only into specified HTML files.

### Revert to External Logo References
```bash
python embed_logo.py --revert
```

Restores original files from backup copies, removing embedded logos.

## Supported Image Formats

- JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`)
- GIF (`.gif`)
- SVG (`.svg`)
- BMP (`.bmp`)
- WebP (`.webp`)

## Target HTML Files

The script automatically processes these files:

### Original Files:
- `dataset_a_primary_energy.html`
- `dataset_b_electricity.html`
- `dataset_c_sectoral_consumption.html`
- `veri_bankasi.html`

### Embedded Data Files:
- `dataset_a_primary_energy_embedded.html`
- `dataset_b_electricity_embedded.html`
- `dataset_c_sectoral_consumption_embedded.html`

## What the Script Does

### Logo Reference Patterns Found:
1. **JavaScript logo loading**: `logo.src = 'logo.jpg'`
2. **HTML img tags**: `<img src="logo.png">`

### Embedding Process:
1. Reads the specified logo image file
2. Converts it to base64 encoding
3. Creates proper data URI with MIME type
4. Finds logo references in HTML files
5. Creates backup files (`.logo_backup` extension)
6. Replaces external references with embedded data URI
7. Reports success/failure for each file

### Data URI Format:
```
data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAAAAAAAD...
```

## Safety Features

- **Automatic Backups**: Creates `.logo_backup` files before modifications
- **Non-destructive**: Original files preserved in backups
- **Revert Capability**: Complete restoration from backups
- **Error Handling**: Graceful handling of missing files or permissions
- **Status Reporting**: Detailed feedback on all operations

## Technical Details

### File Size Considerations:
- Base64 encoding increases file size by ~33%
- A 50KB logo becomes ~67KB when embedded
- Multiple files = multiple copies of embedded logo
- Consider logo optimization before embedding

### Logo Position in Charts:
The chart export functions draw logos at:
- **Position**: Top-right corner
- **Size**: 60x60 pixels  
- **Offset**: 20 pixels from edges

### Browser Compatibility:
Data URIs are supported in all modern browsers and have no compatibility issues.

## Example Workflow

```bash
# 1. Check what's available
python embed_logo.py --status

# 2. Embed your logo
python embed_logo.py --logo company_logo.png --all

# 3. Test chart exports in HTML files

# 4. If needed, revert changes
python embed_logo.py --revert

# 5. Try different logo or settings
python embed_logo.py --logo different_logo.jpg --all
```

## Integration with Chart Export

After embedding, the chart export functions will:

1. Load logo from embedded data URI (no network request)
2. Draw logo on export canvas at specified position
3. Include logo in PNG/JPG downloads
4. Work offline without external file dependencies

## File Structure After Embedding

```
project/
├── embed_logo.py                           # This script
├── logo.jpg                               # Original logo file
├── dataset_a_primary_energy.html          # Updated with embedded logo
├── dataset_a_primary_energy.html.logo_backup  # Backup of original
├── dataset_b_electricity.html             # Updated with embedded logo  
├── dataset_b_electricity.html.logo_backup     # Backup of original
└── (other files...)
```

## Troubleshooting

### Logo Not Found Error:
```bash
❌ Error: Logo file 'logo.jpg' not found
```
**Solution**: Ensure logo file exists in current directory or provide full path.

### No Logo References Found:
```bash
⚠️  No logo references found in dataset_a_primary_energy.html
```
**Solution**: Check if file has chart export functionality or logo loading code.

### Large File Size:
Base64 embedding increases file size. For large logos:
1. Optimize/compress logo before embedding
2. Consider using smaller logo dimensions
3. Use efficient formats (PNG for graphics, JPG for photos)

## Benefits

- **Reliability**: No broken logo links in exports
- **Offline Support**: Works without internet/network access  
- **Portability**: Single HTML files contain everything needed
- **Performance**: No additional HTTP requests for logo loading
- **Simplicity**: No external file management required 