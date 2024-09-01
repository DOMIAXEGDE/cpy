document.addEventListener('DOMContentLoaded', function() {
    const charsetConfig = [
        { name: 'Basic Latin', range: [0x0020, 0x007F] },
        { name: 'Latin-1 Supplement', range: [0x0080, 0x00FF] },
        { name: 'Latin Extended-A', range: [0x0100, 0x017F] },
        { name: 'Latin Extended-B', range: [0x0180, 0x024F] },
        { name: 'Greek and Coptic', range: [0x0370, 0x03FF] },
        { name: 'Cyrillic', range: [0x0400, 0x04FF] },
        { name: 'Arabic', range: [0x0600, 0x06FF] },
        { name: 'Hebrew', range: [0x0590, 0x05FF] },
        { name: 'Devanagari', range: [0x0900, 0x097F] },
        { name: 'Mathematical Operators', range: [0x2200, 0x22FF] },
        { name: 'Supplemental Mathematical Operators', range: [0x2A00, 0x2AFF] },
        { name: 'Miscellaneous Technical', range: [0x2300, 0x23FF] },
        { name: 'Miscellaneous Symbols and Arrows', range: [0x2190, 0x21FF] },
        { name: 'CJK Unified Ideographs', range: [0x4E00, 0x9FFF] },
        { name: 'Hangul Syllables', range: [0xAC00, 0xD7AF] },
        { name: 'Hiragana', range: [0x3040, 0x309F] },
        { name: 'Katakana', range: [0x30A0, 0x30FF] },
        { name: 'Bopomofo', range: [0x3100, 0x312F] },
        { name: 'Currency Symbols', range: [0x20A0, 0x20CF] }, // Currency symbols like €, £, ¥, etc.
        { name: 'Additional Punctuation', range: [0x2000, 0x206F] },
        // Additional symbols and characters can be added similarly.
    ];

    function generateCharsetFromConfig(config) {
        const charset = new Set();
        config.forEach(block => {
            for (let i = block.range[0]; i <= block.range[1]; i++) {
                try {
                    charset.add(String.fromCharCode(i));
                } catch (e) {
                    console.error(`Failed to add character code ${i}: ${e.message}`);
                }
            }
        });
        // Explicitly add newline character
        charset.add('\n');
        charset.add('\t');
        return Array.from(charset);
    }

    const uniqueCharset = generateCharsetFromConfig(charsetConfig);
    console.log(uniqueCharset);

    document.getElementById('main-menu').style.display = 'block';

    function showOption(optionId) {
        const options = document.querySelectorAll('#option-container > div');
        options.forEach(opt => opt.style.display = 'none');
        document.getElementById(optionId).style.display = 'block';
        document.getElementById('option-container').style.display = 'block';
    }

    document.getElementById('show-generate-combinations').addEventListener('click', () => showOption('generate-combinations'));
    document.getElementById('show-calculate-string-id').addEventListener('click', () => showOption('calculate-string-id'));
    document.getElementById('show-decode-id').addEventListener('click', () => showOption('decode-id'));
    document.getElementById('show-find-optimal-variable').addEventListener('click', () => showOption('find-optimal-variable'));

    document.getElementById('generate-combinations-btn').addEventListener('click', generateCombinations);
    document.getElementById('calculate-string-id-btn').addEventListener('click', calculateStringID);
    document.getElementById('decode-id-btn').addEventListener('click', decodeID);
    document.getElementById('find-optimal-variable-btn').addEventListener('click', findOptimalVariable);

    function generateCombinations() {
        try {
            const n = BigInt(document.getElementById('combination-size').value);
            const outputFile = document.getElementById('output-file-generate').value;
            if (isNaN(Number(n)) || n <= 0n) {
                throw new Error("Invalid combination size. Please enter a positive integer.");
            }

            let combinations = '';
            const k = BigInt(uniqueCharset.length);
            const nbrComb = k ** n;
            for (let i = 0n; i < nbrComb; i++) {
                let id = i;
                let combination = '';
                for (let j = 0n; j < n; j++) {
                    combination = uniqueCharset[Number(id % k)] + combination;
                    id = id / k;
                }
                combinations += combination + '\n';
            }
            alert("Combinations generated and saved to " + outputFile);
            console.log(combinations);
            downloadFile(outputFile, combinations);
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    }

    function calculateStringID() {
        try {
            const inputString = document.getElementById('custom-string').value;
            if (inputString.trim() === '') {
                throw new Error("Input string cannot be empty.");
            }

            let id = 0n;
            for (const char of inputString) {
                const charIndex = uniqueCharset.indexOf(char);
                if (charIndex === -1) {
                    throw new Error(`Character "${char}" is not in the charset.`);
                }
                id = id * BigInt(uniqueCharset.length) + BigInt(charIndex);
            }
            const result = id.toString() + "\t\n\n" + inputString;
            document.getElementById('string-id-result').innerText = "The ID for the string is: " + id.toString();

            const lengthOfString = inputString.length;
            const autoDownload = confirm("Do you want to automatically download the ID?");
            if (autoDownload) {
                const outputFile = `${lengthOfString}.txt`;
                downloadFile(outputFile, result);
            }
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    }

    function decodeID() {
        try {
            let id = BigInt(document.getElementById('string-id').value);
            if (id < 0n) {
                throw new Error("ID cannot be negative.");
            }

            const decodedString = [];
            while (id > 0n) {
                decodedString.push(uniqueCharset[Number(id % BigInt(uniqueCharset.length))]);
                id = id / BigInt(uniqueCharset.length);
            }

            if (decodedString.length === 0) {
                throw new Error("Decoded string is empty.");
            }

            document.getElementById('decoded-string-result').innerText = "The decoded string is: " + decodedString.reverse().join('');
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    }

    function optimalVariableGenerator(userNumber, charsetLength, extendedCharsetLength) {
        let k = 1n;
        return {
            next: function() {
                while (true) {
                    const x = k * userNumber;
                    if (x % extendedCharsetLength < charsetLength) {
                        k += 1n;
                        return { value: x, done: false };
                    }
                    k += 1n;
                }
            }
        };
    }

    function findOptimalVariable() {
        try {
            const userNumber = BigInt(document.getElementById('user-number').value);
            const outputFile = document.getElementById('output-file-optimal').value;
            const charsetLength = BigInt(uniqueCharset.length);
            const extendedCharsetLength = BigInt(uniqueCharset.length);
            const generator = optimalVariableGenerator(userNumber, charsetLength, extendedCharsetLength);
            const autoDownload = confirm("Do you want to automatically download the generated file?");

            const results = [];
            for (let i = 0; i < 100; i++) {
                const optVar = generator.next().value;
                const decodedString = decodeIDFromNumber(optVar, uniqueCharset);
                results.push(optVar + '\t' + decodedString);
            }

            const resultString = results.join('\n');

            if (autoDownload) {
                downloadFile(outputFile, resultString);
            } else {
                alert("Optimal variables and their corresponding strings saved to " + outputFile);
                console.log(resultString);
            }
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    }

    function decodeIDFromNumber(id, charset) {
        const decodedString = [];
        while (id > 0n) {
            decodedString.push(charset[Number(id % BigInt(charset.length))]);
            id = id / BigInt(charset.length);
        }
        return decodedString.reverse().join('');
    }

    function downloadFile(filename, content) {
        const blob = new Blob([content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
});