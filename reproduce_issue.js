
// Mock data derived from File 1
const embeddedDataA = [
    {
        "Kategori": "Test Category 1",
        "1972": 100,
        "1973": 110,
        "1974": 120
    },
    {
        "Kategori": "Test Category 2",
        "1972": 200,
        "1973": 210,
        "1974": 220
    }
];

// Global variables simulation
let allYears = [];
let startYear = 1972;
let endYear = 1974;
let currentFilteredData = [];

// Initialize allYears
embeddedDataA.forEach(item => {
    Object.keys(item).forEach(key => {
        if (key !== 'Kategori' && !isNaN(parseInt(key))) {
            const year = parseInt(key);
            if (!allYears.includes(year)) {
                allYears.push(year);
            }
        }
    });
});
allYears.sort((a, b) => a - b);
console.log('allYears:', allYears);

// Function to simulate applyFiltersAndRender
function applyFiltersAndRender(selectedSeriesNames) {
    const data = embeddedDataA;
    const yearsInRange = allYears.filter(year => year >= startYear && year <= endYear);
    console.log('applyFiltersAndRender yearsInRange:', yearsInRange);

    currentFilteredData = selectedSeriesNames.map(seriesName => {
        const seriesData = data.find(item => item.Kategori === seriesName);
        if (!seriesData) return null;

        const result = { Kategori: seriesName };
        yearsInRange.forEach(year => {
            result[year] = seriesData[year];
        });
        return result;
    }).filter(item => item !== null);

    console.log('currentFilteredData:', JSON.stringify(currentFilteredData, null, 2));
}

// Function to simulate convertToCSV from File 1
function convertToCSV(data, years) {
    const headers = ['Kategori', ...years.map(String)];
    const rows = [headers];

    data.forEach(item => {
        const row = [item.Kategori];
        years.forEach(year => {
            // BUG SIMULATION: what if year is string in years array but currentFilteredData expects string key?
            // JS handles it.
            let value = item[year];
            if (value === null || value === undefined) {
                value = '';
            }
            row.push(value);
        });
        rows.push(row);
    });

    return rows.map(row =>
        row.map(cell => {
            const str = String(cell);
            return str.includes(',') ? `"${str}"` : str;
        }).join(',')
    ).join('\r\n');
}

// Function to simulate downloadData
function downloadData(type) {
    let data;

    if (type === 'full') {
        const allData = embeddedDataA;
        data = convertToCSV(allData, allYears);
    } else {
        if (currentFilteredData.length === 0) {
            console.log('No currentFilteredData');
            return;
        }
        const yearsInRange = allYears.filter(year => year >= startYear && year <= endYear);
        console.log('downloadData yearsInRange:', yearsInRange);
        data = convertToCSV(currentFilteredData, yearsInRange);
    }

    console.log(`--- CSV Output (${type}) ---`);
    console.log(data);
}

// Test Case 1: Full range
console.log('\n--- Test Case 1: Full Range ---');
applyFiltersAndRender(['Test Category 1']);
downloadData('filtered');

// Test Case 2: Partial range
console.log('\n--- Test Case 2: Partial Range (1973 only) ---');
startYear = 1973;
endYear = 1973;
applyFiltersAndRender(['Test Category 1']); // Simulate updated render
downloadData('filtered');

// Test Case 4: String inputs
console.log('\n--- Test Case 4: String inputs ---');
startYear = "1973"; // Simulate string input
endYear = "1974";
applyFiltersAndRender(['Test Category 1']);
downloadData('filtered');
