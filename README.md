# Enerji Tüketimi Verisi (Energy Consumption Data Visualization)

## Overview

This project is an interactive web-based data visualization tool for exploring Turkey's energy production, consumption, and sectoral breakdowns from 1923 to 2023. Inspired by the style and usability of [Our World in Data](https://ourworldindata.org), it allows users to:

- View energy data as a table, line chart, or bar chart.
- Filter by year range and by data series (e.g., Net Production, Imports, Exports, sectoral consumption).
- Download the full dataset or any filtered subset as CSV.

All data is embedded and processed client-side for maximum transparency and reproducibility.

---

## Features

- **Interactive Filters:**  
  - Year range selection via slider and numeric inputs (used for both line and bar charts).
  - Multi-select for data series (categories/sectors).
  - Quick "Select All" and "Deselect All" buttons for series.

- **Tabbed Visualization:**  
  - **Table:** See raw data for selected years and series. The first column ("Kategori") is always visible (sticky) when scrolling horizontally. Odd and even rows are striped for readability.
  - **Line Chart:** Visualize trends over time for any combination of series, using a vibrant Material Design color palette.
  - **Bar Chart:** Compare values across series for a selected year range. Users can toggle between displaying the sum or average for each series over the selected range.

- **Data Download & Export:**  
  - Download the entire dataset as CSV.
  - Download the currently filtered data as CSV.
  - Export charts as PNG and JPG (with white background for JPG).
  - Export charts as TikZ code for use in LaTeX documents.

- **Responsive UI & Turkish Localization:**  
  - Clean, modern design with improved Turkish labels (e.g., "Temsil Türü", "Filtrelenmiş Veri").
  - Works on desktop and mobile.

---

## Data Sources & Structure

### Main Data

- **File:** Embedded in `index.html` as `embeddedRawData` (also available in `embedded_data.js`).
- **Source:** Originally from `source.xlsx` and `1923-2023.csv`.
- **Categories:**  
  - Top-level: Net Üretim (Net Production), İthalat (+) (Imports), İhracat (-) (Exports), Elektrik Arzı (Electricity Supply), etc.
  - Sectoral: Gıda (Food), Tekstil (Textile), Kimya-Petrokimya (Chemicals), Ulaştırma (Transport), etc.
- **Years:** 1923–2023 (not all series have data for all years).
- **Special Values:**  
  - Numbers in parentheses (e.g., `(100)`) indicate values highlighted in red in the original Excel (often negative or special cases).

### Category Metadata

- **File:** `categories.csv`
- **Purpose:** Maps top-level and sub-categories for sectoral breakdowns.

### Data Pipeline

- **Excel to JS:**  
  - `excel_to_js.py` reads `source.xlsx` and outputs `embedded_data.js`, preserving red/parenthesized values.
- **CSV to JS:**  
  - `csv_to_js.py` reads `1923-2023.csv` and outputs `embedded_data.js`.

---

## How It Works

### 1. Data Embedding

All data is embedded as a JavaScript array (`embeddedRawData`) in `index.html` for fast, offline access and reproducibility.

### 2. UI & Visualization

- **Filters:**  
  - Year range is controlled by a noUiSlider and numeric inputs.
  - Data series are selected via checkboxes, auto-populated from the data.

- **Tabs:**  
  - Switch between Table, Line Chart, and Bar Chart views.

- **Charts:**  
  - Powered by [Chart.js](https://www.chartjs.org/).
  - Each series gets a unique color.
  - Bar chart allows year selection independent of the main year range.

- **Download:**  
  - "Tam Veri (CSV)" downloads the full dataset.
  - "Filtrelenen Veri (CSV)" downloads only the data currently shown in the table.

### 3. Data Download

- CSVs are generated client-side, matching the current filter state or the full dataset.

---

## File Structure

```
.
├── index.html              # Main app, all logic and data embedded
├── embedded_data.js        # (Optional) Standalone JS data array, generated from Excel/CSV
├── source.xlsx             # Original Excel data source
├── 1923-2023.csv           # Main CSV data source
├── categories.csv          # Category/subcategory mapping
├── excel_to_js.py          # Script: Excel to JS data array
├── csv_to_js.py            # Script: CSV to JS data array
├── code_analysis_report.md # (For reference) Analysis of requirements and code
├── data-section-requirements.md # (For reference) Project requirements
```

---

## How to Use

### As a User

1. **Open `index.html` in your browser.**
2. Use the filters at the top to select year range and data series.
3. Switch between Table, Line Chart, and Bar Chart tabs.
4. Use the download buttons to export data as CSV.

### As a Developer

#### To Update Data

1. **Edit `source.xlsx` or `1923-2023.csv`** with new data.
2. Run the appropriate script:
   - For Excel:  
     ```
     python excel_to_js.py
     ```
   - For CSV:  
     ```
     python csv_to_js.py
     ```
3. Copy the contents of the new `embedded_data.js` into the `<script>` section of `index.html` (or include as a separate file).

#### To Change Categories

- Edit `categories.csv` to update category/subcategory mappings.

---

## Requirements

- No server required; works as a static HTML file.
- Modern browser (Chrome, Firefox, Edge, Safari).
- [Chart.js](https://cdn.jsdelivr.net/npm/chart.js) and [noUiSlider](https://cdn.jsdelivr.net/npm/nouislider) are loaded via CDN.

---

## Reference & Design

- **Design inspired by:** [Our World in Data](https://ourworldindata.org/grapher/global-energy-substitution)
- **Requirements:** See `data-section-requirements.md` for full details.

---

## Extending & Customizing

- **Add new data series:**  
  - Update your data source and regenerate `embedded_data.js`.
- **Change color palette:**  
  - Edit the `getRandomColor()` function in the JS section of `index.html`.
- **Add new charts or filters:**  
  - Extend the JavaScript in `index.html` as needed.

---

## License

This project is open for educational and non-commercial use.  
Data sources should be cited as appropriate.

---

## Contact

For questions or contributions, please open an issue or contact the project maintainer.

---

**Context7**:  
This README was generated with full code and data context using Context7, ensuring all instructions and explanations are accurate and actionable. 