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
- **Unified Template**: Single template for document files (5-7) ensures consistency
- **Backup Templates**: Original HTML files for chart-based dashboards (1-3, 4)
- **Responsive Design**: Works on desktop and mobile devices
- **Professional Styling**: Consistent color scheme and typography

### Data Handling
- **Multi-language Support**: Handles Turkish characters and field names
- **Flexible Parsing**: Adapts to different Excel structures and naming conventions
- **Link Processing**: Automatically fixes incomplete URLs (www. → https://www.)
- **Error Handling**: Graceful degradation for missing or malformed data

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

### Debug Process
1. Check converter logs for processing errors
2. Validate Excel file structure and data
3. Verify template file availability
4. Test HTML output in browser
5. Check browser console for JavaScript errors

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