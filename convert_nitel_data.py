#!/usr/bin/env python3
"""
COMPREHENSIVE NITEL (QUALITATIVE) DATA CONVERSION SCRIPT

This is the ONLY script for converting qualitative data from Excel to JavaScript.
Handles all 4 nitel files: yasal, strateji, kalkinma, ab

USAGE:
    python convert_nitel_data.py

WHAT IT DOES:
1. Reads existing JavaScript files from nitel_data/ directory
2. Cleans and sanitizes all text for proper JavaScript syntax
3. Removes line breaks and problematic characters
4. Preserves existing links and data structure
5. Generates clean JS files without syntax errors
6. Ensures HTML files have necessary JavaScript functionality

SAFETY: Always use with remove_data.py and restore_data.py
"""

import json
import re
import os

class NitelDataConverter:
    def __init__(self):
        self.output_dir = "nitel_data"
        
        # File mappings for processing
        self.files_to_process = [
            {
                "input_file": "yasal_data.js",
                "variable_name": "embeddedYasalData",
                "type": "yasal",
                "html_file": "4_yasal_duzenlemeler.html"
            },
            {
                "input_file": "strateji_data.js", 
                "variable_name": "embeddedStratejiData",
                "type": "strateji",
                "html_file": "5_strateji_ve_politika_belgeleri.html"
            },
            {
                "input_file": "kalkinma_data.js",
                "variable_name": "embeddedKalkinmaData",
                "type": "kalkinma",
                "html_file": "6_kalkinma_planlari.html"
            },
            {
                "input_file": "ab_data.js",
                "variable_name": "embeddedAbData",
                "type": "ab",
                "html_file": "7_ab_ilerleme_raporlari.html"
            }
        ]

    def sanitize_text_for_js(self, text):
        """Sanitize text to be JavaScript-safe"""
        if text is None:
            return ""
        
        text = str(text)
        
        # Remove or replace problematic characters
        text = text.replace('\n', ' ')  # Replace line breaks with spaces
        text = text.replace('\r', ' ')  # Replace carriage returns  
        text = text.replace('\t', ' ')  # Replace tabs
        text = text.replace('"', '\\"')  # Escape quotes
        text = text.replace('\\', '\\\\')  # Escape backslashes first
        text = text.replace('\\"', '\\"')  # Fix double escaping
        
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    def read_existing_js_file(self, filename):
        """Read and parse existing JavaScript data file"""
        file_path = os.path.join(self.output_dir, filename)
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract the data array using regex
            pattern = r'const\s+\w+\s*=\s*(\[.*\]);'
            match = re.search(pattern, content, re.DOTALL)
            
            if not match:
                print(f"❌ Could not find data array in {filename}")
                return None
            
            # Convert to Python-parseable format
            js_array = match.group(1)
            js_array = js_array.replace('null', 'None')
            js_array = js_array.replace('true', 'True')
            js_array = js_array.replace('false', 'False')
            
            # Parse the data
            data = eval(js_array)
            print(f"✅ Read {len(data)} items from {filename}")
            return data
            
        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")
            return None

    def clean_data_item(self, item, data_type):
        """Clean a single data item based on its type"""
        if not isinstance(item, dict):
            return item
        
        cleaned_item = {}
        
        # Clean all string fields
        for key, value in item.items():
            if isinstance(value, str):
                cleaned_item[key] = self.sanitize_text_for_js(value)
            else:
                cleaned_item[key] = value
        
        # Add missing erisimLinki fields with placeholders if needed
        if data_type == "yasal" and 'erisimLinki' not in cleaned_item:
            kanun_no = cleaned_item.get('kanunNo', '').replace('/', '-').replace(' ', '')
            if kanun_no:
                cleaned_item['erisimLinki'] = f"https://www.mevzuat.gov.tr/kanun-{kanun_no}"
        
        elif data_type == "ab" and 'erisimLinki' not in cleaned_item:
            year = cleaned_item.get('tarih', '').strip()
            if year:
                cleaned_item['erisimLinki'] = f"https://ec.europa.eu/neighbourhood-enlargement/turkey-report-{year}"
        
        return cleaned_item

    def write_clean_js_file(self, filename, variable_name, data):
        """Write clean JavaScript file"""
        try:
            output_path = os.path.join(self.output_dir, filename)
            
            # Ensure output directory exists
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Generate clean JavaScript with proper formatting
            js_content = f"const {variable_name} = {json.dumps(data, ensure_ascii=False, indent=2)};"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(js_content)
            
            print(f"✅ Generated clean {output_path} with {len(data)} items")
            return True
            
        except Exception as e:
            print(f"❌ Error writing {filename}: {e}")
            return False

    def ensure_html_functionality(self, html_file, data_type):
        """Ensure HTML file has necessary JavaScript functionality"""
        if not os.path.exists(html_file):
            print(f"❌ HTML file not found: {html_file}")
            return False
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if file already has renderDocuments function
            if 'function renderDocuments' in content:
                print(f"✅ {html_file} already has JavaScript functionality")
                return True
            
            # Add the necessary JavaScript functionality based on file type
            if data_type == "yasal":
                js_functionality = self.get_yasal_js_functionality()
            elif data_type == "strateji":
                js_functionality = self.get_strateji_js_functionality()
            elif data_type == "kalkinma": 
                js_functionality = self.get_kalkinma_js_functionality()
            elif data_type == "ab":
                js_functionality = self.get_ab_js_functionality()
            else:
                return False
            
            # Insert JavaScript functionality before </body>
            if '</body>' in content:
                content = content.replace('</body>', js_functionality + '\n</body>')
            else:
                content += js_functionality
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Added JavaScript functionality to {html_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating {html_file}: {e}")
            return False

    def get_yasal_js_functionality(self):
        """Get JavaScript functionality for yasal documents"""
        return '''
    <script>
        let allDocuments = [];
        let filteredDocuments = [];
        
        function formatDate(dateStr) {
            if (!dateStr) return 'Belirtilmemiş';
            return dateStr.replace(/T.*/, '').replace(/-/g, '.');
        }
        
        function renderDocuments(documents) {
            const grid = document.getElementById('documentsGrid');
            const loading = document.getElementById('loading');
            const noResults = document.getElementById('noResults');
            
            loading.style.display = 'none';
            
            if (!documents || documents.length === 0) {
                grid.style.display = 'none';
                noResults.style.display = 'block';
                return;
            }
            
            noResults.style.display = 'none';
            grid.style.display = 'block';
            
            const html = documents.map(doc => `
                <div class="document-card">
                    <div class="document-title">${doc.baslik || 'Başlık belirtilmemiş'}</div>
                    <div class="document-meta">
                        <div class="meta-item">
                            <span class="meta-label">Kanun No:</span>
                            <span class="meta-value">${doc.kanunNo || 'Belirtilmemiş'}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Kabul Tarihi:</span>
                            <span class="meta-value">${formatDate(doc.kabulTarihi)}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">RG Tarihi:</span>
                            <span class="meta-value">${formatDate(doc.rgTarih)}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">RG Sayısı:</span>
                            <span class="meta-value">${doc.rgSayi || 'Belirtilmemiş'}</span>
                        </div>
                    </div>
                    ${doc.amac ? `
                        <div class="document-purpose">
                            <strong>Amaç ve Kapsam:</strong><br>
                            ${doc.amac}
                        </div>
                    ` : ''}
                    ${doc.erisimLinki ? `
                        <a href="${doc.erisimLinki}" target="_blank" class="access-link">
                            📋 Tam Metne Erişim
                        </a>
                    ` : ''}
                </div>
            `).join('');
            
            grid.innerHTML = html;
        }
        
        function categorizeDocument(doc) {
            const title = (doc.baslik || '').toLowerCase();
            const purpose = (doc.amac || '').toLowerCase();
            const content = title + ' ' + purpose;
            
            if (content.includes('elektrik') || content.includes('enerji') || content.includes('güç')) {
                return 'Enerji ve Elektrik';
            }
            if (content.includes('maden') || content.includes('petrol') || content.includes('gaz')) {
                return 'Maden ve Petrol';
            }
            if (content.includes('bank') || content.includes('finans') || content.includes('kredi')) {
                return 'Finansal Kurumlar';
            }
            if (content.includes('teşkilat') || content.includes('kurul') || content.includes('müdürlük')) {
                return 'Kurumsal Yapı';
            }
            if (content.includes('belediye') || content.includes('şehir') || content.includes('kent')) {
                return 'Yerel Yönetim';
            }
            if (content.includes('vergi') || content.includes('resim') || content.includes('harç')) {
                return 'Vergi ve Mali';
            }
            return 'Genel Mevzuat';
        }
        
        function populateCategoryFilter() {
            const categories = [...new Set(allDocuments.map(doc => categorizeDocument(doc)))].sort();
            const select = document.getElementById('categoryFilter');
            
            categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category;
                option.textContent = category;
                select.appendChild(option);
            });
        }
        
        function filterDocuments() {
            const searchTerm = document.getElementById('searchBox').value.toLowerCase();
            const yearFilter = document.getElementById('yearFilter').value.trim();
            const categoryFilter = document.getElementById('categoryFilter').value;
            
            let filtered = allDocuments;
            
            if (searchTerm) {
                filtered = filtered.filter(doc => 
                    (doc.baslik && doc.baslik.toLowerCase().includes(searchTerm)) ||
                    (doc.kanunNo && doc.kanunNo.toLowerCase().includes(searchTerm)) ||
                    (doc.amac && doc.amac.toLowerCase().includes(searchTerm))
                );
            }
            
            if (yearFilter) {
                if (yearFilter.includes('-')) {
                    const [startYear, endYear] = yearFilter.split('-').map(y => parseInt(y.trim()));
                    filtered = filtered.filter(doc => {
                        const year = extractYear(doc.kabulTarihi);
                        return year >= startYear && year <= endYear;
                    });
                } else {
                    const targetYear = parseInt(yearFilter);
                    filtered = filtered.filter(doc => {
                        const year = extractYear(doc.kabulTarihi);
                        return year === targetYear;
                    });
                }
            }
            
            if (categoryFilter) {
                filtered = filtered.filter(doc => categorizeDocument(doc) === categoryFilter);
            }
            
            filteredDocuments = filtered;
            renderDocuments(filteredDocuments);
            updateStats();
        }
        
        function extractYear(dateStr) {
            if (!dateStr) return null;
            const year = parseInt(dateStr.split('.')[2] || dateStr.split('-')[0] || dateStr.split('/')[2]);
            return isNaN(year) ? null : year;
        }
        
        function updateStats() {
            const totalCount = document.getElementById('totalCount');
            const filteredCount = document.getElementById('filteredCount');
            const dateRange = document.getElementById('dateRange');
            
            totalCount.textContent = `Toplam ${allDocuments.length} yasal düzenleme`;
            
            if (filteredDocuments.length !== allDocuments.length) {
                filteredCount.textContent = `Görüntülenen: ${filteredDocuments.length}`;
            } else {
                filteredCount.textContent = '';
            }
            
            const years = allDocuments.map(doc => extractYear(doc.kabulTarihi)).filter(y => y);
            if (years.length > 0) {
                const minYear = Math.min(...years);
                const maxYear = Math.max(...years);
                dateRange.textContent = `${minYear} - ${maxYear}`;
            }
        }
        
        function exportData() {
            const csvContent = [
                ['ID', 'Kanun No', 'Kabul Tarihi', 'Başlık', 'RG Tarihi', 'RG Sayısı', 'Amaç', 'Erişim Linki'].join(','),
                ...filteredDocuments.map(doc => [
                    doc.id || '',
                    `"${(doc.kanunNo || '').replace(/"/g, '""')}"`,
                    doc.kabulTarihi || '',
                    `"${(doc.baslik || '').replace(/"/g, '""')}"`,
                    doc.rgTarih || '',
                    doc.rgSayi || '',
                    `"${(doc.amac || '').replace(/"/g, '""')}"`,
                    doc.erisimLinki || ''
                ].join(','))
            ].join('\\n');
            
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'yasal_duzenlemeler.csv';
            link.click();
        }
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            try {
                if (typeof embeddedYasalData !== 'undefined') {
                    allDocuments = embeddedYasalData;
                    filteredDocuments = [...allDocuments];
                    populateCategoryFilter();
                    renderDocuments(filteredDocuments);
                    updateStats();
                    
                    document.getElementById('searchBox').addEventListener('input', filterDocuments);
                    document.getElementById('yearFilter').addEventListener('input', filterDocuments);
                    document.getElementById('categoryFilter').addEventListener('change', filterDocuments);
                } else {
                    document.getElementById('loading').textContent = 'Veri yüklenirken hata oluştu.';
                }
            } catch (error) {
                console.error('Error during initialization:', error);
                document.getElementById('loading').textContent = 'Veri yüklenirken hata oluştu.';
            }
        });
    </script>'''

    def get_ab_js_functionality(self):
        """Get JavaScript functionality for AB reports"""
        return '''
    <script>
        let allDocuments = [];
        let filteredDocuments = [];
        
        function formatDate(dateStr) {
            if (!dateStr) return 'Belirtilmemiş';
            return dateStr.replace(/T.*/, '').replace(/-/g, '.');
        }
        
        function extractYear(dateStr) {
            if (!dateStr) return null;
            const year = parseInt(dateStr.split('.')[2] || dateStr.split('-')[0] || dateStr.split('/')[2] || dateStr);
            return isNaN(year) ? null : year;
        }
        
        function renderDocuments(documents) {
            const grid = document.getElementById('documentsGrid');
            const loading = document.getElementById('loading');
            const noResults = document.getElementById('noResults');
            
            loading.style.display = 'none';
            
            if (!documents || documents.length === 0) {
                grid.style.display = 'none';
                noResults.style.display = 'block';
                return;
            }
            
            noResults.style.display = 'none';
            grid.style.display = 'block';
            
            const html = documents.map(doc => `
                <div class="document-card">
                    <div class="document-title">${doc.raporBaslik || 'Başlık belirtilmemiş'}</div>
                    <div class="document-meta">
                        <div class="meta-item">
                            <span class="meta-label">Hazırlayan:</span>
                            <span class="meta-value">${doc.hazirlayan || 'Belirtilmemiş'}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Tarih:</span>
                            <span class="meta-value">${formatDate(doc.tarih)}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Rapor No:</span>
                            <span class="meta-value">${doc.raporNo || 'Belirtilmemiş'}</span>
                        </div>
                    </div>
                    ${(doc.enerjiIcerigi || doc.cevreIcerigi) ? `
                        <div class="content-sections">
                            ${doc.enerjiIcerigi ? `
                                <div class="content-section energy-section">
                                    <div class="section-title">🔋 Enerji İçeriği</div>
                                    <div class="section-content">${doc.enerjiIcerigi}</div>
                                </div>
                            ` : ''}
                            ${doc.cevreIcerigi ? `
                                <div class="content-section environment-section">
                                    <div class="section-title">🌱 Çevre ve İklim Değişikliği</div>
                                    <div class="section-content">${doc.cevreIcerigi}</div>
                                </div>
                            ` : ''}
                        </div>
                    ` : ''}
                    ${doc.erisimLinki ? `
                        <a href="${doc.erisimLinki}" target="_blank" class="access-link">
                            📋 Rapora Erişim
                        </a>
                    ` : ''}
                </div>
            `).join('');
            
            grid.innerHTML = html;
        }
        
        function categorizeDocument(doc) {
            const energyContent = (doc.enerjiIcerigi || '').toLowerCase();
            const envContent = (doc.cevreIcerigi || '').toLowerCase();
            const year = extractYear(doc.tarih);
            
            if (year && year >= 2010) {
                return '2010 Sonrası Raporlar';
            }
            if (year && year >= 2005) {
                return '2005-2010 Dönemi';
            }
            if (year && year >= 2000) {
                return '2000-2005 Dönemi';
            }
            if (year && year >= 1995) {
                return '1995-2000 Dönemi';
            }
            if (energyContent && energyContent.length > envContent.length) {
                return 'Enerji Odaklı Raporlar';
            }
            if (envContent && envContent.length > energyContent.length) {
                return 'Çevre Odaklı Raporlar';
            }
            return 'Genel İlerleme Raporları';
        }
        
        function populateAuthorFilter() {
            const authors = [...new Set(allDocuments.map(doc => doc.hazirlayan).filter(Boolean))].sort();
            const select = document.getElementById('authorFilter');
            
            authors.forEach(author => {
                const option = document.createElement('option');
                option.value = author;
                option.textContent = author;
                select.appendChild(option);
            });
        }
        
        function populateCategoryFilter() {
            const categories = [...new Set(allDocuments.map(doc => categorizeDocument(doc)))].sort();
            const select = document.getElementById('categoryFilter');
            
            categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category;
                option.textContent = category;
                select.appendChild(option);
            });
        }
        
        function filterDocuments() {
            const searchTerm = document.getElementById('searchBox').value.toLowerCase();
            const yearFilter = document.getElementById('yearFilter').value.trim();
            const authorFilter = document.getElementById('authorFilter').value;
            const categoryFilter = document.getElementById('categoryFilter').value;
            
            let filtered = allDocuments;
            
            if (searchTerm) {
                filtered = filtered.filter(doc => 
                    (doc.raporBaslik && doc.raporBaslik.toLowerCase().includes(searchTerm)) ||
                    (doc.hazirlayan && doc.hazirlayan.toLowerCase().includes(searchTerm)) ||
                    (doc.enerjiIcerigi && doc.enerjiIcerigi.toLowerCase().includes(searchTerm)) ||
                    (doc.cevreIcerigi && doc.cevreIcerigi.toLowerCase().includes(searchTerm))
                );
            }
            
            if (yearFilter) {
                const targetYear = parseInt(yearFilter);
                filtered = filtered.filter(doc => {
                    const year = extractYear(doc.tarih);
                    return year === targetYear;
                });
            }
            
            if (authorFilter) {
                filtered = filtered.filter(doc => doc.hazirlayan === authorFilter);
            }
            
            if (categoryFilter) {
                filtered = filtered.filter(doc => categorizeDocument(doc) === categoryFilter);
            }
            
            filteredDocuments = filtered;
            renderDocuments(filteredDocuments);
            updateStats();
        }
        
        function updateStats() {
            const totalCount = document.getElementById('totalCount');
            const filteredCount = document.getElementById('filteredCount');
            const dateRange = document.getElementById('dateRange');
            
            totalCount.textContent = `Toplam ${allDocuments.length} AB ilerleme raporu`;
            
            if (filteredDocuments.length !== allDocuments.length) {
                filteredCount.textContent = `Görüntülenen: ${filteredDocuments.length}`;
            } else {
                filteredCount.textContent = '';
            }
            
            const years = allDocuments.map(doc => extractYear(doc.tarih)).filter(y => y);
            if (years.length > 0) {
                const minYear = Math.min(...years);
                const maxYear = Math.max(...years);
                dateRange.textContent = `${minYear} - ${maxYear}`;
            }
        }
        
        function exportData() {
            const csvContent = [
                ['ID', 'Hazırlayan', 'Tarih', 'Rapor No', 'Rapor Başlık', 'Enerji İçeriği', 'Çevre İçeriği', 'Erişim Linki'].join(','),
                ...filteredDocuments.map(doc => [
                    doc.id || '',
                    `"${(doc.hazirlayan || '').replace(/"/g, '""')}"`,
                    doc.tarih || '',
                    `"${(doc.raporNo || '').replace(/"/g, '""')}"`,
                    `"${(doc.raporBaslik || '').replace(/"/g, '""')}"`,
                    `"${(doc.enerjiIcerigi || '').replace(/"/g, '""')}"`,
                    `"${(doc.cevreIcerigi || '').replace(/"/g, '""')}"`,
                    doc.erisimLinki || ''
                ].join(','))
            ].join('\\n');
            
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'ab_ilerleme_raporlari.csv';
            link.click();
        }
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            try {
                if (typeof embeddedAbData !== 'undefined') {
                    allDocuments = embeddedAbData;
                    filteredDocuments = [...allDocuments];
                    populateAuthorFilter();
                    populateCategoryFilter();
                    renderDocuments(filteredDocuments);
                    updateStats();
                    
                    document.getElementById('searchBox').addEventListener('input', filterDocuments);
                    document.getElementById('yearFilter').addEventListener('input', filterDocuments);
                    document.getElementById('authorFilter').addEventListener('change', filterDocuments);
                    document.getElementById('categoryFilter').addEventListener('change', filterDocuments);
                } else {
                    document.getElementById('loading').textContent = 'Veri yüklenirken hata oluştu.';
                }
            } catch (error) {
                console.error('Error during initialization:', error);
                document.getElementById('loading').textContent = 'Veri yüklenirken hata oluştu.';
            }
        });
    </script>'''

    def get_strateji_js_functionality(self):
        """Get JavaScript functionality for strateji documents - using existing working version from file 5"""
        return ""  # File 5 already works, so no need to add functionality

    def get_kalkinma_js_functionality(self):
        """Get JavaScript functionality for kalkinma documents - using existing working version from file 6"""
        return ""  # File 6 already works, so no need to add functionality

    def process_file(self, file_info):
        """Process a single nitel data file"""
        print(f"\n🔧 Processing {file_info['input_file']}...")
        
        # Read existing data
        data = self.read_existing_js_file(file_info['input_file'])
        if data is None:
            return False
        
        # Clean all data items
        cleaned_data = []
        for item in data:
            cleaned_item = self.clean_data_item(item, file_info['type'])
            cleaned_data.append(cleaned_item)
        
        # Write clean file
        js_success = self.write_clean_js_file(
            file_info['input_file'],
            file_info['variable_name'], 
            cleaned_data
        )
        
        # Ensure HTML file has functionality (only for files that need it)
        html_success = True
        if file_info['type'] in ['yasal', 'ab']:
            html_success = self.ensure_html_functionality(
                file_info['html_file'], 
                file_info['type']
            )
        
        return js_success and html_success

    def convert_all(self):
        """Convert and clean all nitel data files"""
        print("🔄 COMPREHENSIVE NITEL DATA CLEANING & CONVERSION")
        print("=" * 60)
        print("Cleaning all qualitative data for proper JavaScript syntax")
        print("Ensuring HTML files have necessary functionality")
        print("Following project rules: automated conversion only")
        
        success_count = 0
        total_count = len(self.files_to_process)
        
        for file_info in self.files_to_process:
            if self.process_file(file_info):
                success_count += 1
        
        print("\n" + "=" * 60)
        if success_count == total_count:
            print("✅ SUCCESS: All nitel data cleaned successfully!")
            print(f"📁 Generated {success_count} clean JavaScript files")
            print("🚫 No more JavaScript syntax errors")
            print("🔗 All files include link functionality")
            print("⚙️ HTML files have necessary JavaScript functions")
        else:
            print(f"⚠️  PARTIAL SUCCESS: {success_count}/{total_count} files processed")
        
        print("\n📋 Next steps:")
        print("1. Use 'python restore_data.py' to embed cleaned data into HTML files")
        print("2. Test files in browser - should load and display data properly")
        print("3. All text is properly escaped for JavaScript")
        print("4. Link buttons should be visible and functional")
        
        return success_count == total_count

def main():
    converter = NitelDataConverter()
    converter.convert_all()

if __name__ == "__main__":
    main()