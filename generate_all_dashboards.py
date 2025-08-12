#!/usr/bin/env python3
"""
Master script to generate all dashboard HTML files from Excel data
Generates files 1, 2, 3 (dashboards) and 4, 5, 6, 7 (qualitative) from Excel sources
"""

import pandas as pd
import json
import os
from pathlib import Path

def discover_excel_files(directory):
    """Discover all Excel files in a directory and return them with their actual filenames"""
    if not os.path.exists(directory):
        return []
    
    files = []
    for filename in os.listdir(directory):
        if filename.endswith('.xlsx') and not filename.startswith('~'):
            files.append({
                'filename': filename,
                'path': os.path.join(directory, filename),
                'number': filename.split('.')[0] if '.' in filename else '0'
            })
    
    # Sort by the number prefix
    files.sort(key=lambda x: int(x['number']) if x['number'].isdigit() else 999)
    return files

def read_excel_to_json(excel_path, sheet_name=None, is_qualitative=False):
    """Read Excel file and convert to JSON format"""
    try:
        # For qualitative files, use row 1 as header and skip first column if empty
        if is_qualitative:
            df = pd.read_excel(excel_path, sheet_name=sheet_name, header=1)
            # Drop first column if it's unnamed or mostly empty
            if len(df.columns) > 0 and df.columns[0].startswith('Unnamed:') and df.iloc[:, 0].isna().sum() > len(df) * 0.8:
                df = df.drop(df.columns[0], axis=1)
        else:
            if sheet_name:
                df = pd.read_excel(excel_path, sheet_name=sheet_name)
            else:
                df = pd.read_excel(excel_path)
        
        # Convert datetime objects to strings
        for col in df.columns:
            if df[col].dtype == 'datetime64[ns]':
                df[col] = df[col].dt.strftime('%Y-%m-%d').replace('NaT', '')
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].astype(str).replace('NaT', '').replace('nat', '')
        
        # Convert NaN to None for JSON serialization
        df = df.where(pd.notnull(df), None)
        
        # Handle any remaining non-serializable objects
        result = []
        for _, row in df.iterrows():
            row_dict = {}
            for col, value in row.items():
                if pd.isna(value):
                    row_dict[col] = None
                elif hasattr(value, 'timestamp'):  # datetime-like objects
                    row_dict[col] = str(value)
                else:
                    row_dict[col] = value
            result.append(row_dict)
        
        return result
    except Exception as e:
        print(f"Error reading {excel_path}: {e}")
        return []

def generate_dashboard_html(title, data_var_name, data_json, y_axis_label="Değer", chart_title="Enerji Verileri"):
    """Generate complete dashboard HTML with embedded data and functionality"""
    
    html_template = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/nouislider@15.7.1/dist/nouislider.min.css">
    <script src="https://cdn.jsdelivr.net/npm/nouislider@15.7.1/dist/nouislider.min.js"></script>
    <style>
        * {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important; 
            box-sizing: border-box;
        }}
        
        body {{ 
            margin: 0; 
            padding: 20px;
            background: white;
            color: #333; 
            line-height: 1.6;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        }}
        
        .main-container {{
            max-width: 1600px;
            width: 95%;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        }}
        
        .header {{
            background: linear-gradient(135deg, #006400 0%, #228B22 100%);
            color: white;
            padding: 2rem;
            text-align: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            position: relative;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.2rem;
            font-weight: 600;
            color: white !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        }}
        
        .logo {{
            position: absolute;
            top: 20px;
            right: 20px;
            width: 80px;
            height: 80px;
            background: url('data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCABQAFADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAWX/aAAwDAQACEQMRAD8A+f6KKK0AKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA//9k=') center/contain no-repeat;
            border-radius: 8px;
            background-color: rgba(255,255,255,0.1);
        }}
        
        .content-layout {{
            display: flex;
            min-height: 600px;
        }}
        
        .filters-panel {{
            width: 300px;
            background: #f8f9fa;
            padding: 2rem;
            border-right: 1px solid #e9ecef;
        }}
        
        .filter-group {{
            margin-bottom: 2rem;
        }}
        
        .filter-group label {{
            display: block;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #495057;
        }}
        
        .year-range-container {{
            margin-bottom: 1rem;
        }}
        
        #yearRangeSlider {{
            margin: 1rem 0;
        }}
        
        .year-inputs {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .year-inputs input {{
            width: 80px;
            padding: 0.25rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            text-align: center;
        }}
        
        .series-checkboxes {{
            max-height: 300px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 0.5rem;
        }}
        
        .series-checkboxes div {{
            display: flex;
            align-items: center;
            padding: 0.25rem;
            gap: 0.5rem;
        }}
        
        .series-checkboxes input[type="checkbox"] {{
            margin: 0;
        }}
        
        .search-input {{
            width: 100%;
            padding: 0.5rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-bottom: 0.5rem;
        }}
        
        .filter-buttons {{
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }}
        
        .filter-buttons button {{
            flex: 1;
            padding: 0.5rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            background: white;
            cursor: pointer;
        }}
        
        .filter-buttons button:hover {{
            background: #f8f9fa;
        }}
        
        .download-buttons {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            margin-top: 1rem;
        }}
        
        .download-buttons button {{
            padding: 0.5rem;
            border: 1px solid #006400;
            border-radius: 4px;
            background: #006400;
            color: white;
            cursor: pointer;
        }}
        
        .download-buttons button:hover {{
            background: #228B22;
        }}
        
        .content-panel {{
            flex: 1;
            padding: 2rem;
        }}
        
        .tabs {{
            display: flex;
            border-bottom: 2px solid #e9ecef;
            margin-bottom: 2rem;
        }}
        
        .tab-button {{
            padding: 1rem 2rem;
            background: none;
            border: none;
            border-bottom: 3px solid transparent;
            cursor: pointer;
            font-weight: 600;
            color: #495057;
            transition: all 0.3s ease;
        }}
        
        .tab-button.active {{
            color: #006400;
            border-bottom-color: #006400;
        }}
        
        .tab-button:hover {{
            color: #228B22;
        }}
        
        .tab-content {{
            display: none;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        .chart-container {{
            position: relative;
            height: 500px;
            margin-bottom: 2rem;
        }}
        
        .calculation-mode {{
            margin-bottom: 1rem;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        
        .calculation-mode label {{
            font-weight: 600;
            margin-bottom: 0.5rem;
            display: block;
        }}
        
        .mode-options {{
            display: flex;
            gap: 1rem;
        }}
        
        .mode-options input[type="radio"] {{
            margin-right: 0.25rem;
        }}
        
        .chart-download {{
            text-align: center;
        }}
        
        .chart-download button {{
            padding: 0.75rem 1.5rem;
            background: #006400;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 600;
        }}
        
        .chart-download button:hover {{
            background: #228B22;
        }}
        
        .table-container {{
            overflow-x: auto;
            border: 1px solid #ddd;
            border-radius: 8px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }}
        
        th, td {{
            padding: 0.75rem;
            text-align: right;
            border-bottom: 1px solid #e9ecef;
        }}
        
        th:first-child, td:first-child {{
            text-align: left;
            position: sticky;
            left: 0;
            background: white;
            font-weight: 600;
        }}
        
        th {{
            background: #f8f9fa;
            font-weight: 600;
            position: sticky;
            top: 0;
        }}
        
        .stats {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            font-size: 0.9rem;
            color: #6c757d;
        }}
    </style>
</head>
<body>
    <div class="main-container">
        <div class="header">
            <div class="logo"></div>
            <h1>{title}</h1>
        </div>
        
        <div class="content-layout">
            <div class="filters-panel">
                <div class="filter-group">
                    <label>Yıl Aralığı</label>
                    <div class="year-range-container">
                        <div id="yearRangeSlider"></div>
                        <div class="year-inputs">
                            <input type="number" id="yearInputStart" min="1972" max="2023" value="1972">
                            <span>-</span>
                            <input type="number" id="yearInputEnd" min="1972" max="2023" value="2023">
                        </div>
                    </div>
                </div>
                
                <div class="filter-group">
                    <label>Veri Serileri</label>
                    <input type="text" id="seriesSearch" class="search-input" placeholder="Kategori ara...">
                    <div class="filter-buttons">
                        <button id="selectAllBtn">Hepsini Seç</button>
                        <button id="deselectAllBtn">Hiçbirini Seçme</button>
                    </div>
                    <div id="seriesCheckboxes" class="series-checkboxes"></div>
                    
                    <div class="download-buttons">
                        <button id="downloadFullData">Tam Veriyi İndir</button>
                        <button id="downloadFilteredData">Filtrelenmiş Veriyi İndir</button>
                    </div>
                </div>
            </div>
            
            <div class="content-panel">
                <div class="tabs">
                    <button class="tab-button active" data-tab="table">Tablo</button>
                    <button class="tab-button" data-tab="line">Çizgi Grafik</button>
                    <button class="tab-button" data-tab="bar">Sütun Grafik</button>
                    <button class="tab-button" data-tab="pie">Pasta Grafik</button>
                </div>
                
                <div id="tableContent" class="tab-content active">
                    <div class="stats">
                        <span id="dataStats">Veri yükleniyor...</span>
                        <span id="yearRange">1972 - 2023</span>
                    </div>
                    <div class="table-container">
                        <table id="dataTable">
                            <thead></thead>
                            <tbody></tbody>
                        </table>
                    </div>
                </div>
                
                <div id="lineContent" class="tab-content">
                    <div class="chart-container">
                        <canvas id="lineChart"></canvas>
                    </div>
                    <div class="chart-download">
                        <button id="downloadLineChart">Çizgi Grafiği İndir</button>
                    </div>
                </div>
                
                <div id="barContent" class="tab-content">
                    <div class="calculation-mode">
                        <label>Hesaplama Türü</label>
                        <div class="mode-options">
                            <input type="radio" id="mode-sum" name="barChartMode" value="sum" checked>
                            <label for="mode-sum">Toplam</label>
                            <input type="radio" id="mode-average" name="barChartMode" value="average">
                            <label for="mode-average">Ortalama</label>
                        </div>
                    </div>
                    <div class="chart-container">
                        <canvas id="barChart"></canvas>
                    </div>
                    <div class="chart-download">
                        <button id="downloadBarChart">Sütun Grafiği İndir</button>
                    </div>
                </div>
                
                <div id="pieContent" class="tab-content">
                    <div class="calculation-mode">
                        <label>Hesaplama Türü</label>
                        <div class="mode-options">
                            <input type="radio" id="pie-mode-sum" name="pieChartMode" value="sum" checked>
                            <label for="pie-mode-sum">Toplam</label>
                            <input type="radio" id="pie-mode-average" name="pieChartMode" value="average">
                            <label for="pie-mode-average">Ortalama</label>
                        </div>
                    </div>
                    <div class="chart-container">
                        <canvas id="pieChart"></canvas>
                    </div>
                    <div class="chart-download">
                        <button id="downloadPieChart">Pasta Grafiği İndir</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
const {data_var_name} = {data_json};
    </script>

    <script>
        // Dashboard functionality
        let currentData = {data_var_name};
        let lineChart, barChart, pieChart;
        let yearRange = [1972, 2023];
        let selectedSeries = new Set();
        let filteredData = [];
        
        // Initialize year range slider
        function initializeYearRange() {{
            const slider = document.getElementById('yearRangeSlider');
            const allYears = getAllYears();
            const minYear = Math.min(...allYears);
            const maxYear = Math.max(...allYears);
            
            yearRange = [minYear, maxYear];
            document.getElementById('yearInputStart').min = minYear;
            document.getElementById('yearInputStart').max = maxYear;
            document.getElementById('yearInputStart').value = minYear;
            document.getElementById('yearInputEnd').min = minYear;
            document.getElementById('yearInputEnd').max = maxYear;
            document.getElementById('yearInputEnd').value = maxYear;
            
            noUiSlider.create(slider, {{
                start: [minYear, maxYear],
                connect: true,
                range: {{
                    'min': minYear,
                    'max': maxYear
                }},
                step: 1,
                format: {{
                    to: function (value) {{
                        return Math.round(value);
                    }},
                    from: function (value) {{
                        return Number(value);
                    }}
                }}
            }});
            
            slider.noUiSlider.on('update', function (values) {{
                yearRange = [parseInt(values[0]), parseInt(values[1])];
                document.getElementById('yearInputStart').value = yearRange[0];
                document.getElementById('yearInputEnd').value = yearRange[1];
                updateAll();
            }});
            
            document.getElementById('yearInputStart').addEventListener('change', function() {{
                const newStart = parseInt(this.value);
                if (newStart <= yearRange[1]) {{
                    yearRange[0] = newStart;
                    slider.noUiSlider.set([newStart, yearRange[1]]);
                }}
            }});
            
            document.getElementById('yearInputEnd').addEventListener('change', function() {{
                const newEnd = parseInt(this.value);
                if (newEnd >= yearRange[0]) {{
                    yearRange[1] = newEnd;
                    slider.noUiSlider.set([yearRange[0], newEnd]);
                }}
            }});
        }}
        
        function getAllYears() {{
            const years = new Set();
            currentData.forEach(item => {{
                Object.keys(item).forEach(key => {{
                    if (key !== 'Kategori' && !isNaN(parseInt(key))) {{
                        years.add(parseInt(key));
                    }}
                }});
            }});
            return Array.from(years).sort((a, b) => a - b);
        }}
        
        function initializeSeriesCheckboxes() {{
            const container = document.getElementById('seriesCheckboxes');
            const searchInput = document.getElementById('seriesSearch');
            
            function renderCheckboxes(dataToShow = currentData) {{
                container.innerHTML = '';
                dataToShow.forEach((item, index) => {{
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.id = `series_${{index}}`;
                    checkbox.value = index;
                    checkbox.checked = selectedSeries.has(index);
                    
                    const label = document.createElement('label');
                    label.htmlFor = `series_${{index}}`;
                    label.textContent = item.Kategori;
                    
                    const div = document.createElement('div');
                    div.appendChild(checkbox);
                    div.appendChild(label);
                    container.appendChild(div);
                    
                    checkbox.addEventListener('change', function() {{
                        if (this.checked) {{
                            selectedSeries.add(index);
                        }} else {{
                            selectedSeries.delete(index);
                        }}
                        updateAll();
                    }});
                }});
            }}
            
            searchInput.addEventListener('input', function() {{
                const searchTerm = this.value.toLowerCase();
                if (searchTerm) {{
                    const filtered = currentData.filter(item => 
                        item.Kategori.toLowerCase().includes(searchTerm)
                    );
                    renderCheckboxes(filtered);
                }} else {{
                    renderCheckboxes();
                }}
            }});
            
            // Initially select all series
            currentData.forEach((_, index) => selectedSeries.add(index));
            renderCheckboxes();
            
            // Select/Deselect all buttons
            document.getElementById('selectAllBtn').addEventListener('click', function() {{
                currentData.forEach((_, index) => selectedSeries.add(index));
                renderCheckboxes();
                updateAll();
            }});
            
            document.getElementById('deselectAllBtn').addEventListener('click', function() {{
                selectedSeries.clear();
                renderCheckboxes();
                updateAll();
            }});
        }}
        
        function getFilteredData() {{
            return currentData.filter((_, index) => selectedSeries.has(index));
        }}
        
        function getYearFilteredData(data) {{
            return data.map(item => {{
                const filteredItem = {{ Kategori: item.Kategori }};
                for (let year = yearRange[0]; year <= yearRange[1]; year++) {{
                    if (item[year.toString()] !== undefined) {{
                        filteredItem[year.toString()] = item[year.toString()];
                    }}
                }}
                return filteredItem;
            }});
        }}
        
        function createTable() {{
            const data = getYearFilteredData(getFilteredData());
            const table = document.getElementById('dataTable');
            const thead = table.querySelector('thead');
            const tbody = table.querySelector('tbody');
            
            if (data.length === 0) {{
                table.innerHTML = '<thead><tr><th>Veri Yok</th></tr></thead>';
                return;
            }}
            
            // Create header
            const years = [];
            for (let year = yearRange[0]; year <= yearRange[1]; year++) {{
                years.push(year);
            }}
            
            thead.innerHTML = '<tr><th>Kategori</th>' + 
                years.map(year => `<th>${{year}}</th>`).join('') + '</tr>';
            
            // Create rows
            tbody.innerHTML = data.map(item => {{
                const values = years.map(year => {{
                    const value = item[year.toString()];
                    return value !== null && value !== undefined ? 
                        (typeof value === 'number' ? value.toLocaleString('tr-TR') : value) : '-';
                }});
                
                return '<tr><td>' + item.Kategori + '</td><td>' + values.join('</td><td>') + '</td></tr>';
            }}).join('');
            
            updateStats();
        }}
        
        function updateStats() {{
            const stats = document.getElementById('dataStats');
            const yearRangeSpan = document.getElementById('yearRange');
            
            stats.textContent = `${{getFilteredData().length}} veri serisi görüntüleniyor`;
            yearRangeSpan.textContent = `${{yearRange[0]}} - ${{yearRange[1]}}`;
        }}
        
        function createLineChart() {{
            const ctx = document.getElementById('lineChart').getContext('2d');
            const data = getYearFilteredData(getFilteredData());
            
            if (lineChart) lineChart.destroy();
            
            const datasets = data.map((item, index) => {{
                const chartData = [];
                for (let year = yearRange[0]; year <= yearRange[1]; year++) {{
                    const value = item[year.toString()];
                    if (value !== null && value !== undefined) {{
                        chartData.push({{ x: year, y: value }});
                    }}
                }}
                
                return {{
                    label: item.Kategori,
                    data: chartData,
                    borderColor: `hsl(${{index * 137.5 % 360}}, 70%, 50%)`,
                    backgroundColor: `hsla(${{index * 137.5 % 360}}, 70%, 50%, 0.1)`,
                    fill: false,
                    tension: 0.1
                }};
            }});
            
            lineChart = new Chart(ctx, {{
                type: 'line',
                data: {{ datasets }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        x: {{
                            type: 'linear',
                            title: {{ display: true, text: 'Yıl' }}
                        }},
                        y: {{
                            title: {{ display: true, text: '{y_axis_label}' }}
                        }}
                    }},
                    plugins: {{
                        legend: {{ display: true, position: 'top' }},
                        title: {{ display: true, text: '{chart_title}' }}
                    }}
                }}
            }});
        }}
        
        function createBarChart() {{
            const ctx = document.getElementById('barChart').getContext('2d');
            const data = getYearFilteredData(getFilteredData());
            const mode = document.querySelector('input[name="barChartMode"]:checked').value;
            
            if (barChart) barChart.destroy();
            
            const chartData = data.map(item => {{
                const values = [];
                for (let year = yearRange[0]; year <= yearRange[1]; year++) {{
                    const value = item[year.toString()];
                    if (value !== null && value !== undefined) {{
                        values.push(value);
                    }}
                }}
                
                let result = 0;
                if (values.length > 0) {{
                    result = mode === 'sum' ? 
                        values.reduce((a, b) => a + b, 0) : 
                        values.reduce((a, b) => a + b, 0) / values.length;
                }}
                
                return {{
                    label: item.Kategori,
                    value: result
                }};
            }}).filter(item => Math.abs(item.value) > 0);
            
            barChart = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: chartData.map(item => item.label),
                    datasets: [{{
                        label: mode === 'sum' ? 'Toplam' : 'Ortalama',
                        data: chartData.map(item => item.value),
                        backgroundColor: chartData.map((_, index) => 
                            `hsla(${{index * 40 % 360}}, 70%, 50%, 0.7)`
                        )
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{
                            title: {{ display: true, text: '{y_axis_label}' }}
                        }}
                    }},
                    plugins: {{
                        legend: {{ display: false }},
                        title: {{ 
                            display: true, 
                            text: `{chart_title} (${{mode === 'sum' ? 'Toplam' : 'Ortalama'}})`
                        }}
                    }}
                }}
            }});
        }}
        
        function createPieChart() {{
            const ctx = document.getElementById('pieChart').getContext('2d');
            const data = getYearFilteredData(getFilteredData());
            const mode = document.querySelector('input[name="pieChartMode"]:checked').value;
            
            if (pieChart) pieChart.destroy();
            
            const chartData = data.map(item => {{
                const values = [];
                for (let year = yearRange[0]; year <= yearRange[1]; year++) {{
                    const value = item[year.toString()];
                    if (value !== null && value !== undefined) {{
                        values.push(value);
                    }}
                }}
                
                let result = 0;
                if (values.length > 0) {{
                    result = mode === 'sum' ? 
                        values.reduce((a, b) => a + b, 0) : 
                        values.reduce((a, b) => a + b, 0) / values.length;
                }}
                
                return {{
                    label: item.Kategori,
                    value: Math.abs(result)
                }};
            }}).filter(item => item.value > 0);
            
            pieChart = new Chart(ctx, {{
                type: 'pie',
                data: {{
                    labels: chartData.map(item => item.label),
                    datasets: [{{
                        data: chartData.map(item => item.value),
                        backgroundColor: chartData.map((_, index) => 
                            `hsla(${{index * 40 % 360}}, 70%, 50%, 0.7)`
                        )
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: true, position: 'right' }},
                        title: {{ 
                            display: true, 
                            text: `{chart_title} Dağılımı (${{mode === 'sum' ? 'Toplam' : 'Ortalama'}})`
                        }}
                    }}
                }}
            }});
        }}
        
        function updateAll() {{
            const activeTab = document.querySelector('.tab-content.active').id;
            
            if (activeTab === 'tableContent') {{
                createTable();
            }} else if (activeTab === 'lineContent') {{
                createLineChart();
            }} else if (activeTab === 'barContent') {{
                createBarChart();
            }} else if (activeTab === 'pieContent') {{
                createPieChart();
            }}
        }}
        
        function initializeTabs() {{
            const tabButtons = document.querySelectorAll('.tab-button');
            const tabContents = document.querySelectorAll('.tab-content');
            
            tabButtons.forEach(button => {{
                button.addEventListener('click', function() {{
                    // Remove active from all
                    tabButtons.forEach(b => b.classList.remove('active'));
                    tabContents.forEach(c => c.classList.remove('active'));
                    
                    // Add active to clicked
                    this.classList.add('active');
                    const targetTab = this.getAttribute('data-tab');
                    document.getElementById(targetTab + 'Content').classList.add('active');
                    
                    // Update content
                    setTimeout(updateAll, 100);
                }});
            }});
        }}
        
        function downloadChart(chartInstance, filename) {{
            if (chartInstance) {{
                const url = chartInstance.toBase64Image();
                const a = document.createElement('a');
                a.href = url;
                a.download = filename;
                a.click();
            }}
        }}
        
        function downloadData(dataToExport, filename) {{
            const years = [];
            for (let year = yearRange[0]; year <= yearRange[1]; year++) {{
                years.push(year);
            }}
            
            const csvContent = [
                ['Kategori', ...years].join(','),
                ...dataToExport.map(item => {{
                    const values = years.map(year => {{
                        const value = item[year.toString()];
                        return value !== null && value !== undefined ? value : '';
                    }});
                    return [item.Kategori, ...values].join(',');
                }})
            ].join('\\n');
            
            const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = filename;
            link.click();
        }}
        
        // Initialize everything
        document.addEventListener('DOMContentLoaded', function() {{
            try {{
                if (!currentData || currentData.length === 0) {{
                    throw new Error('Veri yok');
                }}
                
                initializeYearRange();
                initializeSeriesCheckboxes();
                initializeTabs();
                
                // Chart mode listeners
                document.querySelectorAll('input[name="barChartMode"]').forEach(radio => {{
                    radio.addEventListener('change', createBarChart);
                }});
                
                document.querySelectorAll('input[name="pieChartMode"]').forEach(radio => {{
                    radio.addEventListener('change', createPieChart);
                }});
                
                // Download listeners
                document.getElementById('downloadLineChart').addEventListener('click', () => {{
                    downloadChart(lineChart, 'cizgi_grafigi.png');
                }});
                
                document.getElementById('downloadBarChart').addEventListener('click', () => {{
                    downloadChart(barChart, 'sutun_grafigi.png');
                }});
                
                document.getElementById('downloadPieChart').addEventListener('click', () => {{
                    downloadChart(pieChart, 'pasta_grafigi.png');
                }});
                
                document.getElementById('downloadFullData').addEventListener('click', () => {{
                    downloadData(currentData, 'tam_veri.csv');
                }});
                
                document.getElementById('downloadFilteredData').addEventListener('click', () => {{
                    downloadData(getYearFilteredData(getFilteredData()), 'filtreli_veri.csv');
                }});
                
                // Initialize with table view
                createTable();
                
            }} catch (error) {{
                console.error('Initialization error:', error);
                document.body.innerHTML = '<div style="text-align: center; padding: 50px; font-size: 18px;">Veri yüklenemedi: ' + error.message + '</div>';
            }}
        }});
    </script>
</body>
</html>'''
    
    return html_template

def generate_qualitative_html(title, data_var_name, data_json, doc_type="belgeler"):
    """Generate complete qualitative document HTML with embedded data and functionality"""
    
    html_template = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important; 
            box-sizing: border-box;
        }}
        
        body {{ 
            margin: 0; 
            padding: 20px;
            background: white;
            color: #333; 
            line-height: 1.6;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        }}
        
        .main-container {{
            max-width: 1600px;
            width: 95%;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        }}
        
        .header {{
            background: linear-gradient(135deg, #006400 0%, #228B22 100%);
            color: white;
            padding: 2rem;
            text-align: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            position: relative;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.2rem;
            font-weight: 600;
            color: white !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        }}
        
        .header p {{
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
            opacity: 0.9;
            color: white !important;
        }}
        
        .logo {{
            position: absolute;
            top: 20px;
            right: 20px;
            width: 80px;
            height: 80px;
            background: url('data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCABQAFADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAWX/aAAwDAQACEQMRAD8A+f6KKK0AKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA//9k=') center/contain no-repeat;
            border-radius: 8px;
            background-color: rgba(255,255,255,0.1);
        }}
        
        .controls {{
            padding: 2rem;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .search-filter-row {{
            display: flex;
            gap: 1rem;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }}
        
        .search-box {{
            flex: 1;
            min-width: 300px;
            padding: 0.75rem;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }}
        
        .search-box:focus {{
            outline: none;
            border-color: #006400;
        }}
        
        .filter-select {{
            padding: 0.75rem;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 1rem;
            background: white;
            min-width: 150px;
        }}
        
        .filter-select:focus {{
            outline: none;
            border-color: #006400;
        }}
        
        .year-filter {{
            padding: 0.75rem;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 1rem;
            width: 120px;
        }}
        
        .year-filter:focus {{
            outline: none;
            border-color: #006400;
        }}
        
        .stats-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.95rem;
            color: #6c757d;
        }}
        
        .content {{
            padding: 2rem;
        }}
        
        .loading {{
            text-align: center;
            padding: 3rem;
            font-size: 1.2rem;
            color: #6c757d;
        }}
        
        .no-results {{
            text-align: center;
            padding: 3rem;
            font-size: 1.2rem;
            color: #6c757d;
            background: #f8f9fa;
            border-radius: 8px;
            margin: 1rem 0;
        }}
        
        .documents-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 1.5rem;
        }}
        
        .document-card {{
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .document-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }}
        
        .document-title {{
            font-size: 1.2rem;
            font-weight: 600;
            color: #006400;
            margin-bottom: 1rem;
            line-height: 1.4;
        }}
        
        .document-meta {{
            margin-bottom: 1rem;
        }}
        
        .meta-item {{
            display: flex;
            margin-bottom: 0.5rem;
            align-items: flex-start;
        }}
        
        .meta-label {{
            font-weight: 600;
            color: #495057;
            min-width: 120px;
            margin-right: 0.5rem;
        }}
        
        .meta-value {{
            color: #6c757d;
            flex: 1;
        }}
        
        .energy-content {{
            margin: 1rem 0;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #006400;
        }}
        
        .energy-content h4 {{
            margin: 0 0 0.5rem 0;
            color: #006400;
            font-size: 1rem;
        }}
        
        .energy-items {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}
        
        .energy-item {{
            background: white;
            padding: 0.5rem;
            border-radius: 4px;
            border: 1px solid #e9ecef;
            font-size: 0.9rem;
            line-height: 1.4;
        }}
        
        .access-link {{
            display: inline-block;
            background: #006400;
            color: white !important;
            padding: 0.5rem 1rem;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.9rem;
            transition: background-color 0.3s ease;
            margin-top: 1rem;
        }}
        
        .access-link:hover {{
            background: #228B22;
            text-decoration: none;
        }}
        
        .export-btn {{
            background: #006400;
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }}
        
        .export-btn:hover {{
            background: #228B22;
        }}
    </style>
</head>
<body>
    <div class="main-container">
        <div class="header">
            <div class="logo"></div>
            <h1>{title}</h1>
            <p>Türkiye enerji sektörü {doc_type} arşivi</p>
        </div>
        
        <div class="controls">
            <div class="search-filter-row">
                <input type="text" id="searchBox" class="search-box" placeholder="Belge adı, yazar veya kurum bazında arama yapın...">
                <select id="yearFilter" class="year-filter">
                    <option value="">Tüm Yıllar</option>
                </select>
                <select id="categoryFilter" class="filter-select">
                    <option value="">Tüm Kategoriler</option>
                </select>
                <button id="exportBtn" class="export-btn">CSV İndir</button>
            </div>
            <div class="stats-row">
                <div>
                    <span id="totalCount">Yükleniyor...</span>
                    <span id="filteredCount"></span>
                </div>
                <div>
                    <span id="dateRange"></span>
                </div>
            </div>
        </div>
        
        <div class="content">
            <div class="loading" id="loading">Belgeler yükleniyor...</div>
            <div class="no-results" id="noResults" style="display: none;">
                Arama kriterlerinize uygun belge bulunamadı.
            </div>
            <div class="documents-grid" id="documentsGrid"></div>
        </div>
    </div>

    <script>
const {data_var_name} = {data_json};
    </script>

    <script>
        let allDocuments = [];
        let filteredDocuments = [];
        
        function formatDate(dateStr) {{
            if (!dateStr) return 'Belirtilmemiş';
            return dateStr.toString();
        }}
        
        function extractYear(dateStr) {{
            if (!dateStr) return null;
            const match = dateStr.toString().match(/(\\d{{4}})/);
            return match ? parseInt(match[1]) : null;
        }}
        
        function renderDocuments(documents) {{
            const grid = document.getElementById('documentsGrid');
            const loading = document.getElementById('loading');
            const noResults = document.getElementById('noResults');
            
            loading.style.display = 'none';
            
            if (!documents || documents.length === 0) {{
                grid.style.display = 'none';
                noResults.style.display = 'block';
                return;
            }}
            
            noResults.style.display = 'none';
            grid.style.display = 'block';
            
            const html = documents.map(doc => `
                <div class="document-card">
                    <div class="document-title">${{doc.baslik || 'Başlık belirtilmemiş'}}</div>
                    <div class="document-meta">
                        ${{doc.yazar ? `
                            <div class="meta-item">
                                <span class="meta-label">Yazar:</span>
                                <span class="meta-value">${{doc.yazar}}</span>
                            </div>
                        ` : ''}}
                        ${{doc.basimTarihi ? `
                            <div class="meta-item">
                                <span class="meta-label">Basım Tarihi:</span>
                                <span class="meta-value">${{formatDate(doc.basimTarihi)}}</span>
                            </div>
                        ` : ''}}
                        ${{doc.yayinevi ? `
                            <div class="meta-item">
                                <span class="meta-label">Yayınevi:</span>
                                <span class="meta-value">${{doc.yayinevi}}</span>
                            </div>
                        ` : ''}}
                        ${{doc.basimYeri ? `
                            <div class="meta-item">
                                <span class="meta-label">Basım Yeri:</span>
                                <span class="meta-value">${{doc.basimYeri}}</span>
                            </div>
                        ` : ''}}
                        ${{doc.yayinlayanKurum ? `
                            <div class="meta-item">
                                <span class="meta-label">Yayınlayan Kurum:</span>
                                <span class="meta-value">${{doc.yayinlayanKurum}}</span>
                            </div>
                        ` : ''}}
                    </div>
                    ${{doc.enerjiIcerigi && Array.isArray(doc.enerjiIcerigi) && doc.enerjiIcerigi.length > 0 ? `
                        <div class="energy-content">
                            <h4>Enerji İçeriği:</h4>
                            <div class="energy-items">
                                ${{doc.enerjiIcerigi.map(item => `<span class="energy-item">${{item}}</span>`).join('')}}
                            </div>
                        </div>
                    ` : ''}}
                    ${{(doc.erisimLinki || doc.link) ? `
                        <a href="${{doc.erisimLinki || doc.link}}" target="_blank" class="access-link">
                            🔗 Belgeye Erişim
                        </a>
                    ` : ''}}
                </div>
            `).join('');
            
            grid.innerHTML = html;
        }}
        
        function populateYearFilter() {{
            const years = [...new Set(allDocuments.map(doc => extractYear(doc.basimTarihi)).filter(y => y))].sort((a, b) => b - a);
            const select = document.getElementById('yearFilter');
            
            years.forEach(year => {{
                const option = document.createElement('option');
                option.value = year;
                option.textContent = year;
                select.appendChild(option);
            }});
        }}
        
        function categorizeDocument(doc) {{
            const title = (doc.baslik || '').toLowerCase();
            const author = (doc.yazar || '').toLowerCase();
            const content = title + ' ' + author;
            
            if (content.includes('plan') && content.includes('kalkınma')) {{
                return 'Kalkınma Planları';
            }}
            if (content.includes('strateji') || content.includes('politika')) {{
                return 'Strateji ve Politika Belgeleri';
            }}
            if (content.includes('kanun') || content.includes('yönetmelik') || content.includes('düzenleme')) {{
                return 'Yasal Düzenlemeler';
            }}
            if (content.includes('ab') || content.includes('avrupa') || content.includes('ilerleme')) {{
                return 'AB İlerleme Raporları';
            }}
            if (content.includes('rapor') || content.includes('araştırma')) {{
                return 'Raporlar ve Araştırmalar';
            }}
            return 'Diğer Belgeler';
        }}
        
        function populateCategoryFilter() {{
            const categories = [...new Set(allDocuments.map(doc => categorizeDocument(doc)))].sort();
            const select = document.getElementById('categoryFilter');
            
            categories.forEach(category => {{
                const option = document.createElement('option');
                option.value = category;
                option.textContent = category;
                select.appendChild(option);
            }});
        }}
        
        function filterDocuments() {{
            const searchTerm = document.getElementById('searchBox').value.toLowerCase();
            const yearFilter = document.getElementById('yearFilter').value;
            const categoryFilter = document.getElementById('categoryFilter').value;
            
            let filtered = allDocuments;
            
            if (searchTerm) {{
                filtered = filtered.filter(doc => 
                    (doc.baslik && doc.baslik.toLowerCase().includes(searchTerm)) ||
                    (doc.yazar && doc.yazar.toLowerCase().includes(searchTerm)) ||
                    (doc.yayinevi && doc.yayinevi.toLowerCase().includes(searchTerm)) ||
                    (doc.yayinlayanKurum && doc.yayinlayanKurum.toLowerCase().includes(searchTerm))
                );
            }}
            
            if (yearFilter) {{
                const targetYear = parseInt(yearFilter);
                filtered = filtered.filter(doc => {{
                    const year = extractYear(doc.basimTarihi);
                    return year === targetYear;
                }});
            }}
            
            if (categoryFilter) {{
                filtered = filtered.filter(doc => categorizeDocument(doc) === categoryFilter);
            }}
            
            filteredDocuments = filtered;
            renderDocuments(filteredDocuments);
            updateStats();
        }}
        
        function updateStats() {{
            const totalCount = document.getElementById('totalCount');
            const filteredCount = document.getElementById('filteredCount');
            const dateRange = document.getElementById('dateRange');
            
            totalCount.textContent = `Toplam ${{allDocuments.length}} {doc_type}`;
            
            if (filteredDocuments.length !== allDocuments.length) {{
                filteredCount.textContent = `Görüntülenen: ${{filteredDocuments.length}}`;
            }} else {{
                filteredCount.textContent = '';
            }}
            
            const years = allDocuments.map(doc => extractYear(doc.basimTarihi)).filter(y => y);
            if (years.length > 0) {{
                const minYear = Math.min(...years);
                const maxYear = Math.max(...years);
                dateRange.textContent = `${{minYear}} - ${{maxYear}}`;
            }}
        }}
        
        function exportData() {{
            const headers = ['ID', 'Başlık'];
            if (allDocuments.some(doc => doc.yazar)) headers.push('Yazar');
            if (allDocuments.some(doc => doc.basimTarihi)) headers.push('Basım Tarihi');
            if (allDocuments.some(doc => doc.yayinevi)) headers.push('Yayınevi');
            if (allDocuments.some(doc => doc.basimYeri)) headers.push('Basım Yeri');
            if (allDocuments.some(doc => doc.yayinlayanKurum)) headers.push('Yayınlayan Kurum');
            if (allDocuments.some(doc => doc.enerjiIcerigi)) headers.push('Enerji İçeriği');
            if (allDocuments.some(doc => doc.erisimLinki || doc.link)) headers.push('Erişim Linki');
            
            const csvContent = [
                headers.join(','),
                ...filteredDocuments.map(doc => {{
                    const row = [doc.id || ''];
                    row.push(`"${{(doc.baslik || '').replace(/"/g, '""')}}"`);
                    if (headers.includes('Yazar')) row.push(`"${{(doc.yazar || '').replace(/"/g, '""')}}"`);
                    if (headers.includes('Basım Tarihi')) row.push(doc.basimTarihi || '');
                    if (headers.includes('Yayınevi')) row.push(`"${{(doc.yayinevi || '').replace(/"/g, '""')}}"`);
                    if (headers.includes('Basım Yeri')) row.push(`"${{(doc.basimYeri || '').replace(/"/g, '""')}}"`);
                    if (headers.includes('Yayınlayan Kurum')) row.push(`"${{(doc.yayinlayanKurum || '').replace(/"/g, '""')}}"`);
                    if (headers.includes('Enerji İçeriği')) {{
                        const content = Array.isArray(doc.enerjiIcerigi) ? doc.enerjiIcerigi.join('; ') : (doc.enerjiIcerigi || '');
                        row.push(`"${{content.replace(/"/g, '""')}}"`);
                    }}
                    if (headers.includes('Erişim Linki')) row.push(doc.erisimLinki || doc.link || '');
                    return row.join(',');
                }})
            ].join('\\n');
            
            const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = '{doc_type.replace(" ", "_")}.csv';
            link.click();
        }}
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {{
            if (typeof {data_var_name} !== 'undefined') {{
                allDocuments = {data_var_name};
                filteredDocuments = [...allDocuments];
                populateYearFilter();
                populateCategoryFilter();
                renderDocuments(filteredDocuments);
                updateStats();
                
                document.getElementById('searchBox').addEventListener('input', filterDocuments);
                document.getElementById('yearFilter').addEventListener('change', filterDocuments);
                document.getElementById('categoryFilter').addEventListener('change', filterDocuments);
                document.getElementById('exportBtn').addEventListener('click', exportData);
            }} else {{
                document.getElementById('loading').textContent = 'Veri yüklenirken hata oluştu.';
            }}
        }});
    </script>
</body>
</html>'''
    
    return html_template

def main():
    print("🚀 Generating all dashboard HTML files from Excel data...")
    
    # Discover Excel files dynamically
    dashboard_excel_files = discover_excel_files('new_data')
    qualitative_excel_files = discover_excel_files('nitel')
    
    print(f"📁 Found {len(dashboard_excel_files)} dashboard Excel files")
    print(f"📚 Found {len(qualitative_excel_files)} qualitative Excel files")
    
    # Dashboard files configuration - dynamically generated
    dashboard_configs = []
    
    # Map discovered files to configurations
    for file_info in dashboard_excel_files:
        file_num = file_info['number']
        filename = file_info['filename']
        
        if '1.' in filename and 'Birincil' in filename:
            config = {
                'excel_path': file_info['path'],
                'html_file': '1_birincil_enerjinin_kaynaklara_gore_uretimi_ve_tuketimi.html',
                'title': '1. Birincil Enerjinin Kaynaklara Göre Üretimi ve Tüketimi',
                'data_var': 'embeddedDataA',
                'y_axis': 'Değer (ktoe)',
                'chart_title': 'Birincil Enerji Üretimi ve Tüketimi'
            }
        elif '2.' in filename and 'Elektrik' in filename and 'Kurulu' in filename:
            config = {
                'excel_path': file_info['path'],
                'html_file': '2_elektrik_enerjisinin_kaynaklara_gore_kurulu_gucu_ve_uretimi.html',
                'title': '2. Elektrik Enerjisinin Kaynaklara Göre Kurulu Gücü ve Üretimi',
                'data_var': 'embeddedDataB',
                'y_axis': 'Değer (MW/GWh)',
                'chart_title': 'Elektrik Enerjisi Kurulu Güç ve Üretimi'
            }
        elif '3.' in filename and 'Elektrik' in filename and ('Br' in filename and 'Sekt' in filename):
            config = {
                'excel_path': file_info['path'],
                'html_file': '3_elektrik_enerjisinin_brut_uretimi_ve_sektorel_tuketimi.html',
                'title': '3. Elektrik Enerjisinin Brüt Üretimi ve Sektörel Tüketimi',
                'data_var': 'embeddedRawData',
                'y_axis': 'Değer (GWh)',
                'chart_title': 'Elektrik Enerjisi Sektörel Tüketimi'
            }
        else:
            continue  # Skip unrecognized files
            
        dashboard_configs.append(config)
        print(f"  📊 {file_num} -> {config['html_file']}")
    
    # Qualitative files configuration - dynamically generated
    qualitative_configs = []
    
    for file_info in qualitative_excel_files:
        file_num = file_info['number']
        filename = file_info['filename']
        
        if '1.' in filename and 'Yasal' in filename:
            config = {
                'excel_path': file_info['path'],
                'html_file': '4_yasal_duzenlemeler.html',
                'title': 'Yasal Düzenlemeler',
                'data_var': 'embeddedYasalData',
                'doc_type': 'yasal düzenlemeler'
            }
        elif '2.' in filename and 'Strateji' in filename:
            config = {
                'excel_path': file_info['path'],
                'html_file': '5_strateji_ve_politika_belgeleri.html',
                'title': 'Strateji ve Politika Belgeleri',
                'data_var': 'embeddedStratejiData',
                'doc_type': 'strateji ve politika belgeleri'
            }
        elif '3.' in filename and ('Kalk' in filename or 'Plan' in filename):
            config = {
                'excel_path': file_info['path'],
                'html_file': '6_kalkinma_planlari.html',
                'title': 'Kalkınma Planları',
                'data_var': 'embeddedKalkinmaData',
                'doc_type': 'kalkınma planları'
            }
        elif '4.' in filename and 'AB' in filename:
            config = {
                'excel_path': file_info['path'],
                'html_file': '7_ab_ilerleme_raporlari.html',
                'title': 'AB İlerleme Raporları',
                'data_var': 'embeddedAbData',
                'doc_type': 'AB ilerleme raporları'
            }
        else:
            continue  # Skip unrecognized files
            
        qualitative_configs.append(config)
        print(f"  📚 {file_num} -> {config['html_file']}")
    
    success_count = 0
    
    # Generate dashboard files
    for config in dashboard_configs:
        print(f"\n📊 Processing {config['title']}...")
        
        if not os.path.exists(config['excel_path']):
            print(f"❌ Excel file not found: {config['excel_path']}")
            continue
        
        data = read_excel_to_json(config['excel_path'])
        if not data:
            print(f"❌ Failed to read data from {config['excel_path']}")
            continue
        
        data_json = json.dumps(data, ensure_ascii=False, indent=2)
        
        html_content = generate_dashboard_html(
            title=config['title'],
            data_var_name=config['data_var'],
            data_json=data_json,
            y_axis_label=config['y_axis'],
            chart_title=config['chart_title']
        )
        
        try:
            with open(config['html_file'], 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✅ Generated {config['html_file']}")
            success_count += 1
        except Exception as e:
            print(f"❌ Failed to write {config['html_file']}: {e}")
    
    # Generate qualitative files
    for config in qualitative_configs:
        print(f"\n📚 Processing {config['title']}...")
        
        if not os.path.exists(config['excel_path']):
            print(f"❌ Excel file not found: {config['excel_path']}")
            continue
        
        data = read_excel_to_json(config['excel_path'], is_qualitative=True)
        if not data:
            print(f"❌ Failed to read data from {config['excel_path']}")
            continue
        
        data_json = json.dumps(data, ensure_ascii=False, indent=2)
        
        html_content = generate_qualitative_html(
            title=config['title'],
            data_var_name=config['data_var'],
            data_json=data_json,
            doc_type=config['doc_type']
        )
        
        try:
            with open(config['html_file'], 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✅ Generated {config['html_file']}")
            success_count += 1
        except Exception as e:
            print(f"❌ Failed to write {config['html_file']}: {e}")
    
    total_expected = len(dashboard_configs) + len(qualitative_configs)
    print(f"\n{'='*60}")
    if success_count == total_expected:
        print("🎉 SUCCESS: All HTML files generated successfully!")
        print("📁 Files are ready for immediate use")
        print("🚀 No safety procedures needed - direct generation from Excel")
    else:
        print(f"⚠️  PARTIAL SUCCESS: {success_count}/{total_expected} files generated")
    
    print("\n📋 Generated files:")
    for config in dashboard_configs + qualitative_configs:
        if os.path.exists(config['html_file']):
            size = os.path.getsize(config['html_file']) / 1024
            print(f"  - {config['html_file']} ({size:.1f}KB)")

if __name__ == "__main__":
    main() 