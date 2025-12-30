# Enerdata Project - AI Assistant Guidelines

## Project Overview

This is a comprehensive data visualization and analysis system for Turkish energy sector data. The system converts Excel data files into interactive HTML dashboards with charts, filters, and document catalogs.

## System Architecture

### Core Components
- **Excel Source Files**: Raw data in `.xlsx` format (files 1-7)
- **Conversion Engine**: `excel_to_html_converter.py` - Python script with multi-format detection and special processing functions
- **HTML Dashboards**: Interactive web interfaces with Chart.js visualizations and document catalogs
- **Template System**: Unified template structure with intelligent field categorization and beautiful labeling
- **Backup System**: `backup_html/` directory preserves original working versions
- **WordPress Integration**: Static HTML links to WordPress media files for seamless Excel downloads

### File Structure
```
enerdata/
├── excel_to_html_converter.py    # Main conversion script
├── unified_document_template.html # Template for document catalogs (files 5-7)
├── backup_html/                  # Original working HTML files
├── [1-7]_*.xlsx                  # Source Excel data files
├── [1-7]_*.html                  # Generated dashboard files
└── CLAUDE.md                     # AI Assistant guidelines and technical documentation
```

## Data Categories

### Chart-Based Dashboards (Files 1-3)
- **File 1**: Primary energy production and consumption by sources
- **File 2**: Electricity generation capacity and production by sources  
- **File 3**: Electricity generation and sectoral consumption
- **Features**: Interactive charts, year range sliders, category filtering, data export

### Document Catalogs (Files 4-7)
- **File 4**: Legal regulations (282+ documents) 
- **File 5**: Strategy and policy documents
- **File 6**: Development plans (with multi-row Excel data consolidation)
- **File 7**: EU progress reports
- **Features**: Document search, category filtering, year filtering, metadata display, comprehensive Excel data inclusion
- **Special Processing**: File 6 uses `process_kalkinma_planlari_excel()` for multi-row data consolidation

## Technical Implementation

### Conversion Process
1. **Excel Analysis**: Multi-format detection (year-based sheets, year columns, document catalogs)
2. **Data Processing**: Handles Turkish characters, missing data, complex structures
3. **Template Selection**: Automatic template choice based on file type
4. **HTML Generation**: JavaScript data embedding with proper encoding
5. **Link Validation**: Automatic protocol addition for web links

### Template System
- **Unified Template**: Single template for document files (4-7) ensures consistency using `embeddedData` variable
- **Backup Templates**: Original HTML files for chart-based dashboards (1-3)
- **Responsive Design**: Works on desktop and mobile devices
- **Professional Styling**: Consistent color scheme and typography

### Data Handling
- **Multi-language Support**: Handles Turkish characters and field names
- **Flexible Parsing**: Adapts to different Excel structures and naming conventions (year-based sheets, years as rows/columns, document catalogs)
- **Link Processing**: Automatically fixes incomplete URLs (www. → https://www.)
- **Error Handling**: Graceful degradation for missing or malformed data
- **Text Cleaning**: Enhanced `clean_text_for_json()` function prevents JSON syntax errors by removing all control characters
- **Multi-row Processing**: Special handling for Excel files with content spanning multiple rows (File 6)
- **Field Categorization**: Intelligent separation of metadata vs content fields with beautiful labeling
- **Data Variable Consistency**: All document files (4-7) use `embeddedData` variable for unified template compatibility
- **Title Standardization**: All files use clean Turkish titles without numbers for professional appearance

## WordPress Integration

### Excel Download Implementation
- **Static HTML Links**: Direct `<a href="..." download>` tags with WordPress media URLs
- **No JavaScript Processing**: Pure browser-native download handling to preserve original Excel formatting
- **Button Text**: "📄 Excel'e Erişim" (Excel Access)
- **Configurable WordPress URLs**: Set via environment variable `EXCEL_URL_BASE` (e.g., `http://enerjiveri.khas.edu.tr/wp-content/uploads/2025/12/`). Defaults to December 2025 if not provided.
- **Template Placeholder**: `{{EXCEL_URL}}` replaced during conversion with file-specific URLs

### Template Processing
- **Automatic URL Assignment**: Converter sets correct WordPress URL based on output filename
- **File Mapping**:
  - File 4: `4_yasal_duzenlemeler.xlsx`
  - File 5: `5_strateji_ve_politika_belgeleri.xlsx`
  - File 6: `6_kalkinma_planlari.xlsx`
  - File 7: `7_ab_ilerleme_raporlari.xlsx`

### WordPress Deployment
- **Copy-Paste Ready**: HTML files can be directly pasted into WordPress custom HTML blocks
- **No Server Dependencies**: All functionality works client-side
- **Cross-Browser Compatible**: Standard HTML/CSS/JavaScript with no special requirements

## Development Guidelines

### Code Standards
- Use descriptive variable names in English
- Handle Turkish characters properly with UTF-8 encoding
- Implement comprehensive error handling
- Log conversion progress and issues
- Maintain backward compatibility with existing data

### File Naming Conventions
- Excel files: `[number]_descriptive_name.xlsx`
- HTML files: `[number]_descriptive_name.html`
- Template files: `*_template.html`
- Backup files: `backup_html/[original_name].html`

### Data Processing Rules
1. **Always backup original HTML files** before modifications
2. **Preserve original functionality** when updating templates
3. **Test with Turkish characters** and special formatting
4. **Validate all external links** during processing
5. **Maintain consistent aesthetics** across file types

## Troubleshooting

### Common Issues
- **Missing data display**: Check JavaScript data embedding patterns
- **Broken links**: Verify protocol (https://) is included
- **Template selection errors**: Ensure unified template exists and is accessible
- **Character encoding**: Use UTF-8 for all file operations
- **Chart rendering**: Verify Chart.js library is loaded correctly
- **JavaScript syntax errors**: Usually caused by unescaped line breaks, quotes, or special characters in JSON data
- **Wrong data variable**: Files 4-7 use `embeddedData`, backup templates may use legacy variables like `embeddedYasalData`

### Debug Process
1. Check converter logs for processing errors
2. Validate Excel file structure and data
3. Verify template file availability
4. Test HTML output in browser
5. Check browser console for JavaScript errors
6. **For JavaScript errors**: Check data variable names match template expectations
7. **For file 4 specifically**: Ensure it uses unified template with `embeddedData` variable, not corrupted backup template

## Maintenance Tasks

### Regular Updates
- **Excel data refresh**: Re-run converter when source files change
- **Template updates**: Modify unified template for styling improvements
- **Link validation**: Periodically check external document links
- **Performance optimization**: Monitor dashboard loading times

### Version Control
- Commit changes with descriptive messages
- Tag releases for major updates
- Maintain development branch for testing
- Document breaking changes in commit messages

## Security Considerations

- **Input validation**: Sanitize Excel data during processing
- **XSS prevention**: Escape user-generated content in HTML output
- **File permissions**: Restrict write access to conversion script
- **External links**: Validate URLs before embedding in HTML
- **Data privacy**: Ensure no sensitive information in public repositories

## Performance Optimization

### Loading Speed
- Minimize JavaScript data size where possible
- Use efficient chart rendering options
- Implement lazy loading for large datasets
- Compress images and assets

### Browser Compatibility
- Test with major browsers (Chrome, Firefox, Safari, Edge)
- Ensure mobile responsiveness
- Graceful degradation for older browsers
- Accessibility compliance (ARIA labels, keyboard navigation)

## Future Enhancements

### Planned Features
- Real-time data updates from external APIs
- Advanced filtering and search capabilities
- Data comparison tools across years
- Export functionality for charts and data
- Multi-language interface support

### Technical Improvements
- Database integration for dynamic data
- API endpoints for programmatic access
- Automated testing suite
- Performance monitoring
- User analytics integration

---

## AI Assistant Instructions

When working with this project:

1. **Always backup original files** before making changes
2. **Test thoroughly** with Turkish data and special characters
3. **Maintain consistency** across all dashboards and templates
4. **Document changes** clearly in commit messages
5. **Preserve functionality** while improving aesthetics or performance
6. **Consider mobile users** in all design decisions
7. **Validate external links** and data integrity
8. **Use the conversion script** rather than manual HTML editing
9. **Keep templates minimal** and focused on essential functionality
10. **Prioritize user experience** over technical complexity

## Critical Technical Notes (MUST READ)

### File 4 Special Handling
- **ALWAYS use unified template**: File 4 (`4_yasal_duzenlemeler.xlsx`) MUST use `unified_document_template.html`
- **Data variable**: Uses `embeddedData` variable, NOT `embeddedYasalData` from corrupted backup
- **Common error**: If file 4 shows "Belgeler yükleniyor" (loading documents) but no data appears, check that:
  1. Template selection logic correctly chooses unified template for file 4
  2. Converter includes `embeddedData` pattern in replacement patterns
  3. No corrupted backup template is being used

### Data Variable Pattern Matching
The converter must include ALL these patterns for proper data embedding:
```python
patterns = [
    (r'const embeddedDataA = \[[\s\S]*?\];', lambda: f'const embeddedDataA = {js_data_str};'),
    (r'const embeddedDataB = \[[\s\S]*?\];', lambda: f'const embeddedDataB = {js_data_str};'),
    (r'const embeddedDataC = \[[\s\S]*?\];', lambda: f'const embeddedDataC = {js_data_str};'),
    (r'const embeddedData = \[[\s\S]*?\];', lambda: f'const embeddedData = {js_data_str};'),  # CRITICAL for files 4-7
    (r'const embeddedYasalData = \[[\s\S]*?\];', lambda: f'const embeddedYasalData = {js_data_str};'),  # Legacy backup only
]
```

### JSON Syntax Error Prevention
- **ALWAYS use `clean_text_for_json()`**: All text data must be cleaned before JSON serialization
- **Root cause**: Raw Excel text contains unescaped line breaks, quotes, and control characters
- **Enhanced solution**: The `clean_text_for_json()` function removes all control characters (\\x00-\\x1f\\x7f-\\x9f)
- **Multi-row processing**: Avoid adding literal line breaks (`\\n\\n`) when consolidating multi-row content
- **Testing**: After regenerating files, check browser console for "SyntaxError" messages

### File 6 Multi-Row Processing
- **Special function**: Uses `process_kalkinma_planlari_excel()` for complex Excel structure
- **Data consolidation**: Combines content from multiple Excel rows into single document entries
- **Field mapping**: Col_5 → "Detaylar ve Analiz", Col_7 → "Çevresel Boyut"
- **Space separation**: Multi-row content joined with spaces, not line breaks
- **Template integration**: Unified template recognizes Col_5 and Col_7 as content fields

### Template File Requirements
```
enerdata/
├── unified_document_template.html  # MUST exist for files 4-7
├── backup_html/                   # Original templates for files 1-3
│   ├── 1_*.html                   # Chart templates only
│   ├── 2_*.html
│   └── 3_*.html
└── [generated files]
```

### Disaster Recovery
If file 4 breaks again:
1. Verify `unified_document_template.html` exists and is not corrupted
2. Check converter includes `embeddedData` pattern (see replacement patterns in `create_html_from_template`)
3. Regenerate with: `python excel_to_html_converter.py 4_yasal_duzenlemeler.xlsx`
4. Verify file 4 uses `embeddedData` variable: `grep embeddedData 4_yasal_duzenlemeler.html`

## Operational Update Steps (New Datasets)

1. Place the updated `.xlsx` files into the project root with canonical names (1–7).
2. Set the WordPress upload base (if changed):
   - Linux: `export EXCEL_URL_BASE='http://enerjiveri.khas.edu.tr/wp-content/uploads/YYYY/MM/'`
3. Regenerate all outputs:
   - `python3 excel_to_html_converter.py`
4. Validate:
   - For files 4–7, ensure `embeddedData` is present in HTML.
   - Load locally with: `python3 -m http.server 8000` and open each HTML.
5. Optional QA:
   - `python3 screenshot_analyzer.py` to capture headless screenshots.