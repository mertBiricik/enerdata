# Enerji Tüketimi Verisi (Enerji Tüketimi Veri Görselleştirme Aracı)

## Genel Bakış

Bu proje, Türkiye'nin 1923-2023 yılları arasındaki enerji üretimi, tüketimi ve sektörel dağılımlarını keşfetmek için etkileşimli, web tabanlı bir veri görselleştirme aracıdır. [Our World in Data](https://ourworldindata.org) sitesinin tarzı ve kullanılabilirliğinden esinlenilmiştir. Kullanıcılar şunları yapabilir:

- Enerji verilerini tablo, çizgi grafik veya sütun grafik olarak görüntüleyebilir.
- Yıl aralığı ve veri serisine (ör. Net Üretim, İthalat, İhracat, sektörel tüketim) göre filtreleme yapabilir.
- Tüm veri setini veya filtrelenmiş alt kümeleri CSV olarak indirebilir.

Tüm veriler istemci tarafında gömülü ve işlenmektedir; bu da maksimum şeffaflık ve tekrarlanabilirlik sağlar.

---

## Özellikler

- **Etkileşimli Filtreler:**  
  - Hem çizgi hem de sütun grafik için kullanılan yıl aralığı seçimi (slider ve sayısal girişlerle).
  - Veri serileri (kategori/sektör) için çoklu seçim.
  - Seri seçimleri için "Hepsini Seç" ve "Hiçbirini Seçme" kısayol butonları.

- **Sekmeli Görselleştirme:**  
  - **Tablo:** Seçilen yıllar ve seriler için ham verileri görüntüleyin. İlk sütun ("Kategori") yatay kaydırmada her zaman görünür (sabit). Satırlar okunabilirlik için şeritli (çizgili) renklendirilmiştir.
  - **Çizgi Grafik:** Herhangi bir seri kombinasyonu için zaman içindeki eğilimleri, canlı Material Design renk paletiyle görselleştirin.
  - **Sütun Grafik:** Seçilen yıl aralığı için seriler arasında karşılaştırma yapın. Kullanıcılar, her serinin toplamını veya ortalamasını göstermek arasında geçiş yapabilir.

- **Veri İndirme & Dışa Aktarma:**  
  - Tüm veri setini CSV olarak indirin.
  - Şu anda filtrelenmiş verileri CSV olarak indirin.
  - Grafikleri PNG ve JPG (JPG için beyaz arka plan) olarak dışa aktarın.
  - Grafikleri LaTeX belgelerinde kullanmak için TikZ kodu olarak dışa aktarın.

- **Duyarlı Arayüz & Türkçe Yerelleştirme:**  
  - Geliştirilmiş Türkçe etiketlerle (ör. "Temsil Türü", "Filtrelenmiş Veri") temiz, modern tasarım.
  - Masaüstü ve mobilde sorunsuz çalışır.

---

## Veri Kaynakları & Yapısı

### Ana Veri

- **Dosya:** `index.html` içinde `embeddedRawData` olarak gömülü (isteğe bağlı olarak `embedded_data.js` dosyasında da mevcut).
- **Kaynak:** Aslen `source.xlsx` ve `1923-2023.csv` dosyalarından.
- **Kategoriler:**  
  - Üst düzey: Net Üretim, İthalat (+), İhracat (-), Elektrik Arzı vb.
  - Sektörel: Gıda, Tekstil, Kimya-Petrokimya, Ulaştırma vb.
- **Yıllar:** 1923–2023 (her seri tüm yıllara sahip olmayabilir).
- **Özel Değerler:**  
  - Parantez içindeki sayılar (ör. `(100)`) orijinal Excel'de kırmızıyla vurgulanan değerleri gösterir (genellikle negatif veya özel durumlar).

### Kategori Metaverisi

- **Dosya:** `categories.csv`
- **Amaç:** Sektörel dağılımlar için üst ve alt kategorileri eşler.

### Veri İşleme

- **Excel'den JS'ye:**  
  - `excel_to_js.py`, `source.xlsx`'i okuyup kırmızı/parantezli değerleri koruyarak `embedded_data.js` üretir.
- **CSV'den JS'ye:**  
  - `csv_to_js.py`, `1923-2023.csv`'yi okuyup `embedded_data.js` üretir.

---

## Nasıl Çalışır?

### 1. Veri Gömme

Tüm veriler, hızlı ve çevrimdışı erişim için `index.html` içinde bir JavaScript dizisi (`embeddedRawData`) olarak gömülüdür.

### 2. Arayüz & Görselleştirme

- **Filtreler:**  
  - Yıl aralığı noUiSlider ve sayısal girişlerle kontrol edilir.
  - Veri serileri, veriden otomatik olarak oluşturulan onay kutuları ile seçilir.

- **Sekmeler:**  
  - Tablo, Çizgi Grafik ve Sütun Grafik görünümleri arasında geçiş yapın.

- **Grafikler:**  
  - [Chart.js](https://www.chartjs.org/) ile oluşturulur.
  - Her seri için benzersiz ve canlı bir renk atanır.
  - Sütun grafik, ana yıl aralığına bağlıdır ve toplama/ortalama seçimi yapılabilir.

- **İndirme:**  
  - "Tam Veri (CSV)" tüm veri setini indirir.
  - "Filtrelenmiş Veri (CSV)" yalnızca tabloda gösterilen verileri indirir.

### 3. Veri İndirme

- CSV'ler, mevcut filtre durumuna veya tüm veri setine göre istemci tarafında oluşturulur.

---

## Dosya Yapısı

```
.
├── index.html              # Ana uygulama, tüm mantık ve veri gömülü
├── embedded_data.js        # (İsteğe bağlı) Ayrı JS veri dizisi, Excel/CSV'den üretilir
├── source.xlsx             # Orijinal Excel veri kaynağı
├── 1923-2023.csv           # Ana CSV veri kaynağı
├── categories.csv          # Kategori/alt kategori eşlemesi
├── excel_to_js.py          # Excel'den JS veri dizisine dönüştürme scripti
├── csv_to_js.py            # CSV'den JS veri dizisine dönüştürme scripti
├── code_analysis_report.md # (Referans) Gereksinim ve kod analizi
├── data-section-requirements.md # (Referans) Proje gereksinimleri
```

---

## Kullanım

### Kullanıcı Olarak

1. **`index.html` dosyasını tarayıcınızda açın.**
2. Üstteki filtreleri kullanarak yıl aralığı ve veri serilerini seçin.
3. Tablo, Çizgi Grafik ve Sütun Grafik sekmeleri arasında geçiş yapın.
4. İndirme butonlarını kullanarak verileri CSV olarak dışa aktarın.

### Geliştirici Olarak

#### Veriyi Güncellemek İçin

1. **`source.xlsx` veya `1923-2023.csv`** dosyalarını yeni verilerle güncelleyin.
2. Uygun scripti çalıştırın:
   - Excel için:  
     ```
     python excel_to_js.py
     ```
   - CSV için:  
     ```
     python csv_to_js.py
     ```
3. Yeni `embedded_data.js` içeriğini `index.html`'deki `<script>` bölümüne kopyalayın (veya ayrı dosya olarak dahil edin).

#### Kategorileri Değiştirmek İçin

- Kategori/alt kategori eşleşmelerini güncellemek için `categories.csv` dosyasını düzenleyin.

---

## Gereksinimler

- Sunucu gerekmez; statik HTML dosyası olarak çalışır.
- Modern tarayıcı (Chrome, Firefox, Edge, Safari).
- [Chart.js](https://cdn.jsdelivr.net/npm/chart.js) ve [noUiSlider](https://cdn.jsdelivr.net/npm/nouislider) CDN üzerinden yüklenir.

---

## Referans & Tasarım

- **Tasarım esin kaynağı:** [Our World in Data](https://ourworldindata.org/grapher/global-energy-substitution)
- **Gereksinimler:** Tam detay için `data-section-requirements.md` dosyasına bakınız.

---

## Genişletme & Özelleştirme

- **Yeni veri serisi eklemek:**  
  - Veri kaynağınızı güncelleyin ve `embedded_data.js`'yi yeniden oluşturun.
- **Renk paletini değiştirmek:**  
  - `index.html` içindeki renk fonksiyonunu güncelleyin.
- **Yeni grafik veya filtre eklemek:**  
  - Gerekli JavaScript kodunu `index.html`'e ekleyin.

---

## Lisans

Bu proje eğitim ve ticari olmayan kullanım için açıktır.  
Veri kaynakları uygun şekilde belirtilmelidir.

---

## İletişim

Sorularınız veya katkılarınız için lütfen bir issue açın veya proje sorumlusuyla iletişime geçin.

---

**Context7**:  
Bu README, Context7 ile tam kod ve veri bağlamı kullanılarak oluşturulmuştur; tüm talimatlar ve açıklamalar güncel ve uygulanabilirdir.

---

# English Version Below

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