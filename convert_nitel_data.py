#!/usr/bin/env python3
"""
Nitel (Qualitative) Data Conversion Script
Converts Excel files from nitel/ directory to HTML files with embedded JavaScript data.

Mappings:
- nitel/1. Yasal Düzenlemeler.xlsx → 4_yasal_duzenlemeler.html (embeddedYasalData)
- nitel/2. Strateji ve Politika Belgeleri.xlsx → 5_strateji_ve_politika_belgeleri.html (embeddedStratejiData)
- nitel/3. Kalkınma Planları.xlsx → 6_kalkinma_planlari.html (embeddedKalkinmaData)
- nitel/4. AB İlerleme Raporları.xlsx → 7_ab_ilerleme_raporlari.html (embeddedAbData)
"""

import pandas as pd
import json
import re
import os
from pathlib import Path

# File mappings: (excel_file, html_file, js_variable_name, title)
FILE_MAPPINGS = [
    ("nitel/1. Yasal Düzenlemeler.xlsx", "4_yasal_duzenlemeler.html", "embeddedYasalData", "Yasal Düzenlemeler"),
    ("nitel/2. Strateji ve Politika Belgeleri.xlsx", "5_strateji_ve_politika_belgeleri.html", "embeddedStratejiData", "Strateji ve Politika Belgeleri"),
    ("nitel/3. Kalkınma Planları.xlsx", "6_kalkinma_planlari.html", "embeddedKalkinmaData", "Kalkınma Planları"),
    ("nitel/4. AB İlerleme Raporları.xlsx", "7_ab_ilerleme_raporlari.html", "embeddedAbData", "AB İlerleme Raporları")
]

def clean_text_for_js(text):
    """Clean text for JavaScript string literal"""
    if pd.isna(text) or text is None:
        return ""
    
    text = str(text)
    # Remove problematic characters and ensure single line
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = text.replace('"', '\\"')  # Escape quotes
    text = text.replace('\\', '\\\\')  # Escape backslashes
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    return text.strip()

def excel_to_js_object(df, var_name):
    """Convert DataFrame to JavaScript array of objects"""
    
    objects = []
    
    for index, row in df.iterrows():
        obj = {}
        
        # Process each column based on variable name
        if var_name == "embeddedYasalData":
            # Yasal Düzenlemeler structure
            obj = {
                "id": str(index + 1),
                "kanunNo": clean_text_for_js(row.get("Kanun No", "")),
                "kabulTarihi": clean_text_for_js(row.get("Kabul Tarihi", "")),
                "baslik": clean_text_for_js(row.get("Başlık", "")),
                "rgTarih": clean_text_for_js(row.get("RG Tarih", "")),
                "rgSayi": clean_text_for_js(row.get("RG Sayı", "")),
                "amac": clean_text_for_js(row.get("Amaç", "")),
                "category": "Yasal Düzenlemeler",
                "erisimLinki": clean_text_for_js(row.get("Erişim Linki", ""))
            }
            
        elif var_name == "embeddedStratejiData":
            # Strateji ve Politika structure - using actual Excel column names
            obj = {
                "id": str(index + 1),
                "yazar": clean_text_for_js(row.get("Yazar", "")),
                "baslik": clean_text_for_js(row.get("Başlık", "")),
                "basimTarihi": clean_text_for_js(row.get("Basım Tarihi", "")),
                "yayinevi": clean_text_for_js(row.get("Yayınevi/Basımevi", "")),
                "basimYeri": clean_text_for_js(row.get("Basım Yeri", "")),
                "erisimLinki": clean_text_for_js(row.get("Erişim Linki", "")),
                "category": "Strateji ve Politika Belgeleri"
            }
            
        elif var_name == "embeddedKalkinmaData":
            # Kalkınma Planları structure
            enerji_icerigi = []
            # Look for multiple content columns
            for col in df.columns:
                if "enerji" in col.lower() or "içerik" in col.lower():
                    content = clean_text_for_js(row.get(col, ""))
                    if content:
                        enerji_icerigi.append(content)
            
            obj = {
                "id": str(index + 1),
                "yayinlayanKurum": clean_text_for_js(row.get("Yayınlayan Kurum", "")),
                "baslik": clean_text_for_js(row.get("Başlık", "")),
                "enerjiIcerigi": enerji_icerigi,
                "link": clean_text_for_js(row.get("Link", "")),
                "category": "Kalkınma Planları"
            }
            
        elif var_name == "embeddedAbData":
            # AB İlerleme Raporları structure
            obj = {
                "id": str(index + 1),
                "hazirlayan": clean_text_for_js(row.get("Hazırlayan", "")),
                "tarih": clean_text_for_js(row.get("Tarih", "")),
                "raporNo": clean_text_for_js(row.get("Rapor No", "")) or None,
                "raporBaslik": clean_text_for_js(row.get("Rapor Başlık", "")),
                "enerjiIcerigi": clean_text_for_js(row.get("Enerji İçeriği", "")),
                "cevreIcerigi": clean_text_for_js(row.get("Çevre İçeriği", "")),
                "category": "AB İlerleme Raporları",
                "erisimLinki": clean_text_for_js(row.get("Erişim Linki", ""))
            }
        
        objects.append(obj)
    
    # Convert to JavaScript
    js_content = f"const {var_name} = {json.dumps(objects, ensure_ascii=False, indent=2)};"
    return js_content

def create_html_template(title, js_variable, js_content):
    """Create complete HTML file with embedded data"""
    
    return f"""<!DOCTYPE html>
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
        
        .search-container {{
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
            align-items: center;
        }}
        
        .search-box {{
            flex: 1;
            min-width: 300px;
            padding: 12px 16px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }}
        
        .search-box:focus {{
            outline: none;
            border-color: #006400;
        }}
        
        .filter-select {{
            padding: 12px 16px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            background: white;
            min-width: 200px;
        }}
        
        .documents-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
        }}
        
        .document-card {{
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
            cursor: pointer;
        }}
        
        .document-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        }}
        
        .document-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #006400;
            margin-bottom: 0.5rem;
            line-height: 1.4;
        }}
        
        .document-meta {{
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }}
        
        .document-content {{
            color: #333;
            font-size: 0.95rem;
            line-height: 1.5;
            margin-bottom: 1rem;
        }}
        
        .document-link {{
            display: inline-block;
            background: #006400;
            color: white !important;
            padding: 8px 16px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 0.9rem;
            transition: background-color 0.3s;
        }}
        
        .document-link:hover {{
            background: #228B22;
        }}
        
        .results-info {{
            margin: 1rem 0;
            font-size: 1rem;
            color: #666;
        }}
        
        .no-results {{
            text-align: center;
            padding: 3rem;
            color: #666;
            font-size: 1.1rem;
        }}
        
        .loading {{
            text-align: center;
            padding: 3rem;
            font-size: 1.1rem;
            color: #006400;
        }}
        
        @media (max-width: 768px) {{
            .search-container {{
                flex-direction: column;
            }}
            
            .search-box, .filter-select {{
                min-width: 100%;
            }}
            
            .documents-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="main-container">
        <div class="header">
            <h1>{title}</h1>
            <p>Enerji alanında yayınlanan belgeler ve dokümantasyon</p>
        </div>
        
        <div class="content">
            <div class="search-container">
                <input type="text" id="searchInput" class="search-box" placeholder="Başlık, yazar veya içerik ara...">
                <select id="categoryFilter" class="filter-select">
                    <option value="">Tüm Kategoriler</option>
                </select>
            </div>
            
            <div class="results-info" id="resultsInfo"></div>
            
            <div id="loading" class="loading">Veriler yükleniyor...</div>
            <div id="documentsContainer" class="documents-grid" style="display: none;"></div>
            <div id="noResults" class="no-results" style="display: none;">
                Arama kriterlerinize uygun belge bulunamadı.
            </div>
        </div>
    </div>

    <script>
        let allDocuments = [];
        let filteredDocuments = [];

        document.addEventListener('DOMContentLoaded', function() {{
            try {{
                if (typeof {js_variable} !== 'undefined') {{
                    allDocuments = {js_variable};
                    filteredDocuments = [...allDocuments];
                    setupEventListeners();
                    populateFilters();
                    displayDocuments();
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('documentsContainer').style.display = 'grid';
                }} else {{
                    document.getElementById('loading').textContent = 'Veri yüklenirken hata oluştu.';
                }}
            }} catch (error) {{
                console.error('Error during initialization:', error);
                document.getElementById('loading').textContent = 'Veri yüklenirken hata oluştu.';
            }}
        }});

        function setupEventListeners() {{
            document.getElementById('searchInput').addEventListener('input', filterDocuments);
            document.getElementById('categoryFilter').addEventListener('change', filterDocuments);
        }}

        function populateFilters() {{
            const categories = [...new Set(allDocuments.map(doc => doc.category))];
            const categorySelect = document.getElementById('categoryFilter');
            
            categories.forEach(category => {{
                const option = document.createElement('option');
                option.value = category;
                option.textContent = category;
                categorySelect.appendChild(option);
            }});
        }}

        function filterDocuments() {{
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const selectedCategory = document.getElementById('categoryFilter').value;

            filteredDocuments = allDocuments.filter(doc => {{
                const matchesSearch = !searchTerm || 
                    Object.values(doc).some(value => {{
                        if (Array.isArray(value)) {{
                            return value.some(item => item.toString().toLowerCase().includes(searchTerm));
                        }}
                        return value && value.toString().toLowerCase().includes(searchTerm);
                    }});
                
                const matchesCategory = !selectedCategory || doc.category === selectedCategory;
                
                return matchesSearch && matchesCategory;
            }});

            displayDocuments();
        }}

        function displayDocuments() {{
            const container = document.getElementById('documentsContainer');
            const resultsInfo = document.getElementById('resultsInfo');
            const noResults = document.getElementById('noResults');

            if (filteredDocuments.length === 0) {{
                container.style.display = 'none';
                noResults.style.display = 'block';
                resultsInfo.textContent = '';
                return;
            }}

            noResults.style.display = 'none';
            container.style.display = 'grid';
            resultsInfo.textContent = `${{filteredDocuments.length}} belge gösteriliyor (toplam ${{allDocuments.length}} belge)`;

            container.innerHTML = filteredDocuments.map(doc => createDocumentCard(doc)).join('');
        }}

        function createDocumentCard(doc) {{
            const title = doc.baslik || doc.raporBaslik || 'Başlık bulunamadı';
            
            let metaInfo = '';
            if (doc.yazar) metaInfo += `Yazar: ${{doc.yazar}}<br>`;
            if (doc.hazirlayan) metaInfo += `Hazırlayan: ${{doc.hazirlayan}}<br>`;
            if (doc.yayinlayanKurum) metaInfo += `Kurum: ${{doc.yayinlayanKurum}}<br>`;
            if (doc.basimTarihi) metaInfo += `Basım Tarihi: ${{doc.basimTarihi}}<br>`;
            if (doc.tarih) metaInfo += `Tarih: ${{doc.tarih}}<br>`;
            if (doc.kabulTarihi) metaInfo += `Kabul Tarihi: ${{doc.kabulTarihi}}<br>`;
            if (doc.kanunNo) metaInfo += `Kanun No: ${{doc.kanunNo}}<br>`;
            
            let content = '';
            if (doc.amac) content = doc.amac;
            else if (doc.enerjiIcerigi) {{
                if (Array.isArray(doc.enerjiIcerigi)) {{
                    content = doc.enerjiIcerigi.join('<br><br>');
                }} else {{
                    content = doc.enerjiIcerigi;
                }}
            }}
            else if (doc.cevreIcerigi) content = doc.cevreIcerigi;
            
            if (content.length > 300) {{
                content = content.substring(0, 300) + '...';
            }}
            
            const link = doc.erisimLinki || doc.link || '#';
            
            return `
                <div class="document-card" onclick="window.open('${{link}}', '_blank')">
                    <div class="document-title">${{title}}</div>
                    <div class="document-meta">${{metaInfo}}</div>
                    <div class="document-content">${{content}}</div>
                    <a href="${{link}}" target="_blank" class="document-link" onclick="event.stopPropagation();">
                        Belgeyi Görüntüle
                    </a>
                </div>
            `;
        }}
    </script>

    <!-- Embedded Data -->
    <script>
{js_content}
    </script>
</body>
</html>"""

def convert_excel_to_html(excel_path, html_path, js_variable, title):
    """Convert single Excel file to HTML"""
    
    print(f"Converting {excel_path} to {html_path}...")
    
    # Read Excel file with proper header handling
    try:
        df = pd.read_excel(excel_path, header=1)  # Header is in row 1 (0-indexed)
        print(f"  Loaded {len(df)} rows from Excel")
        print(f"  Columns: {list(df.columns)}")
    except Exception as e:
        print(f"  Error reading Excel file: {e}")
        return False
    
    # Convert to JavaScript
    js_content = excel_to_js_object(df, js_variable)
    
    # Create HTML content
    html_content = create_html_template(title, js_variable, js_content)
    
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
    """Convert all nitel Excel files to HTML"""
    
    print("Starting nitel data conversion...")
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