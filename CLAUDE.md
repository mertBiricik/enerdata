# Enerdata Project - AI Assistant Guidelines

## Project Overview

This is a comprehensive data visualization and analysis system for Turkish energy sector data. The system converts Excel data files into interactive HTML dashboards with charts, filters, and document catalogs.

## System Architecture

### Core Components
- **Excel Source Files**: Raw data in `.xlsx` format (files 1-7)
- **Conversion Engine**: `excel_to_html_converter.py` - Python script that processes Excel files
- **HTML Dashboards**: Interactive web interfaces with Chart.js visualizations
- **Template System**: Unified template structure for consistent styling
- **Backup System**: `backup_html/` directory preserves original working versions

### File Structure
```
enerdata/
├── excel_to_html_converter.py    # Main conversion script
├── unified_document_template.html # Template for document catalogs (files 5-7)
├── backup_html/                  # Original working HTML files
├── [1-7]_*.xlsx                  # Source Excel data files
├── [1-7]_*.html                  # Generated dashboard files
└── CONVERSION_SUMMARY.md         # Technical documentation
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
- **File 6**: Development plans
- **File 7**: EU progress reports
- **Features**: Document search, category filtering, year filtering, metadata display

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
- **Flexible Parsing**: Adapts to different Excel structures and naming conventions
- **Link Processing**: Automatically fixes incomplete URLs (www. → https://www.)
- **Error Handling**: Graceful degradation for missing or malformed data
- **Text Cleaning**: `clean_text_for_json()` function prevents JSON syntax errors by removing line breaks, carriage returns, and tabs
- **Data Variable Consistency**: All document files (4-7) use `embeddedData` variable for unified template compatibility

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
- **Root cause**: Raw Excel text contains unescaped line breaks, quotes, and special characters
- **Solution implemented**: The `clean_text_for_json()` function in converter handles text cleaning automatically
- **Testing**: After regenerating files, check browser console for "SyntaxError" messages

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
2. Check converter includes `embeddedData` pattern (line ~332 in excel_to_html_converter.py)
3. Regenerate with: `python excel_to_html_converter.py 4_yasal_duzenlemeler.xlsx`
4. Verify file 4 uses `embeddedData` variable: `grep embeddedData 4_yasal_duzenlemeler.html`