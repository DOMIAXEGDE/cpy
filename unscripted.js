document.addEventListener('DOMContentLoaded', () => {
    const prefixForm = document.getElementById('prefixForm');
    const inputCombination = document.getElementById('inputCombination');
    const feedback = document.getElementById('feedback');
    const combinationList = document.getElementById('combinationList');
    const trieVisualization = document.getElementById('trieVisualization');
    const downloadTrieButton = document.getElementById('downloadTrieButton');

    let combinations = [];  // Store combinations locally
    let trie = {};  // Trie object

    // Function to add multiple combinations from textarea
    function addCombinations(combinationsText) {
        const combinationArray = combinationsText.split(/\n/).map(item => item.trim()).filter(Boolean);  // Split by newline and remove empty lines
        let allAdded = true;
        combinationArray.forEach(combination => {
            if (!isPrefixFree(combination)) {
                feedback.innerText = `Combination "${combination}" is not prefix-free!`;
                feedback.style.color = 'red';
                allAdded = false;
                return;
            }
        });

        if (allAdded) {
            combinationArray.forEach(combination => {
                insertIntoTrie(combination);
                combinations.push(combination);
            });
            feedback.innerText = 'All combinations added successfully!';
            feedback.style.color = 'green';
            updateCombinationList();
            updateTrieVisualization();
        }
    }

    // Handle form submission
    prefixForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const combinationsText = inputCombination.value.trim();
        if (combinationsText) {
            addCombinations(combinationsText);
            inputCombination.value = '';
        }
    });

    // Function to check if a combination is prefix-free
    function isPrefixFree(word) {
        let currentNode = trie;
        for (let char of word) {
            if (currentNode[char]) {
                currentNode = currentNode[char];
                if (currentNode['isEndOfWord']) {
                    return false;
                }
            } else {
                break;
            }
        }
        return true;
    }

    // Insert combination into Trie
    function insertIntoTrie(word) {
        let currentNode = trie;
        for (let char of word) {
            if (!currentNode[char]) {
                currentNode[char] = {};
            }
            currentNode = currentNode[char];
        }
        currentNode['isEndOfWord'] = true;
    }

    // Update combination list display
    function updateCombinationList() {
        combinationList.innerHTML = '';
        combinations.forEach(combination => {
            const listItem = document.createElement('li');
            listItem.textContent = combination;
            combinationList.appendChild(listItem);
        });
    }

    // Visualize the Trie using simple squares
    function updateTrieVisualization() {
        trieVisualization.innerHTML = '';
        visualizeNode(trie, '');
    }

    // Recursive function to visualize each node
    function visualizeNode(node, prefix) {
        for (let key in node) {
            if (key !== 'isEndOfWord') {
                const gridItem = document.createElement('div');
                gridItem.className = 'grid-item';
                gridItem.innerText = prefix + key;
                gridItem.onclick = () => alert(`Node: ${prefix + key}`);  // Show pop-up with value on click
                trieVisualization.appendChild(gridItem);
                visualizeNode(node[key], prefix + key);
            }
        }
    }

    // Download Trie Data as JSON
    downloadTrieButton.addEventListener('click', () => {
        const trieData = JSON.stringify(trie, null, 2);
        const blob = new Blob([trieData], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'trie_data.json';
        a.click();
        URL.revokeObjectURL(url);
    });

    // Initial setup
    updateCombinationList();
    updateTrieVisualization();
});
