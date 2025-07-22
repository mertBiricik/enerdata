# WordPress Single HTML Block Improvements

## 🎯 **Constraints**
- Single custom HTML block in WordPress
- All data embedded (no external files)
- All CSS and JavaScript inline
- WordPress theme compatibility

---

## 🚀 **Critical Fixes**

### **1. Fixed Download Function**

```javascript
function downloadCurrentData() {
    try {
        const activeTab = document.querySelector('.energy-dashboard-container .tab-button.active');
        const tabType = activeTab ? activeTab.getAttribute('data-tab') : 'table';
        
        let csvData = [];
        let filename = '';
        
        switch(tabType) {
            case 'table':
                csvData = getCurrentTableData();
                filename = `energy_data_filtered_${startYear || 'all'}-${endYear || 'all'}.csv`;
                break;
            case 'line':
                csvData = extractLineChartData();
                filename = `energy_trends_${startYear || 'all'}-${endYear || 'all'}.csv`;
                break;
            case 'bar':
                csvData = extractBarChartData();
                filename = `energy_comparison_${new Date().toISOString().split('T')[0]}.csv`;
                break;
            default:
                csvData = getCurrentTableData();
                filename = `energy_data_${new Date().toISOString().split('T')[0]}.csv`;
        }
        
        if (csvData && csvData.length > 0) {
            const csvString = convertToCSV(csvData);
            triggerDownload(csvString, filename);
        }
        
    } catch (error) {
        console.error('Download error:', error);
    }
}

function getCurrentTableData() {
    const table = document.querySelector('.energy-dashboard-container table');
    if (!table) return [];
    
    const csvData = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const rowData = [];
        const cells = row.querySelectorAll('td, th');
        cells.forEach(cell => {
            rowData.push(cell.textContent.trim());
        });
        if (rowData.length > 0) {
            csvData.push(rowData);
        }
    });
    
    return csvData;
}

function extractLineChartData() {
    if (!lineChart) return [];
    
    const labels = lineChart.data.labels;
    const datasets = lineChart.data.datasets;
    
    if (!labels || !datasets) return [];
    
    const csvData = [['Year', ...datasets.map(d => d.label)]];
    
    labels.forEach((year, index) => {
        const row = [year];
        datasets.forEach(dataset => {
            row.push(dataset.data[index] || 'N/A');
        });
        csvData.push(row);
    });
    
    return csvData;
}

function extractBarChartData() {
    if (!barChart) return [];
    
    const labels = barChart.data.labels;
    const dataset = barChart.data.datasets[0];
    
    if (!labels || !dataset) return [];
    
    const csvData = [['Category', dataset.label || 'Value']];
    
    labels.forEach((label, index) => {
        csvData.push([label, dataset.data[index] || 'N/A']);
    });
    
    return csvData;
}

function convertToCSV(dataArray) {
    if (!dataArray || dataArray.length === 0) return '';
    
    return dataArray.map(row => 
        row.map(cell => {
            const value = String(cell || '');
            if (value.includes(',') || value.includes('"') || value.includes('\n')) {
                return `"${value.replace(/"/g, '""')}"`;
            }
            return value;
        }).join(',')
    ).join('\r\n');
}

function triggerDownload(csvString, fileName) {
    try {
        const BOM = '\uFEFF';
        const blob = new Blob([BOM + csvString], { 
            type: 'text/csv;charset=utf-8;' 
        });
        
        const link = document.createElement("a");
        const url = URL.createObjectURL(blob);
        link.setAttribute("href", url);
        link.setAttribute("download", fileName);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Download trigger error:', error);
        window.open('data:text/csv;charset=utf-8,' + encodeURIComponent(csvString));
    }
}
```

### **2. Mobile Responsiveness**

```css
@media (max-width: 768px) {
    .energy-dashboard-container .main-container {
        flex-direction: column !important;
        gap: 10px !important;
        padding: 10px !important;
    }
    
    .energy-dashboard-container .filters-panel {
        width: 100% !important;
        height: auto !important;
        max-height: 200px !important;
        overflow-y: auto !important;
        -webkit-overflow-scrolling: touch !important;
    }
    
    .energy-dashboard-container .content-panel {
        width: 100% !important;
    }
    
    .energy-dashboard-container .chart-container {
        height: 250px !important;
        min-height: 250px !important;
    }
    
    .energy-dashboard-container .tab-button {
        font-size: 12px !important;
        padding: 8px 12px !important;
    }
    
    .energy-dashboard-container input[type="checkbox"] {
        transform: scale(1.2) !important;
        margin-right: 8px !important;
    }
    
    .energy-dashboard-container .table-container {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
    }
    
    .energy-dashboard-container table {
        min-width: 600px !important;
    }
}

@media (max-width: 480px) {
    .energy-dashboard-container .filter-group {
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 8px !important;
    }
    
    .energy-dashboard-container .filter-group label {
        font-size: 14px !important;
        font-weight: bold !important;
    }
    
    .energy-dashboard-container .series-checkboxes {
        max-height: 120px !important;
        overflow-y: auto !important;
    }
}
```

### **3. Error Handling**

```javascript
function safeApplyFiltersAndRender() {
    try {
        const checkboxes = document.querySelectorAll('.energy-dashboard-container input[type="checkbox"]:checked');
        const selectedSeriesNames = Array.from(checkboxes).map(cb => cb.value);

        if (selectedSeriesNames.length === 0) {
            alert('Lütfen en az bir veri serisi seçin.');
            return;
        }

        const startYear = parseInt(document.querySelector('.energy-dashboard-container #yearInputStart')?.value) || minYear;
        const endYear = parseInt(document.querySelector('.energy-dashboard-container #yearInputEnd')?.value) || maxYear;

        if (startYear > endYear) {
            alert('Başlangıç yılı bitiş yılından büyük olamaz.');
            return;
        }

        const yearsForCharts = allYearsInData.filter(year => year >= startYear && year <= endYear);
        
        if (yearsForCharts.length === 0) {
            alert('Seçilen yıl aralığında veri bulunmuyor.');
            return;
        }

        // Your existing chart rendering logic here
        renderChartsWithData(selectedSeriesNames, yearsForCharts);
        
    } catch (error) {
        console.error('Error in applyFiltersAndRender:', error);
        alert('Grafik oluşturulurken bir hata oluştu. Lütfen sayfayı yenileyin.');
    }
}

function validateEmbeddedData() {
    try {
        if (typeof embeddedDataA === 'undefined' && 
            typeof embeddedDataB === 'undefined' && 
            typeof embeddedRawData === 'undefined') {
            alert('Veri yüklenemedi. Lütfen sayfayı yenileyin.');
            return false;
        }
        return true;
    } catch (error) {
        console.error('Data validation error:', error);
        return false;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    if (validateEmbeddedData()) {
        initializeDashboard();
    }
});
```

### **4. Table Pagination**

```javascript
function renderPaginatedTable(data, itemsPerPage = 50) {
    if (!data || data.length === 0) {
        return '<p style="text-align: center; color: #666;">Gösterilecek veri yok</p>';
    }
    
    let currentPage = 1;
    const totalPages = Math.ceil(data.length / itemsPerPage);
    
    function renderPage(page) {
        const startIndex = (page - 1) * itemsPerPage;
        const endIndex = Math.min(startIndex + itemsPerPage, data.length);
        const pageData = data.slice(startIndex, endIndex);
        
        let tableHTML = '<table style="width: 100%; border-collapse: collapse;">';
        
        pageData.forEach((row, index) => {
            tableHTML += '<tr>';
            row.forEach(cell => {
                tableHTML += `<td style="border: 1px solid #ddd; padding: 8px;">${cell}</td>`;
            });
            tableHTML += '</tr>';
        });
        
        tableHTML += '</table>';
        
        if (totalPages > 1) {
            tableHTML += `
                <div style="text-align: center; margin-top: 15px;">
                    <button onclick="changePage(${page - 1})" ${page <= 1 ? 'disabled style="opacity: 0.5;"' : ''}>
                        ◀ Önceki
                    </button>
                    <span style="margin: 0 15px;">Sayfa ${page} / ${totalPages}</span>
                    <button onclick="changePage(${page + 1})" ${page >= totalPages ? 'disabled style="opacity: 0.5;"' : ''}>
                        Sonraki ▶
                    </button>
                </div>
            `;
        }
        
        return tableHTML;
    }
    
    window.changePage = function(page) {
        if (page >= 1 && page <= totalPages) {
            currentPage = page;
            const container = document.querySelector('.energy-dashboard-container .table-container');
            if (container) {
                container.innerHTML = renderPage(page);
            }
        }
    };
    
    return renderPage(currentPage);
}
``` 