# HTML Data Manager for Energy Dashboard

This Python script helps you prepare your energy dashboard HTML files for WordPress deployment and revert them back to the original structure when needed.

## 🎯 Purpose

WordPress doesn't always handle external JavaScript files well in custom HTML blocks. This script:
- **Embeds** external JS data directly into HTML files for WordPress deployment
- **Reverts** embedded files back to the original external JS structure
- **Protects** styling from WordPress theme interference with `!important` CSS rules

## 📋 Requirements

- Python 3.6 or higher
- No additional packages required (uses only standard library)

## 🚀 Usage

### Check Current Status
```bash
python html_data_manager.py status
```

### Embed Data for WordPress
```bash
python html_data_manager.py embed
```

This will:
- Create `*_embedded.html` files with data embedded
- Add WordPress-safe CSS styling with `!important` rules
- Wrap content in `.energy-dashboard-container` for style isolation
- Create `.backup` files of originals
- Make files ready for WordPress Custom HTML blocks

### Revert to Original Structure
```bash
python html_data_manager.py revert
```

This will:
- Restore original files from backups
- Remove embedded versions
- Clean up backup files
- Return to external JS file structure

## 📁 File Structure

### Before Embedding (Original):
```
dataset_a_primary_energy.html      # Uses <script src="data/a/data_a_embedded.js">
dataset_b_electricity.html         # Uses <script src="data/b/data_b_embedded.js">
dataset_c_sectoral_consumption.html # Uses <script src="data/C/c_embedded_data.js">
```

### After Embedding:
```
dataset_a_primary_energy.html              # Original (backed up)
dataset_a_primary_energy.html.backup       # Backup of original
dataset_a_primary_energy_embedded.html     # WordPress-ready version

dataset_b_electricity.html                 # Original (backed up)
dataset_b_electricity.html.backup          # Backup of original
dataset_b_electricity_embedded.html        # WordPress-ready version

dataset_c_sectoral_consumption.html        # Original (backed up)
dataset_c_sectoral_consumption.html.backup # Backup of original
dataset_c_sectoral_consumption_embedded.html # WordPress-ready version
```

## 🎨 WordPress Integration

### For WordPress Deployment:
1. Run `python html_data_manager.py embed`
2. Copy content from `*_embedded.html` files
3. Paste into WordPress **Custom HTML blocks**
4. The embedded files include WordPress-safe styling that won't be overridden

### WordPress-Safe Features:
- All styles use `!important` to prevent theme interference
- Content wrapped in `.energy-dashboard-container` for isolation
- Font families, colors, and layouts protected
- Canvas elements properly sized for responsive design

## 🔧 What the Script Does

### Embedding Process:
1. **Reads** external JS data files (e.g., `data/a/data_a_embedded.js`)
2. **Replaces** `<script src="...">` tags with inline `<script>` containing data
3. **Adds** WordPress-safe CSS styling to `<head>`
4. **Wraps** content in protective container div
5. **Creates** backup of original files
6. **Generates** `*_embedded.html` files ready for WordPress

### Reversion Process:
1. **Restores** original files from `.backup` copies
2. **Removes** embedded versions
3. **Cleans up** backup files
4. **Returns** to external JS file structure

## 🛡️ Safety Features

- **Automatic backups** before any modifications
- **Non-destructive** operations (originals preserved)
- **Error handling** for missing files
- **UTF-8 encoding** support for international characters
- **Detailed logging** of all operations

## 📝 Example Workflow

```bash
# Check current status
python html_data_manager.py status

# Create WordPress-ready files
python html_data_manager.py embed

# Upload *_embedded.html content to WordPress

# Later, when you need to edit locally:
python html_data_manager.py revert

# Make your changes to original files

# Re-embed for WordPress update:
python html_data_manager.py embed
```

## ⚠️ Important Notes

- Always run `status` first to check file availability
- Use `*_embedded.html` files ONLY for WordPress
- Keep original files for local development
- The script handles Turkish characters properly with UTF-8 encoding
- WordPress-safe CSS ensures consistent appearance across themes

## 🎉 Benefits

- **Easy WordPress deployment** without external file dependencies
- **Style protection** from WordPress theme interference  
- **Reversible process** for seamless development workflow
- **Automated backups** prevent data loss
- **Single command** operation for both embedding and reverting 