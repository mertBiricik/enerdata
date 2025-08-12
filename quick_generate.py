#!/usr/bin/env python3
"""
Quick generation script using actual file names
"""

import pandas as pd
import json
import os
import glob

def read_excel_to_json(excel_path):
    """Read Excel file and convert to JSON format"""
    try:
        df = pd.read_excel(excel_path)
        df = df.where(pd.notnull(df), None)
        return df.to_dict('records')
    except Exception as e:
        print(f"Error reading {excel_path}: {e}")
        return []

def generate_dashboard_html(title, data_var_name, data_json, y_axis_label="Değer", chart_title="Enerji Verileri"):
    """Generate complete dashboard HTML"""
    
    return f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/nouislider@15.7.1/dist/nouislider.min.css">
    <script src="https://cdn.jsdelivr.net/npm/nouislider@15.7.1/dist/nouislider.min.js"></script>
    <style>
        * {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important; box-sizing: border-box; }}
        body {{ margin: 0; padding: 20px; background: white; color: #333; line-height: 1.6; }}
        .main-container {{ max-width: 1600px; width: 95%; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #006400 0%, #228B22 100%); color: white; padding: 2rem; text-align: center; position: relative; }}
        .header h1 {{ margin: 0; font-size: 2.2rem; font-weight: 600; color: white !important; }}
        .logo {{ position: absolute; top: 20px; right: 20px; width: 80px; height: 80px; background: url('data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCABQAFADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAWX/aAAwDAQACEQMRAD8A+f6KKK0AKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA//9k=') center/contain no-repeat; border-radius: 8px; background-color: rgba(255,255,255,0.1); }}
        .content-layout {{ display: flex; min-height: 600px; }}
        .filters-panel {{ width: 300px; background: #f8f9fa; padding: 2rem; border-right: 1px solid #e9ecef; }}
        .content-panel {{ flex: 1; padding: 2rem; }}
        .tabs {{ display: flex; border-bottom: 2px solid #e9ecef; margin-bottom: 2rem; }}
        .tab-button {{ padding: 1rem 2rem; background: none; border: none; border-bottom: 3px solid transparent; cursor: pointer; font-weight: 600; color: #495057; transition: all 0.3s ease; }}
        .tab-button.active {{ color: #006400; border-bottom-color: #006400; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        .chart-container {{ position: relative; height: 500px; margin-bottom: 2rem; }}
        .table-container {{ overflow-x: auto; border: 1px solid #ddd; border-radius: 8px; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
        th, td {{ padding: 0.75rem; text-align: right; border-bottom: 1px solid #e9ecef; }}
        th:first-child, td:first-child {{ text-align: left; position: sticky; left: 0; background: white; font-weight: 600; }}
        th {{ background: #f8f9fa; font-weight: 600; position: sticky; top: 0; }}
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
                <h3>Veri Kontrolleri</h3>
                <p>Gelişmiş filtreleme özellikleri...</p>
            </div>
            
            <div class="content-panel">
                <div class="tabs">
                    <button class="tab-button active" data-tab="table">Tablo</button>
                    <button class="tab-button" data-tab="line">Çizgi Grafik</button>
                    <button class="tab-button" data-tab="bar">Sütun Grafik</button>
                </div>
                
                <div id="tableContent" class="tab-content active">
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
                </div>
                
                <div id="barContent" class="tab-content">
                    <div class="chart-container">
                        <canvas id="barChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
const {data_var_name} = {data_json};
    </script>

    <script>
        let currentData = {data_var_name};
        let lineChart, barChart;
        
        function createTable() {{
            const table = document.getElementById('dataTable');
            const thead = table.querySelector('thead');
            const tbody = table.querySelector('tbody');
            
            if (!currentData || currentData.length === 0) {{
                table.innerHTML = '<thead><tr><th>Veri Yok</th></tr></thead>';
                return;
            }}
            
            // Get all year columns
            const yearColumns = [];
            Object.keys(currentData[0]).forEach(key => {{
                if (key !== 'Kategori' && !isNaN(parseInt(key))) {{
                    yearColumns.push(parseInt(key));
                }}
            }});
            yearColumns.sort((a, b) => a - b);
            
            // Create header
            thead.innerHTML = '<tr><th>Kategori</th>' + 
                yearColumns.map(year => `<th>${{year}}</th>`).join('') + '</tr>';
            
            // Create rows
            tbody.innerHTML = currentData.map(item => {{
                const values = yearColumns.map(year => {{
                    const value = item[year.toString()];
                    return value !== null && value !== undefined ? 
                        (typeof value === 'number' ? value.toLocaleString('tr-TR') : value) : '-';
                }});
                
                return '<tr><td>' + item.Kategori + '</td><td>' + values.join('</td><td>') + '</td></tr>';
            }}).join('');
        }}
        
        function createLineChart() {{
            const ctx = document.getElementById('lineChart').getContext('2d');
            
            if (lineChart) lineChart.destroy();
            
            const yearColumns = [];
            Object.keys(currentData[0]).forEach(key => {{
                if (key !== 'Kategori' && !isNaN(parseInt(key))) {{
                    yearColumns.push(parseInt(key));
                }}
            }});
            yearColumns.sort((a, b) => a - b);
            
            const datasets = currentData.slice(0, 10).map((item, index) => {{
                const data = yearColumns.map(year => {{
                    const value = item[year.toString()];
                    return value !== null && value !== undefined ? value : null;
                }});
                
                return {{
                    label: item.Kategori,
                    data: data,
                    borderColor: `hsl(${{index * 36}}, 70%, 50%)`,
                    backgroundColor: `hsla(${{index * 36}}, 70%, 50%, 0.1)`,
                    fill: false,
                    tension: 0.1
                }};
            }});
            
            lineChart = new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: yearColumns,
                    datasets: datasets
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
                        legend: {{ display: true, position: 'top' }},
                        title: {{ display: true, text: '{chart_title}' }}
                    }}
                }}
            }});
        }}
        
        function createBarChart() {{
            const ctx = document.getElementById('barChart').getContext('2d');
            
            if (barChart) barChart.destroy();
            
            const yearColumns = [];
            Object.keys(currentData[0]).forEach(key => {{
                if (key !== 'Kategori' && !isNaN(parseInt(key))) {{
                    yearColumns.push(parseInt(key));
                }}
            }});
            
            const latestYear = Math.max(...yearColumns);
            
            const chartData = currentData.slice(0, 15).map(item => {{
                const value = item[latestYear.toString()];
                return {{
                    label: item.Kategori,
                    value: value !== null && value !== undefined ? value : 0
                }};
            }}).filter(item => Math.abs(item.value) > 0);
            
            barChart = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: chartData.map(item => item.label),
                    datasets: [{{
                        label: `${{latestYear}} Değerleri`,
                        data: chartData.map(item => item.value),
                        backgroundColor: chartData.map((_, index) => 
                            `hsla(${{index * 24}}, 70%, 50%, 0.7)`
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
                        title: {{ display: true, text: `{chart_title} (${{latestYear}})` }}
                    }}
                }}
            }});
        }}
        
        function initializeTabs() {{
            const tabButtons = document.querySelectorAll('.tab-button');
            const tabContents = document.querySelectorAll('.tab-content');
            
            tabButtons.forEach(button => {{
                button.addEventListener('click', function() {{
                    tabButtons.forEach(b => b.classList.remove('active'));
                    tabContents.forEach(c => c.classList.remove('active'));
                    
                    this.classList.add('active');
                    const targetTab = this.getAttribute('data-tab');
                    document.getElementById(targetTab + 'Content').classList.add('active');
                    
                    setTimeout(() => {{
                        if (targetTab === 'line') createLineChart();
                        else if (targetTab === 'bar') createBarChart();
                    }}, 100);
                }});
            }});
        }}
        
        document.addEventListener('DOMContentLoaded', function() {{
            try {{
                if (!currentData || currentData.length === 0) {{
                    throw new Error('Veri yok');
                }}
                
                initializeTabs();
                createTable();
                
            }} catch (error) {{
                console.error('Initialization error:', error);
                document.body.innerHTML = '<div style="text-align: center; padding: 50px; font-size: 18px;">Veri yüklenemedi: ' + error.message + '</div>';
            }}
        }});
    </script>
</body>
</html>'''

def main():
    print("🚀 Quick generation from Excel files...")
    
    # Find Excel files in new_data
    excel_files = glob.glob('new_data/*.xlsx')
    print(f"Found {len(excel_files)} Excel files:")
    for f in excel_files:
        print(f"  - {f}")
    
    configs = []
    
    for excel_file in excel_files:
        basename = os.path.basename(excel_file)
        if 'Birincil' in basename:
            configs.append({
                'excel_path': excel_file,
                'html_file': '1_birincil_enerjinin_kaynaklara_gore_uretimi_ve_tuketimi.html',
                'title': '1. Birincil Enerjinin Kaynaklara Göre Üretimi ve Tüketimi',
                'data_var': 'embeddedDataA',
                'y_axis': 'Değer (ktoe)',
                'chart_title': 'Birincil Enerji Üretimi ve Tüketimi'
            })
        elif 'Kurulu' in basename:
            configs.append({
                'excel_path': excel_file,
                'html_file': '2_elektrik_enerjisinin_kaynaklara_gore_kurulu_gucu_ve_uretimi.html',
                'title': '2. Elektrik Enerjisinin Kaynaklara Göre Kurulu Gücü ve Üretimi',
                'data_var': 'embeddedDataB',
                'y_axis': 'Değer (MW/GWh)',
                'chart_title': 'Elektrik Enerjisi Kurulu Güç ve Üretimi'
            })
        elif 'Brüt' in basename or 'Sektörel' in basename:
            configs.append({
                'excel_path': excel_file,
                'html_file': '3_elektrik_enerjisinin_brut_uretimi_ve_sektorel_tuketimi.html',
                'title': '3. Elektrik Enerjisinin Brüt Üretimi ve Sektörel Tüketimi',
                'data_var': 'embeddedRawData',
                'y_axis': 'Değer (GWh)',
                'chart_title': 'Elektrik Enerjisi Sektörel Tüketimi'
            })
    
    success_count = 0
    
    for config in configs:
        print(f"\\n📊 Processing {config['title']}...")
        
        data = read_excel_to_json(config['excel_path'])
        if not data:
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
    
    print(f"\\n🎉 SUCCESS: Generated {success_count} dashboard files!")
    
    for config in configs:
        if os.path.exists(config['html_file']):
            size = os.path.getsize(config['html_file']) / 1024
            print(f"  - {config['html_file']} ({size:.1f}KB)")

if __name__ == "__main__":
    main() 