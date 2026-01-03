
const fs = require('fs');
const path = '/home/ottobeeth/Downloads/enerdata/backup_html/1_birincil_enerjinin_kaynaklara_gore_uretimi_ve_tuketimi.html';

try {
    const content = fs.readFileSync(path, 'utf8');

    // Extract embeddedDataA
    const startMarker = 'const embeddedDataA = [';
    const endMarker = '];'; // Assuming it's followed by newline or generic end

    const startIndex = content.indexOf(startMarker);
    if (startIndex === -1) {
        throw new Error('Could not find embeddedDataA start');
    }

    // Find the matching closing bracket? Or just search for the next variable declaration or script end?
    // Based on previous views, it ends with ]; on a new line
    const endIndex = content.indexOf('];', startIndex);
    if (endIndex === -1) {
        throw new Error('Could not find embeddedDataA end');
    }

    const jsonStr = content.substring(startIndex + startMarker.length - 1, endIndex + 1);

    // Use eval because it might be JS object literal, not strict JSON (e.g. unquoted keys or comments)
    // Wrap in () to make it an expression
    const data = eval('(' + jsonStr + ')');

    console.log('Successfully parsed embeddedDataA. Length:', data.length);

    // Check for issues
    let issues = 0;
    data.forEach((item, index) => {
        Object.keys(item).forEach(key => {
            if (key === 'Kategori') return;

            const val = item[key];
            const type = typeof val;

            if (val !== null && type !== 'number' && type !== 'string') {
                console.log(`[Issue] Index ${index}, Key "${key}": Value is type "${type}"`, val);
                issues++;
            } else if (type === 'object' && val !== null) {
                // Should be covered above but double check
                console.log(`[Issue] Index ${index}, Key "${key}": Value is object`, val);
                issues++;
            }

            if (key === '1971' && type === 'object' && val !== null) {
                console.log('FOUND THE SMOKING GUN: 1971 is an object!');
            }
        });
    });

    console.log(`Verification complete. Found ${issues} issues.`);

} catch (e) {
    console.error('Error:', e);
}
