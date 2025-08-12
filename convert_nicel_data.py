#!/usr/bin/env python3
"""
Nicel (Quantitative) Data Conversion Script
Converts Excel files from nicel/ directory to HTML files with embedded JavaScript data and Chart.js visualizations.

Mappings:
- nicel/1. Birincil Enerjinin Kaynaklara Göre Üretimi ve Tüketimi.xlsx → 1_birincil_enerjinin_kaynaklara_gore_uretimi_ve_tuketimi.html (embeddedDataA)
- nicel/2. Elektrik Enerjisinin Kaynaklara Göre Kurulu Gücü ve Üretimi.xlsx → 2_elektrik_enerjisinin_kaynaklara_gore_kurulu_gucu_ve_uretimi.html (embeddedDataB)
- nicel/3. Elektrik Enerjisinin Brüt Üretimi ve Sektörel Tüketimi.xlsx → 3_elektrik_enerjisinin_brut_uretimi_ve_sektorel_tuketimi.html (embeddedRawData)
"""

import pandas as pd
import json
import re
import os
from pathlib import Path
import base64

# File mappings: (excel_file, html_file, js_variable_name, title)
FILE_MAPPINGS = [
    ("nicel/1. Birincil Enerjinin Kaynaklara Göre Üretimi ve Tüketimi.xlsx", "1_birincil_enerjinin_kaynaklara_gore_uretimi_ve_tuketimi.html", "embeddedDataA", "1. Birincil Enerjinin Kaynaklara Göre Üretimi ve Tüketimi"),
    ("nicel/2. Elektrik Enerjisinin Kaynaklara Göre Kurulu Gücü ve Üretimi.xlsx", "2_elektrik_enerjisinin_kaynaklara_gore_kurulu_gucu_ve_uretimi.html", "embeddedDataB", "2. Elektrik Enerjisinin Kaynaklara Göre Kurulu Gücü ve Üretimi"),
    ("nicel/3. Elektrik Enerjisinin Brüt Üretimi ve Sektörel Tüketimi.xlsx", "3_elektrik_enerjisinin_brut_uretimi_ve_sektorel_tuketimi.html", "embeddedRawData", "3. Elektrik Enerjisinin Brüt Üretimi ve Sektörel Tüketimi")
]

def clean_numeric_value(value):
    """Clean and convert numeric values"""
    if pd.isna(value) or value is None:
        return 0
    
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0

def excel_to_js_object(df):
    """Convert DataFrame to JavaScript array of objects"""
    
    objects = []
    
    for index, row in df.iterrows():
        obj = {"Kategori": str(row.get("Kategori", f"Category_{index}"))}
        
        # Add all year columns
        for col in df.columns:
            if col != "Kategori" and col.isdigit():
                obj[col] = clean_numeric_value(row.get(col, 0))
        
        objects.append(obj)
    
    return objects

def get_logo_base64():
    """Get base64 encoded logo"""
    try:
        with open("logo.jpg", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

def create_dashboard_html(title, js_variable, js_content):
    """Create complete dashboard HTML file with Chart.js visualizations"""
    
    logo_base64 = get_logo_base64()
    
    return f"""<!DOCTYPE html>
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
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        }}
        
        .content {{
            padding: 2rem;
        }}
        
        .controls {{
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
            align-items: center;
        }}
        
        .control-group {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            min-width: 200px;
        }}
        
        .control-label {{
            font-weight: 600;
            color: #006400;
            font-size: 0.9rem;
        }}
        
        .control-select {{
            padding: 10px 12px;
            border: 2px solid #ddd;
            border-radius: 6px;
            font-size: 14px;
            background: white;
            transition: border-color 0.3s;
        }}
        
        .control-select:focus {{
            outline: none;
            border-color: #006400;
        }}
        
        .year-range {{
            width: 300px;
            margin: 1rem 0;
        }}
        
        .year-labels {{
            display: flex;
            justify-content: space-between;
            margin-top: 0.5rem;
            font-size: 0.9rem;
            color: #666;
        }}
        
        .chart-section {{
            margin: 2rem 0;
            padding: 1.5rem;
            background: #f9f9f9;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        }}
        
        .chart-title {{
            font-size: 1.3rem;
            font-weight: 600;
            color: #006400;
            margin-bottom: 1rem;
            text-align: center;
        }}
        
        .chart-container {{
            position: relative;
            height: 500px;
            margin: 1rem 0;
        }}
        
        .chart-export {{
            text-align: center;
            margin-top: 1rem;
        }}
        
        .export-btn {{
            background: #006400;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            transition: background-color 0.3s;
        }}
        
        .export-btn:hover {{
            background: #228B22;
        }}
        
        .legend-container {{
            max-height: 200px;
            overflow-y: auto;
            margin-top: 1rem;
            padding: 1rem;
            background: white;
            border-radius: 6px;
            border: 1px solid #ddd;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin: 0.5rem 0;
            cursor: pointer;
            padding: 0.3rem;
            border-radius: 4px;
            transition: background-color 0.2s;
        }}
        
        .legend-item:hover {{
            background: #f5f5f5;
        }}
        
        .legend-color {{
            width: 20px;
            height: 3px;
            border-radius: 2px;
        }}
        
        .legend-label {{
            font-size: 0.9rem;
            flex: 1;
        }}
        
        .data-table {{
            margin-top: 2rem;
            overflow-x: auto;
        }}
        
        .data-table table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }}
        
        .data-table th,
        .data-table td {{
            padding: 8px 12px;
            text-align: left;
            border: 1px solid #ddd;
        }}
        
        .data-table th {{
            background: #006400;
            color: white;
            font-weight: 600;
        }}
        
        .data-table tr:nth-child(even) {{
            background: #f9f9f9;
        }}
        
        .data-table tr:hover {{
            background: #f0f8f0;
        }}
        
        @media (max-width: 768px) {{
            .controls {{
                flex-direction: column;
            }}
            
            .control-group {{
                min-width: 100%;
            }}
            
            .chart-container {{
                height: 400px;
            }}
        }}
    </style>
</head>
<body>
    <div class="main-container">
        <div class="header">
            <h1>{title}</h1>
            <p>Türkiye Enerji Verileri - İnteraktif Dashboard</p>
        </div>
        
        <div class="content">
            <div class="controls">
                <div class="control-group">
                    <label class="control-label">Grafik Türü</label>
                    <select id="chartType" class="control-select">
                        <option value="line">Çizgi Grafik</option>
                        <option value="bar">Sütun Grafik</option>
                        <option value="pie">Pasta Grafik</option>
                    </select>
                </div>
                
                <div class="control-group">
                    <label class="control-label">Veri Seçimi</label>
                    <select id="dataFilter" class="control-select">
                        <option value="all">Tüm Kategoriler</option>
                    </select>
                </div>
                
                <div class="control-group">
                    <label class="control-label">Yıl Aralığı</label>
                    <div class="year-range" id="yearRange"></div>
                    <div class="year-labels">
                        <span id="startYear">1923</span>
                        <span id="endYear">2023</span>
                    </div>
                </div>
            </div>
            
            <div class="chart-section">
                <div class="chart-title" id="chartTitle">Enerji Verileri</div>
                <div class="chart-container">
                    <canvas id="mainChart"></canvas>
                </div>
                <div class="legend-container" id="legendContainer"></div>
                <div class="chart-export">
                    <button class="export-btn" onclick="exportChart()">Grafiği İndir (PNG)</button>
                </div>
            </div>
            
            <div class="data-table" id="dataTable"></div>
        </div>
    </div>

    <!-- Embedded data -->
    <script>
{js_content}
    </script>

    <script>
        let chart = null;
        let allData = [];
        let currentData = [];
        let yearRange = [1923, 2023];
        
        // Chart colors
        const colors = [
            '#006400', '#228B22', '#32CD32', '#7CFC00', '#ADFF2F', '#9AFF9A',
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD',
            '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9', '#F8C471', '#82E0AA',
            '#F1948A', '#85C1E9', '#D7BDE2', '#A9DFBF', '#F9E79F', '#D5A6BD'
        ];

        document.addEventListener('DOMContentLoaded', function() {{
            // Use {js_variable} from the included script file
            const data = typeof {js_variable} !== 'undefined' ? {js_variable} : [];
            
            if (data.length === 0) {{
                console.error('No data found');
                return;
            }}
            
            allData = data;
            setupControls();
            updateChart();
        }});

        function setupControls() {{
            // Populate data filter
            const categories = [...new Set(allData.map(item => item.Kategori))];
            const dataFilter = document.getElementById('dataFilter');
            
            categories.forEach(category => {{
                const option = document.createElement('option');
                option.value = category;
                option.textContent = category.length > 30 ? category.substring(0, 30) + '...' : category;
                dataFilter.appendChild(option);
            }});
            
            // Setup year range slider
            const years = [];
            allData.forEach(item => {{
                Object.keys(item).forEach(key => {{
                    if (key !== 'Kategori' && key.match(/^\\d{{4}}$/)) {{
                        years.push(parseInt(key));
                    }}
                }});
            }});
            
            if (years.length > 0) {{
                const minYear = Math.min(...years);
                const maxYear = Math.max(...years);
                yearRange = [minYear, maxYear];
                
                document.getElementById('startYear').textContent = minYear;
                document.getElementById('endYear').textContent = maxYear;
                
                const slider = document.getElementById('yearRange');
                noUiSlider.create(slider, {{
                    start: [minYear, maxYear],
                    connect: true,
                    range: {{
                        'min': minYear,
                        'max': maxYear
                    }},
                    step: 1,
                    tooltips: [true, true],
                    format: {{
                        to: value => Math.round(value),
                        from: value => Number(value)
                    }}
                }});
                
                slider.noUiSlider.on('update', function(values) {{
                    yearRange = [parseInt(values[0]), parseInt(values[1])];
                    document.getElementById('startYear').textContent = values[0];
                    document.getElementById('endYear').textContent = values[1];
                    updateChart();
                }});
            }}
            
            // Setup event listeners
            document.getElementById('chartType').addEventListener('change', updateChart);
            document.getElementById('dataFilter').addEventListener('change', updateChart);
        }}

        function updateChart() {{
            const chartType = document.getElementById('chartType').value;
            const dataFilter = document.getElementById('dataFilter').value;
            
            // Filter data
            currentData = allData.filter(item => {{
                return dataFilter === 'all' || item.Kategori === dataFilter;
            }});
            
            // Update chart
            createChart(chartType);
            updateDataTable();
        }}

        function createChart(type) {{
            const ctx = document.getElementById('mainChart').getContext('2d');
            
            if (chart) {{
                chart.destroy();
            }}
            
            const chartData = prepareChartData(type);
            
            const config = {{
                type: type,
                data: chartData,
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        title: {{
                            display: true,
                            text: document.getElementById('chartTitle').textContent,
                            font: {{
                                size: 16,
                                weight: 'bold'
                            }}
                        }},
                        legend: {{
                            display: type !== 'line',
                            position: 'bottom',
                            labels: {{
                                usePointStyle: true,
                                padding: 15,
                                font: {{
                                    size: 11
                                }},
                                generateLabels: function(chart) {{
                                    const labels = Chart.defaults.plugins.legend.labels.generateLabels(chart);
                                    return labels.map(label => {{
                                        if (label.text.length > 25) {{
                                            label.text = label.text.substring(0, 25) + '...';
                                        }}
                                        return label;
                                    }});
                                }}
                            }}
                        }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    let label = context.dataset.label || '';
                                    if (label) {{
                                        label += ': ';
                                    }}
                                    label += context.parsed.y?.toLocaleString('tr-TR') || context.parsed;
                                    return label;
                                }}
                            }}
                        }}
                    }},
                    scales: type !== 'pie' ? {{
                        x: {{
                            display: true,
                            title: {{
                                display: true,
                                text: 'Yıl'
                            }}
                        }},
                        y: {{
                            display: true,
                            title: {{
                                display: true,
                                text: 'Değer'
                            }},
                            ticks: {{
                                callback: function(value) {{
                                    return value.toLocaleString('tr-TR');
                                }}
                            }}
                        }}
                    }} : {{}}
                }}
            }};
            
            chart = new Chart(ctx, config);
            
            if (type === 'line') {{
                createCustomLegend();
            }}
        }}

        function prepareChartData(type) {{
            const years = [];
            for (let year = yearRange[0]; year <= yearRange[1]; year++) {{
                if (allData.some(item => item.hasOwnProperty(year.toString()))) {{
                    years.push(year.toString());
                }}
            }}
            
            if (type === 'pie') {{
                // For pie chart, use the latest year
                const latestYear = years[years.length - 1];
                return {{
                    labels: currentData.map(item => {{
                        return item.Kategori.length > 25 ? item.Kategori.substring(0, 25) + '...' : item.Kategori;
                    }}),
                    datasets: [{{
                        data: currentData.map(item => item[latestYear] || 0),
                        backgroundColor: colors.slice(0, currentData.length),
                        borderWidth: 2,
                        borderColor: '#fff'
                    }}]
                }};
            }} else {{
                // For line and bar charts
                return {{
                    labels: years,
                    datasets: currentData.map((item, index) => ({{
                        label: item.Kategori,
                        data: years.map(year => item[year] || 0),
                        borderColor: colors[index % colors.length],
                        backgroundColor: colors[index % colors.length] + (type === 'bar' ? '80' : '20'),
                        borderWidth: 2,
                        fill: false,
                        tension: 0.1
                    }}))
                }};
            }}
        }}

        function createCustomLegend() {{
            const legendContainer = document.getElementById('legendContainer');
            legendContainer.innerHTML = '';
            
            if (chart.data.datasets.length <= 1) {{
                legendContainer.style.display = 'none';
                return;
            }}
            
            legendContainer.style.display = 'block';
            
            chart.data.datasets.forEach((dataset, index) => {{
                const legendItem = document.createElement('div');
                legendItem.className = 'legend-item';
                legendItem.onclick = () => toggleDataset(index);
                
                const colorBox = document.createElement('div');
                colorBox.className = 'legend-color';
                colorBox.style.backgroundColor = dataset.borderColor;
                
                const label = document.createElement('span');
                label.className = 'legend-label';
                label.textContent = dataset.label.length > 50 ? dataset.label.substring(0, 50) + '...' : dataset.label;
                
                legendItem.appendChild(colorBox);
                legendItem.appendChild(label);
                legendContainer.appendChild(legendItem);
            }});
        }}

        function toggleDataset(index) {{
            const meta = chart.getDatasetMeta(index);
            meta.hidden = meta.hidden === null ? !chart.data.datasets[index].hidden : null;
            chart.update();
        }}

        function updateDataTable() {{
            const tableContainer = document.getElementById('dataTable');
            
            if (currentData.length === 0) {{
                tableContainer.innerHTML = '';
                return;
            }}
            
            const years = [];
            for (let year = yearRange[0]; year <= yearRange[1]; year++) {{
                if (currentData.some(item => item.hasOwnProperty(year.toString()))) {{
                    years.push(year.toString());
                }}
            }}
            
            let html = '<h3>Veri Tablosu</h3><table><thead><tr><th>Kategori</th>';
            years.forEach(year => {{
                html += `<th>${{year}}</th>`;
            }});
            html += '</tr></thead><tbody>';
            
            currentData.forEach(item => {{
                html += `<tr><td>${{item.Kategori}}</td>`;
                years.forEach(year => {{
                    const value = item[year] || 0;
                    html += `<td>${{value.toLocaleString('tr-TR')}}</td>`;
                }});
                html += '</tr>';
            }});
            
            html += '</tbody></table>';
            tableContainer.innerHTML = html;
        }}

        function exportChart() {{
            if (!chart) return;
            
            // Create a temporary canvas with higher resolution
            const originalCanvas = chart.canvas;
            const tempCanvas = document.createElement('canvas');
            const tempCtx = tempCanvas.getContext('2d');
            
            // Set high resolution
            const scaleFactor = 3;
            tempCanvas.width = 1800 * scaleFactor;
            tempCanvas.height = 1200 * scaleFactor;
            tempCtx.scale(scaleFactor, scaleFactor);
            
            // White background
            tempCtx.fillStyle = 'white';
            tempCtx.fillRect(0, 0, 1800, 1200);
            
            // Add logo if available
            {f'''const logoImg = new Image();
            logoImg.onload = function() {{
                // Draw logo with shadow
                tempCtx.shadowColor = 'rgba(0,0,0,0.3)';
                tempCtx.shadowBlur = 10;
                tempCtx.shadowOffsetX = 3;
                tempCtx.shadowOffsetY = 3;
                tempCtx.drawImage(logoImg, 50, 50, 150, 75);
                tempCtx.shadowColor = 'transparent';
                
                // Draw title
                tempCtx.font = 'bold 32px Segoe UI';
                tempCtx.fillStyle = '#006400';
                tempCtx.textAlign = 'center';
                tempCtx.fillText('{title}', 900, 100);
                
                // Draw chart
                tempCtx.drawImage(originalCanvas, 100, 150, 1600, 900);
                
                // Download
                const link = document.createElement('a');
                link.download = '{title.replace(" ", "_")}_chart.png';
                link.href = tempCanvas.toDataURL('image/png');
                link.click();
            }};
            logoImg.src = 'data:image/jpeg;base64,{logo_base64}';''' if logo_base64 else '''
            // Draw title
            tempCtx.font = 'bold 32px Segoe UI';
            tempCtx.fillStyle = '#006400';
            tempCtx.textAlign = 'center';
            tempCtx.fillText('{title}', 900, 100);
            
            // Draw chart
            tempCtx.drawImage(originalCanvas, 100, 150, 1600, 900);
            
            // Download
            const link = document.createElement('a');
            link.download = '{title.replace(" ", "_")}_chart.png';
            link.href = tempCanvas.toDataURL('image/png');
            link.click();'''}
        }}
    </script>
</body>
</html>"""

def convert_excel_to_html(excel_path, html_path, js_variable, title):
    """Convert single Excel file to dashboard HTML"""
    
    print(f"Converting {excel_path} to {html_path}...")
    
    # Read Excel file
    try:
        df = pd.read_excel(excel_path)
        print(f"  Loaded {len(df)} rows from Excel")
        print(f"  Columns: {list(df.columns)}")
    except Exception as e:
        print(f"  Error reading Excel file: {e}")
        return False
    
    # Convert to JavaScript objects
    js_objects = excel_to_js_object(df)
    js_content = f"const {js_variable} = {json.dumps(js_objects, ensure_ascii=False, indent=2)};"
    
    # Create HTML content
    html_content = create_dashboard_html(title, js_variable, js_content)
    
    # Write HTML file
    try:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"  Successfully created {html_path}")
        return True
    except Exception as e:
        print(f"  Error writing HTML file: {e}")
        return False

def main():
    """Convert all nicel Excel files to HTML dashboards"""
    
    print("Starting nicel data conversion...")
    print("=" * 50)
    
    success_count = 0
    
    for excel_file, html_file, js_variable, title in FILE_MAPPINGS:
        if os.path.exists(excel_file):
            if convert_excel_to_html(excel_file, html_file, js_variable, title):
                success_count += 1
        else:
            print(f"Excel file not found: {excel_file}")
        print()
    
    print("=" * 50)
    print(f"Conversion completed: {success_count}/{len(FILE_MAPPINGS)} files successful")

if __name__ == "__main__":
    main() 