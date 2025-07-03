# Enerji Tüketimi Verisi (Enerji Tüketimi Veri Görselleştirme Aracı)

## Genel Bakış

Bu proje, Türkiye'nin 1923-2023 yılları arasındaki enerji üretimi, tüketimi ve sektörel dağılımlarını keşfetmek için etkileşimli, web tabanlı veri görselleştirme araçlarından oluşur. [Our World in Data](https://ourworldindata.org) sitesinin tarzı ve kullanılabilirliğinden esinlenilerek, **üç ayrı, özelleşmiş dashboard** sunulmaktadır:

### 🏭 **Dataset A - Birincil Enerjinin Kaynaklara Göre Üretimi ve Tüketimi**
- **Dosya:** `dataset_a_primary_energy.html`
- **Dönem:** 1972-2023
- **Veri:** Birincil enerji üretimi, ithalatı, ihracatı (Bin TEP)
- **Özellikler:** Enerji dengesi analizi, ithalat-ihracat karşılaştırması

### ⚡ **Dataset B - Elektrik Enerjisinin Kaynaklara Göre Kurulu Gücü ve Üretimi**
- **Dosya:** `dataset_b_electricity.html`
- **Dönem:** 1970-2023
- **Veri:** Elektrik üretim kapasitesi ve üretim miktarları (MW/GWh)
- **Özellikler:** Kaynak bazlı filtreleme, üretim vs. kapasite analizi

### 📊 **Dataset C - Elektrik Brüt Üretimi - Sektörel Tüketim Dağılımı**
- **Dosya:** `dataset_c_sectoral_consumption.html`
- **Dönem:** 1923-2023 (100 yıllık veri)
- **Veri:** Sektörel elektrik tüketimi (GWh)
- **Özellikler:** Sektörel kategorileme, pasta grafikleri, asırlık trend analizi

### 🏠 **Ana Giriş Sayfası**
- **Dosya:** `energy_dashboard_index.html`
- **Amaç:** Üç dataset arasında kolay navigasyon
- **Tasarım:** Modern, renkli kartlar ile kullanıcı dostu arayüz

---

## Özellikler

### Ortak Özellikler (Tüm Dashboardlarda)
- **Etkileşimli Filtreler:**  
  - Yıl aralığı seçimi (slider ve sayısal girişlerle)
  - Veri serileri için çoklu seçim
  - "Hepsini Seç" ve "Hiçbirini Seçme" kısayol butonları
  - Gelişmiş arama fonksiyonu

- **Sekmeli Görselleştirme:**  
  - **Tablo:** Seçilen yıllar ve seriler için ham veriler (sabit ilk sütun)
  - **Çizgi Grafik:** Zaman içindeki trendler, Material Design renk paleti
  - **Sütun Grafik:** Hesaplama modu seçimi (Toplam/Ortalama/Son Değer)

- **Veri İndirme & Dışa Aktarma:**  
  - Tüm veri setini CSV olarak indirin
  - Filtrelenmiş verileri CSV olarak indirin

### Özelleşmiş Özellikler

#### Dataset A (Birincil Enerji)
- Enerji dengesi analizi
- İthalat-ihracat karşılaştırması
- Yerli üretim vs. ithalat oranları

#### Dataset B (Elektrik)
- Veri türü filtresi (Tümü/Üretim/Kurulu Güç)
- Kaynak bazında detaylı analiz
- Kapasite kullanım oranları

#### Dataset C (Sektörel Tüketim)
- Pasta grafik desteği
- Sektörel kategorileme (Sanayi/Enerji/Diğer)
- 100 yıllık tarihsel perspektif
- Sektör bazında trend analizi

---

## Nasıl Kullanılır?

### Kullanıcı Olarak

1. **`energy_dashboard_index.html` dosyasını tarayıcınızda açın**
2. İlgilendiğiniz veri setine tıklayın:
   - **Birincil Enerji** → Genel enerji dengesi için
   - **Elektrik** → Elektrik üretimi ve kapasitesi için  
   - **Sektörel Tüketim** → Detaylı sektörel analiz için
3. Her dashboardda filtreleri kullanarak veri setini özelleştirin
4. Sekmeleri kullanarak farklı görselleştirme türleri arasında geçiş yapın
5. İndirme butonlarını kullanarak verileri CSV olarak dışa aktarın

### Geliştirici Olarak

#### Veriyi Güncellemek İçin

1. **Veri kaynaklarını güncelleyin:**
   - Dataset A: `data/a/` klasöründeki Excel dosyaları
   - Dataset B: `data/b/` klasöründeki Excel dosyaları
   - Dataset C: `data/C/` klasöründeki Excel/CSV dosyaları

2. **İşleme scriptlerini çalıştırın:**
   ```bash
   # Dataset A
   cd data/a && python consolidate_energy_data.py && python convert_data_a.py
   
   # Dataset B  
   cd data/b && python clean_electricity_data.py && python convert_data_b.py
   
   # Dataset C
   python excel_to_js.py  # veya csv_to_js.py
   ```

3. **Güncellenmiş veri dosyaları otomatik olarak dashboard'lara yüklenir**

---

## Dosya Yapısı

```
.
├── energy_dashboard_index.html    # 🏠 Ana navigasyon sayfası
├── dataset_a_primary_energy.html  # 🏭 Birincil enerji dashboard'u
├── dataset_b_electricity.html     # ⚡ Elektrik dashboard'u  
├── dataset_c_sectoral_consumption.html # 📊 Sektörel tüketim dashboard'u
│
├── data/
│   ├── a/                         # Birincil enerji verileri
│   │   ├── *.xlsx                 # Kaynak Excel dosyaları
│   │   ├── consolidate_energy_data.py
│   │   ├── convert_data_a.py
│   │   └── data_a_embedded.js     # Dashboard A için hazır veri
│   │
│   ├── b/                         # Elektrik verileri
│   │   ├── *.xlsx                 # Kaynak Excel dosyaları
│   │   ├── clean_electricity_data.py
│   │   ├── convert_data_b.py
│   │   └── data_b_embedded.js     # Dashboard B için hazır veri
│   │
│   └── C/                         # Sektörel tüketim verileri
│       ├── *.xlsx, *.csv          # Kaynak dosyaları
│       └── c_embedded_data.js     # Dashboard C için hazır veri
│
├── excel_to_js.py                 # Excel → JavaScript dönüştürücü
├── csv_to_js.py                   # CSV → JavaScript dönüştürücü
├── embed_complete_data.py         # Birleşik veri gömme aracı
│
├── veri_bankasi.html              # (Eski) Birleşik dashboard
├── index.html                     # (Referans) Standalone araç
├── wordpress_index.html           # (Referans) WordPress uyumlu
│
└── README.md                      # Bu dosya
```

---

## Teknik Detaylar

### Teknoloji Stack'i
- **Frontend:** Pure HTML5, CSS3, JavaScript (framework yok)
- **Grafikler:** Chart.js (Çizgi, Sütun, Pasta grafikleri)
- **UI Bileşenleri:** noUiSlider (yıl aralığı seçimi)
- **Stil:** Custom CSS with Material Design ilkeleri

### Performans Optimizasyonları
- **Ayrılmış Veri Yükleme:** Her dashboard sadece kendi verisini yükler
- **İstemci Tarafı İşleme:** Sunucu gerekmez, anında yanıt
- **Lazy Loading:** Grafikler sadece gerektiğinde oluşturulur
- **Responsive Design:** Mobil ve masaüstü uyumlu

### Veri İşleme Pipeline'ı
1. **Ham Veri:** Excel/CSV formatında kaynak dosyalar
2. **Temizleme:** Python scriptleri ile veri standardizasyonu
3. **Dönüştürme:** JavaScript formatına çevirme
4. **Gömme:** HTML dosyalarına direkt dahil etme
5. **Görselleştirme:** İstemci tarafında dinamik işleme

---

## Yeni Yapının Avantajları

### ✅ **Performans**
- **3x Daha Hızlı Yükleme:** Her sayfa sadece ihtiyacı olan veriyi yükler
- **Düşük Bellek Kullanımı:** Tek seferde sadece bir veri seti aktif
- **Anında Geçiş:** Sayfalar arası hızlı navigasyon

### ✅ **Kullanıcı Deneyimi** 
- **Odaklanmış Arayüz:** Her dataset için optimize edilmiş tasarım
- **Daha Az Karmaşıklık:** Basit, amaca yönelik kontroller
- **Görsel Tutarlılık:** Dataset'e özel renk şemaları

### ✅ **Bakım & Geliştirme**
- **Modüler Yapı:** Her dashboard bağımsız güncellenir
- **Kolay Debug:** Sorunlar izole edilebilir
- **Ölçeklenebilirlik:** Yeni dataset'ler kolayca eklenebilir

### ✅ **SEO & Erişilebilirlik**
- **Daha İyi URL Yapısı:** Her dashboard'un kendi adresi
- **Spesifik Meta Veriler:** Dataset'e özel açıklamalar
- **Paylaşılabilir Linkler:** Direkt dataset erişimi

---

## Eski vs. Yeni Yapı Karşılaştırması

| Özellik | Eski (veri_bankasi.html) | Yeni (Ayrılmış Dashboard'lar) |
|---------|--------------------------|--------------------------------|
| **Dosya Boyutu** | ~225KB (tüm veriler) | ~35-45KB (veri başına) |
| **Yükleme Süresi** | 3-5 saniye | 1-2 saniye |
| **Bellek Kullanımı** | Yüksek (tüm veriler RAM'de) | Düşük (sadece aktif veri) |
| **Kullanıcı Karmaşıklığı** | Yüksek (çok seçenek) | Düşük (odaklanmış) |
| **Bakım Zorluğu** | Zor (tek dev dosya) | Kolay (modüler) |
| **URL Paylaşımı** | Tek URL | Dataset bazında URL'ler |

---

## Geliştirme Roadmap'i

### Kısa Vadeli İyileştirmeler
- [ ] Grafik dışa aktarma (PNG, JPG, TikZ)
- [ ] Gelişmiş filtreleme seçenekleri
- [ ] Veri karşılaştırma araçları

### Orta Vadeli Geliştirmeler  
- [ ] Mobil uygulama desteği
- [ ] Çevrimdışı çalışma modu
- [ ] Veri güncellemelerini otomatik kontrol

### Uzun Vadeli Vizyonlar
- [ ] Makine öğrenmesi ile trend tahminleri
- [ ] Gerçek zamanlı veri entegrasyonu
- [ ] Çoklu dil desteği

---

## Lisans

Bu proje eğitim ve ticari olmayan kullanım için açıktır.  
Veri kaynakları uygun şekilde belirtilmelidir.

---

## İletişim

Sorularınız, önerileriniz veya katkılarınız için lütfen bir issue açın veya proje sorumlusuyla iletişime geçin.

---

**🚀 Yeni Deneyimi Keşfedin!**  
`energy_dashboard_index.html` dosyasını açarak modern, hızlı ve odaklanmış enerji veri analizi deneyimine başlayın!

---

**Context7**:  
Bu README, Context7 ile tam kod ve veri bağlamı kullanılarak güncellenmiştir; tüm talimatlar ve açıklamalar yeni ayrılmış dashboard yapısına göre düzenlenmiştir. 