/**
 * Operator System - Integrated Computer Science Principles
 * 
 * This JavaScript file implements various computer science principles:
 * - Data Structures (Arrays, Objects, Sets, Trees)
 * - Algorithms (Recursion, Iteration, Search, Binary Operations)
 * - System Operations (File System, Memory Management, Process Management)
 * - CRUD Database Operations
 * - Advanced Concepts (Serialization, Compression, Encoding, Transactions)
 */

// Immediately Invoked Function Expression (IIFE) to avoid global scope pollution
(function() {
    'use strict';

    // ============ UTILITY FUNCTIONS ============

    /**
     * Utility function to show an error modal
     */
    function showError(message) {
        const modal = document.getElementById('error-modal');
        const messageElement = document.getElementById('error-message');
        messageElement.textContent = message;
        modal.style.display = 'block';
    }

    /**
     * Utility function to show a result in the modal
     */
    function showResultModal(content) {
        const modal = document.getElementById('result-modal');
        const resultElement = document.getElementById('modal-result');
        resultElement.innerHTML = '';
        
        if (typeof content === 'string') {
            resultElement.textContent = content;
        } else {
            resultElement.appendChild(content);
        }
        
        modal.style.display = 'block';
    }

    /**
     * Creates a status message element
     */
    function createStatusMessage(message, type) {
        const statusElement = document.createElement('div');
        statusElement.className = `status-message status-${type}`;
        statusElement.textContent = message;
        return statusElement;
    }

    /**
     * Global error handler with try-catch pattern
     */
    function safeExecute(func, errorCallback) {
        try {
            return func();
        } catch (error) {
            console.error('Operation error:', error);
            if (errorCallback) {
                errorCallback(error);
            } else {
                showError(error.message || 'An unexpected error occurred');
            }
            return null;
        }
    }

    // ============ SECTION NAVIGATION ============

    /**
     * Set up section navigation
     */
    function setupNavigation() {
        // Get all section buttons
        const sectionButtons = document.querySelectorAll('#main-nav button');
        
        // Add click event to each button
        sectionButtons.forEach(button => {
            button.addEventListener('click', () => {
                const sectionId = button.getAttribute('data-section');
                showSection(sectionId);
            });
        });
        
        // Show the first section by default
        if (sectionButtons.length > 0) {
            const firstSectionId = sectionButtons[0].getAttribute('data-section');
            showSection(firstSectionId);
        }
    }

    /**
     * Show a specific section and hide all others
     */
    function showSection(sectionId) {
        // Hide all sections
        const allSections = document.querySelectorAll('.operation-section');
        allSections.forEach(section => {
            section.classList.remove('active');
        });
        
        // Show the selected section
        const selectedSection = document.getElementById(sectionId);
        if (selectedSection) {
            selectedSection.classList.add('active');
            selectedSection.classList.add('fade-in');
            setTimeout(() => {
                selectedSection.classList.remove('fade-in');
            }, 500);
        }
    }

    // ============ 1. DATA STRUCTURES ============

    // ======== 1.1 Array Operations ========
    function setupArrayOperations() {
        const arrayInput = document.getElementById('array-input');
        const createArrayBtn = document.getElementById('create-array');
        const sortArrayBtn = document.getElementById('sort-array');
        const filterArrayBtn = document.getElementById('filter-array');
        const mapArrayBtn = document.getElementById('map-array');
        const reduceArrayBtn = document.getElementById('reduce-array');
        const resultContainer = document.getElementById('array-result');
        
        // Current array state
        let currentArray = [];
        
        // Create array from input
        createArrayBtn.addEventListener('click', () => {
            safeExecute(() => {
                const input = arrayInput.value;
                currentArray = input.split(',').map(item => {
                    const trimmed = item.trim();
                    // Try to convert to number if possible
                    const num = Number(trimmed);
                    return isNaN(num) ? trimmed : num;
                });
                
                displayArray(currentArray);
                return `Created array with ${currentArray.length} elements`;
            }, error => {
                resultContainer.textContent = `Error creating array: ${error.message}`;
            });
        });
        
        // Sort the array
        sortArrayBtn.addEventListener('click', () => {
            safeExecute(() => {
                if (currentArray.length === 0) {
                    throw new Error('Array is empty. Create an array first.');
                }
                
                // Check if array has all numbers or all strings for proper sorting
                const allNumbers = currentArray.every(item => typeof item === 'number');
                const allStrings = currentArray.every(item => typeof item === 'string');
                
                if (allNumbers) {
                    currentArray.sort((a, b) => a - b);
                } else if (allStrings) {
                    currentArray.sort();
                } else {
                    // Mixed type sorting - convert all to strings
                    currentArray.sort((a, b) => String(a).localeCompare(String(b)));
                }
                
                displayArray(currentArray);
                return 'Array sorted successfully';
            }, error => {
                resultContainer.textContent = `Error sorting array: ${error.message}`;
            });
        });
        
        // Filter array elements > 5
        filterArrayBtn.addEventListener('click', () => {
            safeExecute(() => {
                if (currentArray.length === 0) {
                    throw new Error('Array is empty. Create an array first.');
                }
                
                const filtered = currentArray.filter(item => {
                    // Only filter numerical values
                    return typeof item === 'number' && item > 5;
                });
                
                displayArray(filtered);
                return `Filtered array to ${filtered.length} elements > 5`;
            }, error => {
                resultContainer.textContent = `Error filtering array: ${error.message}`;
            });
        });
        
        // Map array (multiply by 2)
        mapArrayBtn.addEventListener('click', () => {
            safeExecute(() => {
                if (currentArray.length === 0) {
                    throw new Error('Array is empty. Create an array first.');
                }
                
                const mapped = currentArray.map(item => {
                    // Only multiply numbers, leave strings as is
                    return typeof item === 'number' ? item * 2 : item;
                });
                
                displayArray(mapped);
                return 'Mapped array (numbers multiplied by 2)';
            }, error => {
                resultContainer.textContent = `Error mapping array: ${error.message}`;
            });
        });
        
        // Reduce array (sum)
        reduceArrayBtn.addEventListener('click', () => {
            safeExecute(() => {
                if (currentArray.length === 0) {
                    throw new Error('Array is empty. Create an array first.');
                }
                
                // Extract numbers from the array
                const numbers = currentArray.filter(item => typeof item === 'number');
                
                if (numbers.length === 0) {
                    throw new Error('No numerical values found in the array');
                }
                
                const sum = numbers.reduce((acc, curr) => acc + curr, 0);
                
                resultContainer.innerHTML = '';
                const resultElement = document.createElement('div');
                resultElement.textContent = `Sum of numerical values: ${sum}`;
                resultContainer.appendChild(resultElement);
                
                return `Reduced array to sum: ${sum}`;
            }, error => {
                resultContainer.textContent = `Error reducing array: ${error.message}`;
            });
        });
        
        // Helper function to display the array
        function displayArray(array) {
            resultContainer.innerHTML = '';
            
            const arrayElement = document.createElement('div');
            arrayElement.className = 'array-display';
            
            array.forEach((item, index) => {
                const itemElement = document.createElement('div');
                itemElement.className = 'array-item';
                itemElement.innerHTML = `<span class="array-index">[${index}]</span>: <span class="array-value">${item}</span>`;
                arrayElement.appendChild(itemElement);
            });
            
            resultContainer.appendChild(arrayElement);
        }
    }
    
    // ======== 1.2 Object Operations ========
    function setupObjectOperations() {
        const objectKey = document.getElementById('object-key');
        const objectValue = document.getElementById('object-value');
        const addPropertyBtn = document.getElementById('add-property');
        const removePropertyBtn = document.getElementById('remove-property');
        const clearObjectBtn = document.getElementById('clear-object');
        const resultContainer = document.getElementById('object-result');
        
        // Current object state
        let currentObject = {};
        
        // Add a property to the object
        addPropertyBtn.addEventListener('click', () => {
            safeExecute(() => {
                const key = objectKey.value.trim();
                const value = objectValue.value.trim();
                
                if (!key) {
                    throw new Error('Property key cannot be empty');
                }
                
                // Try to parse the value if it looks like a number or boolean
                let parsedValue = value;
                
                if (value.toLowerCase() === 'true') {
                    parsedValue = true;
                } else if (value.toLowerCase() === 'false') {
                    parsedValue = false;
                } else if (!isNaN(Number(value))) {
                    parsedValue = Number(value);
                }
                
                // Add or update the property
                currentObject[key] = parsedValue;
                
                // Clear inputs
                objectKey.value = '';
                objectValue.value = '';
                
                // Display updated object
                displayObject(currentObject);
                return `Property '${key}' added to object`;
            }, error => {
                resultContainer.textContent = `Error adding property: ${error.message}`;
            });
        });
        
        // Remove a property from the object
        removePropertyBtn.addEventListener('click', () => {
            safeExecute(() => {
                const key = objectKey.value.trim();
                
                if (!key) {
                    throw new Error('Property key cannot be empty');
                }
                
                if (!(key in currentObject)) {
                    throw new Error(`Property '${key}' does not exist in the object`);
                }
                
                // Remove the property
                delete currentObject[key];
                
                // Clear input
                objectKey.value = '';
                
                // Display updated object
                displayObject(currentObject);
                return `Property '${key}' removed from object`;
            }, error => {
                resultContainer.textContent = `Error removing property: ${error.message}`;
            });
        });
        
        // Clear the object
        clearObjectBtn.addEventListener('click', () => {
            currentObject = {};
            displayObject(currentObject);
        });
        
        // Helper function to display the object
        function displayObject(obj) {
            resultContainer.innerHTML = '';
            
            if (Object.keys(obj).length === 0) {
                resultContainer.textContent = 'Empty object: {}';
                return;
            }
            
            const objectElement = document.createElement('div');
            objectElement.className = 'object-display';
            
            // Create JSON representation with syntax highlighting
            const jsonPre = document.createElement('pre');
            jsonPre.className = 'json-display';
            
            // Format JSON with indentation
            const formattedJson = JSON.stringify(obj, null, 2);
            jsonPre.textContent = formattedJson;
            
            objectElement.appendChild(jsonPre);
            resultContainer.appendChild(objectElement);
        }
        
        // Initialize with empty object
        displayObject(currentObject);
    }
    
    // ======== 1.3 Set Operations ========
    function setupSetOperations() {
        const setAInput = document.getElementById('set-a-input');
        const setBInput = document.getElementById('set-b-input');
        const unionBtn = document.getElementById('set-union');
        const intersectionBtn = document.getElementById('set-intersection');
        const differenceBtn = document.getElementById('set-difference');
        const resultContainer = document.getElementById('set-result');
        
        // Helper function to parse input into a Set
        function parseSetInput(input) {
            const values = input.split(',').map(item => item.trim());
            return new Set(values);
        }
        
        // Helper function to display a Set
        function displaySet(set, label) {
            const setElement = document.createElement('div');
            setElement.className = 'set-display';
            
            const setLabel = document.createElement('div');
            setLabel.className = 'set-label';
            setLabel.textContent = label;
            
            const setContent = document.createElement('div');
            setContent.className = 'set-content';
            setContent.textContent = Array.from(set).join(', ');
            
            setElement.appendChild(setLabel);
            setElement.appendChild(setContent);
            
            return setElement;
        }
        
        // Union operation
        unionBtn.addEventListener('click', () => {
            safeExecute(() => {
                const setA = parseSetInput(setAInput.value);
                const setB = parseSetInput(setBInput.value);
                
                // Perform union operation
                const union = new Set([...setA, ...setB]);
                
                // Display the result
                resultContainer.innerHTML = '';
                resultContainer.appendChild(displaySet(setA, 'Set A:'));
                resultContainer.appendChild(displaySet(setB, 'Set B:'));
                resultContainer.appendChild(displaySet(union, 'Union (A ∪ B):'));
                
                return `Union operation complete: ${union.size} elements`;
            }, error => {
                resultContainer.textContent = `Error performing union: ${error.message}`;
            });
        });
        
        // Intersection operation
        intersectionBtn.addEventListener('click', () => {
            safeExecute(() => {
                const setA = parseSetInput(setAInput.value);
                const setB = parseSetInput(setBInput.value);
                
                // Perform intersection operation
                const intersection = new Set(
                    [...setA].filter(item => setB.has(item))
                );
                
                // Display the result
                resultContainer.innerHTML = '';
                resultContainer.appendChild(displaySet(setA, 'Set A:'));
                resultContainer.appendChild(displaySet(setB, 'Set B:'));
                resultContainer.appendChild(displaySet(intersection, 'Intersection (A ∩ B):'));
                
                return `Intersection operation complete: ${intersection.size} elements`;
            }, error => {
                resultContainer.textContent = `Error performing intersection: ${error.message}`;
            });
        });
        
        // Difference operation
        differenceBtn.addEventListener('click', () => {
            safeExecute(() => {
                const setA = parseSetInput(setAInput.value);
                const setB = parseSetInput(setBInput.value);
                
                // Perform difference operation (A - B)
                const difference = new Set(
                    [...setA].filter(item => !setB.has(item))
                );
                
                // Display the result
                resultContainer.innerHTML = '';
                resultContainer.appendChild(displaySet(setA, 'Set A:'));
                resultContainer.appendChild(displaySet(setB, 'Set B:'));
                resultContainer.appendChild(displaySet(difference, 'Difference (A - B):'));
                
                return `Difference operation complete: ${difference.size} elements`;
            }, error => {
                resultContainer.textContent = `Error performing difference: ${error.message}`;
            });
        });
    }
    
    // ======== 1.4 Tree (Quadtree) Operations ========
    function setupTreeOperations() {
        const maxDepthInput = document.getElementById('max-depth');
        const quadtreeSizeInput = document.getElementById('quadtree-size');
        const createQuadtreeBtn = document.getElementById('create-quadtree');
        const resetQuadtreeBtn = document.getElementById('reset-quadtree');
        const exportQuadtreeBtn = document.getElementById('export-quadtree');
        const quadtreeContainer = document.getElementById('quadtree-container');
        
        // Quadtree state
        let quadtreeRoot = null;
        let maxDepth = 3;
        let quadtreeSize = 400;
        
        // QuadtreeNode class
        class QuadtreeNode {
            constructor(x, y, size, depth) {
                this.x = x;
                this.y = y;
                this.size = size;
                this.depth = depth;
                this.children = [];
                this.data = {};
                this.element = this.createElement();
                this.updateVisualState();
            }
            
            createElement() {
                const cell = document.createElement('div');
                cell.className = 'quadtree-cell';
                
                cell.style.left = `${this.x}px`;
                cell.style.top = `${this.y}px`;
                cell.style.width = `${this.size}px`;
                cell.style.height = `${this.size}px`;
                
                const content = document.createElement('div');
                content.className = 'cell-content';
                content.textContent = `d: ${this.depth}`;
                cell.appendChild(content);
                
                cell.addEventListener('click', () => {
                    this.handleClick();
                });
                
                quadtreeContainer.appendChild(cell);
                return cell;
            }
            
            updateVisualState() {
                if (this.depth < maxDepth) {
                    this.element.classList.add('can-subdivide');
                    this.element.title = 'Click to subdivide';
                } else {
                    this.element.classList.remove('can-subdivide');
                    this.element.title = 'Max depth reached';
                }
                
                // Update color based on depth
                const hue = (this.depth * 30) % 360;
                this.element.style.backgroundColor = `hsl(${hue}, 70%, 90%)`;
                this.element.style.borderColor = `hsl(${hue}, 70%, 60%)`;
            }
            
            handleClick() {
                if (this.children.length === 0 && this.depth < maxDepth) {
                    this.subdivide();
                }
            }
            
            subdivide() {
                if (this.children.length > 0 || this.depth >= maxDepth) return false;
                
                const childSize = this.size / 2;
                
                this.children.push(
                    new QuadtreeNode(this.x, this.y, childSize, this.depth + 1),
                    new QuadtreeNode(this.x + childSize, this.y, childSize, this.depth + 1),
                    new QuadtreeNode(this.x, this.y + childSize, childSize, this.depth + 1),
                    new QuadtreeNode(this.x + childSize, this.y + childSize, childSize, this.depth + 1)
                );
                
                this.element.style.display = 'none';
                return true;
            }
        }
        
        // Create the initial quadtree
        function initQuadtree() {
            // Clear the container
            quadtreeContainer.innerHTML = '';
            
            // Get current settings
            maxDepth = parseInt(maxDepthInput.value) || 3;
            quadtreeSize = parseInt(quadtreeSizeInput.value) || 400;
            
            // Set container size
            quadtreeContainer.style.width = `${quadtreeSize}px`;
            quadtreeContainer.style.height = `${quadtreeSize}px`;
            
            // Create root node
            quadtreeRoot = new QuadtreeNode(0, 0, quadtreeSize, 0);
        }
        
        // Export the quadtree as PNG
        function exportQuadtreeAsPNG() {
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            
            canvas.width = quadtreeSize;
            canvas.height = quadtreeSize;
            
            // Fill background
            context.fillStyle = 'white';
            context.fillRect(0, 0, canvas.width, canvas.height);
            
            // Recursive function to draw nodes
            function drawNode(node) {
                if (!node) return;
                
                // Only draw visible nodes
                if (node.element.style.display !== 'none') {
                    // Get computed styles
                    const styles = window.getComputedStyle(node.element);
                    
                    // Draw cell background
                    context.fillStyle = styles.backgroundColor;
                    context.fillRect(node.x, node.y, node.size, node.size);
                    
                    // Draw cell border
                    context.strokeStyle = styles.borderColor;
                    context.lineWidth = 1;
                    context.strokeRect(node.x, node.y, node.size, node.size);
                    
                    // Draw text
                    context.fillStyle = '#333';
                    context.font = '12px sans-serif';
                    context.textAlign = 'center';
                    context.textBaseline = 'middle';
                    context.fillText(`d: ${node.depth}`, 
                                    node.x + node.size/2, 
                                    node.y + node.size/2);
                }
                
                // Draw children
                for (const child of node.children) {
                    drawNode(child);
                }
            }
            
            // Draw the quadtree
            drawNode(quadtreeRoot);
            
            // Create download link
            const link = document.createElement('a');
            link.download = 'quadtree.png';
            link.href = canvas.toDataURL('image/png');
            link.click();
        }
        
        // Event listeners
        createQuadtreeBtn.addEventListener('click', initQuadtree);
        resetQuadtreeBtn.addEventListener('click', initQuadtree);
        exportQuadtreeBtn.addEventListener('click', exportQuadtreeAsPNG);
        
        // Initialize
        initQuadtree();
    }

    // ============ 2. ALGORITHMS ============
    
    // ======== 2.1 Recursion Operations ========
    function setupRecursionOperations() {
        const recursionInput = document.getElementById('recursion-n');
        const factorialBtn = document.getElementById('calc-factorial');
        const fibonacciBtn = document.getElementById('calc-fibonacci');
        const generateTreeBtn = document.getElementById('generate-tree');
        const resultContainer = document.getElementById('recursion-result');
        
        // Recursive factorial function
        function factorial(n) {
            // Base case
            if (n <= 1) return 1;
            
            // Recursive case
            return n * factorial(n - 1);
        }
        
        // Recursive Fibonacci function
        function fibonacci(n) {
            // Base cases
            if (n <= 0) return 0;
            if (n === 1) return 1;
            
            // Recursive case
            return fibonacci(n - 1) + fibonacci(n - 2);
        }
        
        // Generate recursive tree visualization
        function generateTree(n) {
            const container = document.createElement('div');
            container.className = 'tree-container';
            
            function createTreeNode(value, depth) {
                const node = document.createElement('div');
                node.className = 'tree-node';
                
                const nodeContent = document.createElement('div');
                nodeContent.className = 'tree-node-content';
                nodeContent.textContent = value;
                
                node.appendChild(nodeContent);
                
                // Add children if depth > 0
                if (depth > 0) {
                    const children = document.createElement('div');
                    children.className = 'tree-children';
                    
                    // Left child is depth-1
                    children.appendChild(createTreeNode(depth-1, depth-1));
                    
                    // Right child is depth/2 (integer division)
                    if (depth > 1) {
                        children.appendChild(createTreeNode(Math.floor(depth/2), Math.floor(depth/2)));
                    }
                    
                    node.appendChild(children);
                }
                
                return node;
            }
            
            container.appendChild(createTreeNode(n, n));
            return container;
        }
        
        // Calculate factorial button
        factorialBtn.addEventListener('click', () => {
            safeExecute(() => {
                const n = parseInt(recursionInput.value);
                
                if (isNaN(n) || n < 0) {
                    throw new Error('Please enter a non-negative integer');
                }
                
                if (n > 20) {
                    throw new Error('Value too large (max 20)');
                }
                
                const result = factorial(n);
                
                resultContainer.innerHTML = '';
                const resultElement = document.createElement('div');
                resultElement.innerHTML = `<strong>Factorial of ${n}:</strong> ${result}`;
                
                // Add explanation
                const explanation = document.createElement('div');
                explanation.className = 'recursion-explanation';
                explanation.innerHTML = `<p>Factorial is calculated recursively as:</p>
                                        <p>factorial(${n}) = ${n} * factorial(${n-1})</p>
                                        <p>factorial(1) = 1 (base case)</p>`;
                
                resultContainer.appendChild(resultElement);
                resultContainer.appendChild(explanation);
                
                return `Calculated factorial of ${n}: ${result}`;
            }, error => {
                resultContainer.textContent = `Error calculating factorial: ${error.message}`;
            });
        });
        
        // Calculate Fibonacci button
        fibonacciBtn.addEventListener('click', () => {
            safeExecute(() => {
                const n = parseInt(recursionInput.value);
                
                if (isNaN(n) || n < 0) {
                    throw new Error('Please enter a non-negative integer');
                }
                
                if (n > 40) {
                    throw new Error('Value too large (max 40). Recursive Fibonacci is inefficient for large values.');
                }
                
                const result = fibonacci(n);
                
                resultContainer.innerHTML = '';
                const resultElement = document.createElement('div');
                resultElement.innerHTML = `<strong>Fibonacci(${n}):</strong> ${result}`;
                
                // Add explanation
                const explanation = document.createElement('div');
                explanation.className = 'recursion-explanation';
                explanation.innerHTML = `<p>Fibonacci is calculated recursively as:</p>
                                        <p>fibonacci(${n}) = fibonacci(${n-1}) + fibonacci(${n-2})</p>
                                        <p>fibonacci(0) = 0, fibonacci(1) = 1 (base cases)</p>`;
                
                resultContainer.appendChild(resultElement);
                resultContainer.appendChild(explanation);
                
                return `Calculated Fibonacci(${n}): ${result}`;
            }, error => {
                resultContainer.textContent = `Error calculating Fibonacci: ${error.message}`;
            });
        });
        
        // Generate Tree button
        generateTreeBtn.addEventListener('click', () => {
            safeExecute(() => {
                const n = parseInt(recursionInput.value);
                
                if (isNaN(n) || n < 0) {
                    throw new Error('Please enter a non-negative integer');
                }
                
                if (n > 5) {
                    throw new Error('Value too large (max 5). Larger values create very large trees.');
                }
                
                const treeVisualization = generateTree(n);
                
                resultContainer.innerHTML = '';
                resultContainer.appendChild(treeVisualization);
                
                return `Generated recursive tree with depth ${n}`;
            }, error => {
                resultContainer.textContent = `Error generating tree: ${error.message}`;
            });
        });
    }
    
    // ======== 2.2 Iteration Operations ========
    function setupIterationOperations() {
        const iterationInput = document.getElementById('iteration-n');
        const charsetInput = document.getElementById('charset-input');
        const generateBtn = document.getElementById('generate-combinations');
        const stopBtn = document.getElementById('stop-generation');
        const resultContainer = document.getElementById('iteration-result');
        const progressBar = document.getElementById('iteration-progress');
        const progressFill = progressBar.querySelector('.progress-fill');
        
        // Flag to control generation
        let isGenerating = false;
        
        // Generate all possible combinations of length n from charset
        function generateCombinations(charset, n) {
            const combinations = [];
            const charsetArray = Array.from(charset);
            
            // Total number of combinations
            const total = Math.pow(charsetArray.length, n);
            
            // Iterator function using batch processing for UI responsiveness
            async function* combinationIterator() {
                const batchSize = 1000;
                let count = 0;
                
                // For each possible combination
                for (let i = 0; i < total && isGenerating; i++) {
                    let combination = '';
                    let index = i;
                    
                    // Generate combination by extracting characters
                    for (let j = 0; j < n; j++) {
                        combination = charsetArray[index % charsetArray.length] + combination;
                        index = Math.floor(index / charsetArray.length);
                    }
                    
                    combinations.push(combination);
                    count++;
                    
                    // Yield after each batch to allow UI updates
                    if (count % batchSize === 0 || i === total - 1) {
                        yield {
                            progress: (i + 1) / total * 100,
                            combinations: combinations.slice() // Copy current state
                        };
                        await new Promise(resolve => setTimeout(resolve, 0));
                    }
                }
            }
            
            return {
                iterator: combinationIterator(),
                total
            };
        }
        
        // Generate button click handler
        generateBtn.addEventListener('click', async () => {
            safeExecute(async () => {
                const n = parseInt(iterationInput.value);
                const charset = charsetInput.value;
                
                if (isNaN(n) || n < 1) {
                    throw new Error('Please enter a positive integer for n');
                }
                
                if (charset.length === 0) {
                    throw new Error('Charset cannot be empty');
                }
                
                if (n > 5 && charset.length > 5) {
                    throw new Error('Combination too large. Try a smaller n or charset.');
                }
                
                // Calculate total combinations
                const totalCombinations = Math.pow(charset.length, n);
                
                // Update UI
                resultContainer.innerHTML = `<p>Generating ${totalCombinations} combinations...</p>`;
                progressFill.style.width = '0%';
                isGenerating = true;
                generateBtn.disabled = true;
                stopBtn.disabled = false;
                
                // Generate combinations
                const generator = generateCombinations(charset, n);
                
                // Process each batch
                let result;
                try {
                    for await (result of generator.iterator) {
                        if (!isGenerating) break;
                        
                        // Update progress bar
                        progressFill.style.width = `${result.progress}%`;
                        
                        // Display current state (limited to first 100 for performance)
                        const displayCombinations = result.combinations.slice(0, 100);
                        resultContainer.innerHTML = `<p>Generated ${result.combinations.length} of ${totalCombinations} combinations</p>
                                                    <div class="combinations-list">${displayCombinations.join(', ')}${result.combinations.length > 100 ? '...' : ''}</div>`;
                    }
                } catch (e) {
                    console.error('Generation error:', e);
                    throw e;
                }
                
                // Update UI after completion
                isGenerating = false;
                generateBtn.disabled = false;
                stopBtn.disabled = true;
                
                if (result && result.combinations) {
                    return `Generated ${result.combinations.length} combinations with n=${n} and charset="${charset}"`;
                } else {
                    return 'Generation stopped';
                }
            }, error => {
                isGenerating = false;
                generateBtn.disabled = false;
                stopBtn.disabled = true;
                resultContainer.innerHTML = `<p class="error">Error: ${error.message}</p>`;
            });
        });
        
        // Stop button click handler
        stopBtn.addEventListener('click', () => {
            isGenerating = false;
            generateBtn.disabled = false;
            stopBtn.disabled = true;
            resultContainer.innerHTML += '<p>Generation stopped by user</p>';
        });
    }
    
    // ======== 2.3 Search Operations ========
    function setupSearchOperations() {
        const searchData = document.getElementById('search-data');
        const searchQuery = document.getElementById('search-query');
        const linearSearchBtn = document.getElementById('linear-search');
        const binarySearchBtn = document.getElementById('binary-search');
        const fuzzySearchBtn = document.getElementById('fuzzy-search');
        const resultContainer = document.getElementById('search-result');
        
        // Parse the data input into an array
        function parseData() {
            return searchData.value.split(',').map(item => item.trim());
        }
        
        // Linear search implementation
        function linearSearch(arr, query) {
            const results = [];
            const startTime = performance.now();
            
            // Search for the query
            for (let i = 0; i < arr.length; i++) {
                // Record number of comparisons
                let comparisons = 1;
                if (arr[i] === query) {
                    results.push({
                        index: i,
                        value: arr[i],
                        comparisons
                    });
                }
            }
            
            const endTime = performance.now();
            
            return {
                found: results.length > 0,
                results,
                time: endTime - startTime
            };
        }
        
        // Binary search implementation (requires sorted array)
        function binarySearch(arr, query) {
            // Sort array if it contains all numbers or all strings
            const isNumber = arr.every(item => !isNaN(Number(item)));
            const sorted = [...arr];
            
            // Sort the array
            if (isNumber) {
                sorted.sort((a, b) => Number(a) - Number(b));
            } else {
                sorted.sort();
            }
            
            const startTime = performance.now();
            let comparisons = 0;
            
            // Binary search algorithm
            let left = 0;
            let right = sorted.length - 1;
            let foundIndex = -1;
            
            while (left <= right) {
                const mid = Math.floor((left + right) / 2);
                comparisons++;
                
                if (sorted[mid] === query) {
                    foundIndex = mid;
                    break;
                } else if (sorted[mid] < query) {
                    left = mid + 1;
                } else {
                    right = mid - 1;
                }
            }
            
            const endTime = performance.now();
            
            // Map back to original array if found
            let results = [];
            if (foundIndex !== -1) {
                const originalIndex = arr.indexOf(sorted[foundIndex]);
                results.push({
                    index: originalIndex,
                    value: arr[originalIndex],
                    comparisons
                });
            }
            
            return {
                found: foundIndex !== -1,
                results,
                time: endTime - startTime,
                sortedArray: sorted
            };
        }
        
        // Fuzzy search implementation
        function fuzzySearch(arr, query) {
            const results = [];
            const startTime = performance.now();
            
            // Search for partial matches
            for (let i = 0; i < arr.length; i++) {
                let comparisons = 1;
                const strValue = String(arr[i]);
                const strQuery = String(query);
                
                // Check if item contains the query
                if (strValue.includes(strQuery)) {
                    results.push({
                        index: i,
                        value: arr[i],
                        comparisons,
                        matchType: 'contains'
                    });
                } 
                // Check if item is "close" to query using Levenshtein distance
                else {
                    const distance = levenshteinDistance(strValue, strQuery);
                    if (distance <= 2) { // Consider matches with distance <= 2
                        results.push({
                            index: i,
                            value: arr[i],
                            comparisons: comparisons + 1,
                            matchType: 'similar',
                            distance
                        });
                    }
                }
            }
            
            const endTime = performance.now();
            
            return {
                found: results.length > 0,
                results,
                time: endTime - startTime
            };
        }
        
        // Levenshtein distance for fuzzy matching
        function levenshteinDistance(a, b) {
            const matrix = [];
            
            // Initialize the matrix
            for (let i = 0; i <= b.length; i++) {
                matrix[i] = [i];
            }
            
            for (let j = 0; j <= a.length; j++) {
                matrix[0][j] = j;
            }
            
            // Fill the matrix
            for (let i = 1; i <= b.length; i++) {
                for (let j = 1; j <= a.length; j++) {
                    if (b.charAt(i - 1) === a.charAt(j - 1)) {
                        matrix[i][j] = matrix[i - 1][j - 1];
                    } else {
                        matrix[i][j] = Math.min(
                            matrix[i - 1][j - 1] + 1, // substitution
                            matrix[i][j - 1] + 1,     // insertion
                            matrix[i - 1][j] + 1      // deletion
                        );
                    }
                }
            }
            
            return matrix[b.length][a.length];
        }
        
        // Display search results
        function displayResults(searchType, result) {
            resultContainer.innerHTML = '';
            
            const header = document.createElement('div');
            header.innerHTML = `<h3>${searchType} Search Results</h3>`;
            resultContainer.appendChild(header);
            
            const timeElement = document.createElement('div');
            timeElement.className = 'search-time';
            timeElement.textContent = `Search time: ${result.time.toFixed(4)} ms`;
            resultContainer.appendChild(timeElement);
            
            if (result.sortedArray) {
                const sortedElement = document.createElement('div');
                sortedElement.className = 'sorted-array';
                sortedElement.innerHTML = `<strong>Sorted Array:</strong> ${result.sortedArray.join(', ')}`;
                resultContainer.appendChild(sortedElement);
            }
            
            if (result.found) {
                const resultsElement = document.createElement('div');
                resultsElement.className = 'search-results';
                
                result.results.forEach(item => {
                    const resultItem = document.createElement('div');
                    resultItem.className = 'search-result-item';
                    
                    let details = `Found at index ${item.index}: ${item.value} (${item.comparisons} comparisons)`;
                    if (item.matchType) {
                        details += ` - ${item.matchType} match`;
                        if (item.distance !== undefined) {
                            details += ` (distance: ${item.distance})`;
                        }
                    }
                    
                    resultItem.textContent = details;
                    resultsElement.appendChild(resultItem);
                });
                
                resultContainer.appendChild(resultsElement);
            } else {
                const notFoundElement = document.createElement('div');
                notFoundElement.className = 'not-found';
                notFoundElement.textContent = 'Item not found in the array';
                resultContainer.appendChild(notFoundElement);
            }
        }
        
        // Linear search button click handler
        linearSearchBtn.addEventListener('click', () => {
            safeExecute(() => {
                const data = parseData();
                const query = searchQuery.value.trim();
                
                if (data.length === 0) {
                    throw new Error('Please enter comma-separated data');
                }
                
                if (query === '') {
                    throw new Error('Please enter a search query');
                }
                
                const result = linearSearch(data, query);
                displayResults('Linear', result);
                
                return `Linear search complete: ${result.found ? 'Found' : 'Not found'}`;
            }, error => {
                resultContainer.innerHTML = `<div class="error">${error.message}</div>`;
            });
        });
        
        // Binary search button click handler
        binarySearchBtn.addEventListener('click', () => {
            safeExecute(() => {
                const data = parseData();
                const query = searchQuery.value.trim();
                
                if (data.length === 0) {
                    throw new Error('Please enter comma-separated data');
                }
                
                if (query === '') {
                    throw new Error('Please enter a search query');
                }
                
                const result = binarySearch(data, query);
                displayResults('Binary', result);
                
                return `Binary search complete: ${result.found ? 'Found' : 'Not found'}`;
            }, error => {
                resultContainer.innerHTML = `<div class="error">${error.message}</div>`;
            });
        });
        
        // Fuzzy search button click handler
        fuzzySearchBtn.addEventListener('click', () => {
            safeExecute(() => {
                const data = parseData();
                const query = searchQuery.value.trim();
                
                if (data.length === 0) {
                    throw new Error('Please enter comma-separated data');
                }
                
                if (query === '') {
                    throw new Error('Please enter a search query');
                }
                
                const result = fuzzySearch(data, query);
                displayResults('Fuzzy', result);
                
                return `Fuzzy search complete: ${result.found ? 'Found' : 'Not found'}`;
            }, error => {
                resultContainer.innerHTML = `<div class="error">${error.message}</div>`;
            });
        });
    }
    
    // ======== 2.4 Binary Operations ========
    function setupBinaryOperations() {
        const binaryInputA = document.getElementById('binary-input-a');
        const binaryInputB = document.getElementById('binary-input-b');
        const andBtn = document.getElementById('binary-and');
        const orBtn = document.getElementById('binary-or');
        const xorBtn = document.getElementById('binary-xor');
        const notBtn = document.getElementById('binary-not');
        const shiftBtn = document.getElementById('binary-shift');
        const resultContainer = document.getElementById('binary-result');
        
        // Convert number to binary string with padding
        function toBinaryString(number, bits = 8) {
            return (number >>> 0).toString(2).padStart(bits, '0');
        }
        
        // Display binary representation
        function displayBinary(label, value) {
            const binaryString = toBinaryString(value);
            
            const container = document.createElement('div');
            container.className = 'binary-display';
            
            const labelElement = document.createElement('div');
            labelElement.className = 'binary-label';
            labelElement.textContent = label;
            container.appendChild(labelElement);
            
            const binaryRow = document.createElement('div');
            binaryRow.className = 'binary-row';
            
            // Create bit elements
            for (let i = 0; i < binaryString.length; i++) {
                const bit = document.createElement('div');
                bit.className = `bit ${binaryString[i] === '1' ? 'one' : 'zero'}`;
                bit.textContent = binaryString[i];
                binaryRow.appendChild(bit);
            }
            
            container.appendChild(binaryRow);
            
            const decimalValue = document.createElement('div');
            decimalValue.className = 'decimal-value';
            decimalValue.textContent = `Decimal: ${value}`;
            container.appendChild(decimalValue);
            
            return container;
        }
        
        // Display binary operation result
        function displayBinaryOperation(valueA, valueB, result, operationSymbol) {
            resultContainer.innerHTML = '';
            
            // Display inputs
            resultContainer.appendChild(displayBinary('Value A', valueA));
            if (valueB !== undefined) {
                resultContainer.appendChild(displayBinary('Value B', valueB));
            }
            
            // Display operation
            const operationElement = document.createElement('div');
            operationElement.className = 'binary-operation';
            operationElement.textContent = operationSymbol;
            resultContainer.appendChild(operationElement);
            
            // Display result
            resultContainer.appendChild(displayBinary('Result', result));
        }
        
        // AND operation
        andBtn.addEventListener('click', () => {
            safeExecute(() => {
                const valueA = parseInt(binaryInputA.value) || 0;
                const valueB = parseInt(binaryInputB.value) || 0;
                
                if (valueA < 0 || valueA > 255 || valueB < 0 || valueB > 255) {
                    throw new Error('Values must be between 0 and 255');
                }
                
                const result = valueA & valueB;
                displayBinaryOperation(valueA, valueB, result, 'AND');
                
                return `Binary AND: ${valueA} & ${valueB} = ${result}`;
            }, error => {
                resultContainer.innerHTML = `<div class="error">${error.message}</div>`;
            });
        });
        
        // OR operation
        orBtn.addEventListener('click', () => {
            safeExecute(() => {
                const valueA = parseInt(binaryInputA.value) || 0;
                const valueB = parseInt(binaryInputB.value) || 0;
                
                if (valueA < 0 || valueA > 255 || valueB < 0 || valueB > 255) {
                    throw new Error('Values must be between 0 and 255');
                }
                
                const result = valueA | valueB;
                displayBinaryOperation(valueA, valueB, result, 'OR');
                
                return `Binary OR: ${valueA} | ${valueB} = ${result}`;
            }, error => {
                resultContainer.innerHTML = `<div class="error">${error.message}</div>`;
            });
        });
        
        // XOR operation
        xorBtn.addEventListener('click', () => {
            safeExecute(() => {
                const valueA = parseInt(binaryInputA.value) || 0;
                const valueB = parseInt(binaryInputB.value) || 0;
                
                if (valueA < 0 || valueA > 255 || valueB < 0 || valueB > 255) {
                    throw new Error('Values must be between 0 and 255');
                }
                
                const result = valueA ^ valueB;
                displayBinaryOperation(valueA, valueB, result, 'XOR');
                
                return `Binary XOR: ${valueA} ^ ${valueB} = ${result}`;
            }, error => {
                resultContainer.innerHTML = `<div class="error">${error.message}</div>`;
            });
        });
        
        // NOT operation
        notBtn.addEventListener('click', () => {
            safeExecute(() => {
                const valueA = parseInt(binaryInputA.value) || 0;
                
                if (valueA < 0 || valueA > 255) {
                    throw new Error('Value must be between 0 and 255');
                }
                
                const result = ~valueA & 0xFF; // Mask to 8 bits
                displayBinaryOperation(valueA, undefined, result, 'NOT');
                
                return `Binary NOT: ~${valueA} = ${result}`;
            }, error => {
                resultContainer.innerHTML = `<div class="error">${error.message}</div>`;
            });
        });
        
        // Shift Left operation
        shiftBtn.addEventListener('click', () => {
            safeExecute(() => {
                const valueA = parseInt(binaryInputA.value) || 0;
                const shiftAmount = parseInt(binaryInputB.value) || 0;
                
                if (valueA < 0 || valueA > 255) {
                    throw new Error('Value must be between 0 and 255');
                }
                
                if (shiftAmount < 0 || shiftAmount > 7) {
                    throw new Error('Shift amount must be between 0 and 7');
                }
                
                const result = (valueA << shiftAmount) & 0xFF; // Mask to 8 bits
                displayBinaryOperation(valueA, shiftAmount, result, `SHIFT LEFT (${shiftAmount} bits)`);
                
                return `Binary Shift Left: ${valueA} << ${shiftAmount} = ${result}`;
            }, error => {
                resultContainer.innerHTML = `<div class="error">${error.message}</div>`;
            });
        });
    }

    // ============ 3. SYSTEM OPERATIONS ============
    
    // ======== 3.1 File System Operations ========
    function setupFileOperations() {
        const fileContent = document.getElementById('file-content');
        const fileName = document.getElementById('file-name');
        const saveFileBtn = document.getElementById('save-file');
        const loadFileBtn = document.getElementById('load-file');
        const fileUpload = document.getElementById('file-upload');
        const createDirBtn = document.getElementById('create-directory');
        const createZipBtn = document.getElementById('create-zip');
        const fileTree = document.getElementById('file-tree');
        
        // Virtual file system structure
        const virtualFS = {
            root: {
                type: 'directory',
                name: 'root',
                children: {}
            }
        };
        
        // Load file button click handler
        loadFileBtn.addEventListener('click', () => {
            fileUpload.click();
        });
        
        // File upload change handler
        fileUpload.addEventListener('change', (event) => {
            safeExecute(() => {
                const file = event.target.files[0];
                
                if (!file) return;
                
                const reader = new FileReader();
                
                reader.onload = (e) => {
                    const content = e.target.result;
                    fileContent.value = content;
                    fileName.value = file.name;
                    
                    // Add to virtual filesystem
                    addFileToVFS(file.name, content);
                    renderFileTree();
                };
                
                reader.onerror = () => {
                    throw new Error('Error reading file');
                };
                
                reader.readAsText(file);
            }, error => {
                showError(`File loading error: ${error.message}`);
            });
        });
        
        // Save file button click handler
        saveFileBtn.addEventListener('click', () => {
            safeExecute(() => {
                const content = fileContent.value;
                const name = fileName.value.trim();
                
                if (!name) {
                    throw new Error('File name cannot be empty');
                }
                
                // Save file to browser (download)
                const blob = new Blob([content], { type: 'text/plain' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = name;
                a.click();
                
                // Clean up
                setTimeout(() => URL.revokeObjectURL(url), 1000);
                
                // Add to virtual filesystem
                addFileToVFS(name, content);
                renderFileTree();
                
                return `File "${name}" saved successfully`;
            }, error => {
                showError(`File saving error: ${error.message}`);
            });
        });
        
        // Create directory button click handler
        createDirBtn.addEventListener('click', () => {
            safeExecute(() => {
                const dirName = prompt('Enter directory name:');
                
                if (!dirName) return;
                
                if (dirName.trim() === '') {
                    throw new Error('Directory name cannot be empty');
                }
                
                addDirectoryToVFS(dirName);
                renderFileTree();
                
                return `Directory "${dirName}" created`;
            }, error => {
                showError(`Directory creation error: ${error.message}`);
            });
        });
        
        // Create ZIP button click handler (using JSZip)
        createZipBtn.addEventListener('click', () => {
            safeExecute(async () => {
                const zip = new JSZip();
                
                // Add all files from virtual filesystem
                addFilesToZip(zip, virtualFS.root);
                
                // Generate ZIP blob
                const blob = await zip.generateAsync({ type: 'blob' });
                
                // Download ZIP file
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'files.zip';
                a.click();
                
                // Clean up
                setTimeout(() => URL.revokeObjectURL(url), 1000);
                
                return 'ZIP file created and downloaded';
            }, error => {
                showError(`ZIP creation error: ${error.message}`);
            });
        });
        
        // Helper function to add files to ZIP
        function addFilesToZip(zip, directory, path = '') {
            for (const name in directory.children) {
                const item = directory.children[name];
                const itemPath = path ? `${path}/${name}` : name;
                
                if (item.type === 'file') {
                    zip.file(itemPath, item.content);
                } else if (item.type === 'directory') {
                    const folder = zip.folder(itemPath);
                    addFilesToZip(zip, item, itemPath);
                }
            }
        }
        
        // Add file to virtual filesystem
        function addFileToVFS(filePath, content) {
            const parts = filePath.split('/');
            const fileName = parts.pop();
            let currentDir = virtualFS.root;
            
            // Create directories in path if needed
            for (const part of parts) {
                if (!part) continue;
                
                if (!currentDir.children[part]) {
                    currentDir.children[part] = {
                        type: 'directory',
                        name: part,
                        children: {}
                    };
                }
                
                currentDir = currentDir.children[part];
            }
            
            // Add file
            currentDir.children[fileName] = {
                type: 'file',
                name: fileName,
                content: content
            };
        }
        
        // Add directory to virtual filesystem
        function addDirectoryToVFS(dirPath) {
            const parts = dirPath.split('/');
            let currentDir = virtualFS.root;
            
            // Create directories in path
            for (const part of parts) {
                if (!part) continue;
                
                if (!currentDir.children[part]) {
                    currentDir.children[part] = {
                        type: 'directory',
                        name: part,
                        children: {}
                    };
                }
                
                currentDir = currentDir.children[part];
            }
        }
        
        // Render file tree
        function renderFileTree() {
            fileTree.innerHTML = '';
            
            function createTreeItem(item, parent) {
                const li = document.createElement('li');
                
                if (item.type === 'directory') {
                    const dirElement = document.createElement('div');
                    dirElement.className = 'directory-item';
                    dirElement.innerHTML = `<span class="file-icon">📁</span> ${item.name}`;
                    li.appendChild(dirElement);
                    
                    const childList = document.createElement('ul');
                    childList.className = 'directory-children';
                    
                    // Add children
                    const children = Object.values(item.children)
                        .sort((a, b) => {
                            // Sort directories first, then files
                            if (a.type !== b.type) {
                                return a.type === 'directory' ? -1 : 1;
                            }
                            return a.name.localeCompare(b.name);
                        });
                    
                    for (const child of children) {
                        createTreeItem(child, childList);
                    }
                    
                    li.appendChild(childList);
                    
                    // Toggle expand/collapse
                    dirElement.addEventListener('click', () => {
                        childList.style.display = childList.style.display === 'none' ? 'block' : 'none';
                    });
                } else {
                    li.className = 'file-item';
                    li.innerHTML = `<span class="file-icon">📄</span> <span class="file-name">${item.name}</span>`;
                    
                    // Click to load file
                    li.addEventListener('click', () => {
                        fileContent.value = item.content;
                        fileName.value = item.name;
                    });
                }
                
                parent.appendChild(li);
            }
            
            // Create the root node
            createTreeItem(virtualFS.root, fileTree);
        }
        
        // Initialize with empty file tree
        renderFileTree();
    }
    
    // ======== 3.2 Memory Operations ========
    function setupMemoryOperations() {
        const memoryFile = document.getElementById('memory-file');
        const memorySlot = document.getElementById('memory-slot');
        const memoryContent = document.getElementById('memory-content');
        const assignSlotBtn = document.getElementById('assign-slot');
        const readSlotBtn = document.getElementById('read-slot');
        const clearAllSlotsBtn = document.getElementById('clear-all-slots');
        const memoryDisplay = document.getElementById('memory-display');
        
        // Memory manager class
        class MemorySlotManager {
            constructor() {
                this.memorySlots = {};
            }
            
            assignSlot(fileNumber, slotNumber, value) {
                if (!fileNumber || !slotNumber || !value) {
                    return "Error: Invalid input parameters.";
                }
                
                if (this.valueExists(value)) {
                    return "Error: The value already exists in another memory slot.";
                }
                
                if (!this.memorySlots[fileNumber]) {
                    this.memorySlots[fileNumber] = {};
                }
                
                this.memorySlots[fileNumber][slotNumber] = value;
                return `Assigned value to slot ${slotNumber} in file ${fileNumber}.`;
            }
            
            readSlot(fileNumber, slotNumber) {
                if (this.memorySlots[fileNumber] && this.memorySlots[fileNumber][slotNumber] !== undefined) {
                    return this.memorySlots[fileNumber][slotNumber];
                }
                return `Slot ${slotNumber} not found in file ${fileNumber}.`;
            }
            
            valueExists(value) {
                const valueLower = value.toLowerCase();
                
                for (const file in this.memorySlots) {
                    for (const slot in this.memorySlots[file]) {
                        if (this.memorySlots[file][slot].toLowerCase() === valueLower) {
                            return true;
                        }
                    }
                }
                
                return false;
            }
            
            clearAll() {
                this.memorySlots = {};
                return 'All memory slots cleared';
            }
        }
        
        // Initialize memory slot manager
        const memoryManager = new MemorySlotManager();
        
        // Update memory display
        function updateMemoryDisplay() {
            memoryDisplay.innerHTML = '';
            
            const memorySlots = memoryManager.memorySlots;
            
            if (Object.keys(memorySlots).length === 0) {
                memoryDisplay.innerHTML = `
                    <div style="text-align: center; color: #888; margin-top: 20px;">
                        No memory slots available.
                        <br><br>
                        Use the controls to add memory slots.
                    </div>
                `;
                return;
            }
            
            // Sort file numbers numerically if possible
            const sortedFiles = Object.keys(memorySlots).sort((a, b) => {
                if (/^\d+$/.test(a) && /^\d+$/.test(b)) {
                    return parseInt(a) - parseInt(b);
                }
                return a.localeCompare(b);
            });
            
            for (const fileNumber of sortedFiles) {
                const slots = memorySlots[fileNumber];
                const slotCount = Object.keys(slots).length;
                
                const fileElement = document.createElement('div');
                fileElement.className = 'memory-file';
                
                const fileTitle = document.createElement('div');
                fileTitle.className = 'memory-file-title';
                fileTitle.textContent = `FILE ${fileNumber} (${slotCount} slots)`;
                fileElement.appendChild(fileTitle);
                
                // Sort slot numbers numerically if possible
                const sortedSlots = Object.keys(slots).sort((a, b) => {
                    if (/^\d+$/.test(a) && /^\d+$/.test(b)) {
                        return parseInt(a) - parseInt(b);
                    }
                    return a.localeCompare(b);
                });
                
                for (const slotNumber of sortedSlots) {
                    const value = slots[slotNumber];
                    
                    // Truncate long values for display
                    let displayValue = value;
                    if (displayValue.length > 100) {
                        displayValue = displayValue.substring(0, 97) + '...';
                    }
                    
                    const slotElement = document.createElement('div');
                    slotElement.className = 'memory-slot';
                    
                    const slotTitle = document.createElement('div');
                    slotTitle.className = 'memory-slot-title';
                    slotTitle.textContent = `Slot ${slotNumber}`;
                    
                    const slotValue = document.createElement('div');
                    slotValue.className = 'memory-slot-value';
                    slotValue.textContent = displayValue;
                    
                    slotElement.appendChild(slotTitle);
                    slotElement.appendChild(slotValue);
                    fileElement.appendChild(slotElement);
                }
                
                memoryDisplay.appendChild(fileElement);
            }
        }
        
        // Assign slot button click handler
        assignSlotBtn.addEventListener('click', () => {
            safeExecute(() => {
                const fileNum = memoryFile.value.trim();
                const slotNum = memorySlot.value.trim();
                const content = memoryContent.value;
                
                if (!fileNum) {
                    throw new Error('File number cannot be empty');
                }
                
                if (!slotNum) {
                    throw new Error('Slot number cannot be empty');
                }
                
                if (!content) {
                    throw new Error('Content cannot be empty');
                }
                
                const result = memoryManager.assignSlot(fileNum, slotNum, content);
                
                if (result.startsWith('Error')) {
                    throw new Error(result.substring(7));
                }
                
                updateMemoryDisplay();
                
                return result;
            }, error => {
                showError(`Memory error: ${error.message}`);
            });
        });
        
        // Read slot button click handler
        readSlotBtn.addEventListener('click', () => {
            safeExecute(() => {
                const fileNum = memoryFile.value.trim();
                const slotNum = memorySlot.value.trim();
                
                if (!fileNum) {
                    throw new Error('File number cannot be empty');
                }
                
                if (!slotNum) {
                    throw new Error('Slot number cannot be empty');
                }
                
                const result = memoryManager.readSlot(fileNum, slotNum);
                
                if (result.startsWith('Slot')) {
                    throw new Error(result);
                }
                
                memoryContent.value = result;
                
                return `Read value from slot ${slotNum} in file ${fileNum}`;
            }, error => {
                showError(`Memory error: ${error.message}`);
            });
        });
        
        // Clear all slots button click handler
        clearAllSlotsBtn.addEventListener('click', () => {
            if (confirm('Are you sure you want to clear all memory slots?')) {
                memoryManager.clearAll();
                updateMemoryDisplay();
                memoryContent.value = '';
            }
        });
        
        // Initialize memory display
        updateMemoryDisplay();
    }
    
    // ======== 3.3 Process Operations ========
    function setupProcessOperations() {
        const processName = document.getElementById('process-name');
        const processDuration = document.getElementById('process-duration');
        const startProcessBtn = document.getElementById('start-process');
        const stopAllProcessesBtn = document.getElementById('stop-all-processes');
        const processList = document.getElementById('process-list');
        
        // Process manager class
        class ProcessManager {
            constructor() {
                this.processes = new Map();
                this.nextProcessId = 1;
            }
            
            startProcess(name, duration, progressCallback, completeCallback) {
                const processId = this.nextProcessId++;
                const startTime = performance.now();
                const endTime = startTime + duration;
                
                // Create process object
                const process = {
                    id: processId,
                    name,
                    duration,
                    startTime,
                    endTime,
                    progress: 0,
                    status: 'running',
                    intervalId: null
                };
                
                // Start progress updates
                process.intervalId = setInterval(() => {
                    const now = performance.now();
                    const elapsed = now - startTime;
                    
                    if (elapsed >= duration) {
                        // Process complete
                        process.progress = 100;
                        process.status = 'completed';
                        clearInterval(process.intervalId);
                        
                        // Remove process after a delay
                        setTimeout(() => {
                            this.processes.delete(processId);
                            if (completeCallback) {
                                completeCallback(process);
                            }
                        }, 1000);
                    } else {
                        // Update progress
                        process.progress = (elapsed / duration) * 100;
                    }
                    
                    if (progressCallback) {
                        progressCallback(process);
                    }
                }, 50);
                
                // Add to process list
                this.processes.set(processId, process);
                
                return processId;
            }
            
            stopProcess(processId) {
                const process = this.processes.get(processId);
                
                if (process) {
                    clearInterval(process.intervalId);
                    process.status = 'stopped';
                    this.processes.delete(processId);
                    return true;
                }
                
                return false;
            }
            
            stopAllProcesses() {
                for (const [processId, process] of this.processes.entries()) {
                    clearInterval(process.intervalId);
                    process.status = 'stopped';
                }
                
                this.processes.clear();
                return true;
            }
        }
        
        // Create process manager
        const processManager = new ProcessManager();
        
        // Create process element
        function createProcessElement(process) {
            const processElement = document.createElement('div');
            processElement.className = 'process';
            processElement.id = `process-${process.id}`;
            
            const processHeader = document.createElement('div');
            processHeader.className = 'process-header';
            
            const processNameElement = document.createElement('div');
            processNameElement.className = 'process-name';
            processNameElement.textContent = process.name;
            
            const processClose = document.createElement('span');
            processClose.className = 'process-close';
            processClose.textContent = '×';
            processClose.title = 'Stop process';
            processClose.addEventListener('click', () => {
                processManager.stopProcess(process.id);
                processElement.remove();
            });
            
            processHeader.appendChild(processNameElement);
            processHeader.appendChild(processClose);
            
            const processProgress = document.createElement('div');
            processProgress.className = 'process-progress';
            
            const processBar = document.createElement('div');
            processBar.className = 'process-bar';
            processBar.style.width = `${process.progress}%`;
            
            processProgress.appendChild(processBar);
            
            const processStatus = document.createElement('div');
            processStatus.className = 'process-status';
            processStatus.textContent = `Status: ${process.status} - Progress: ${Math.round(process.progress)}%`;
            
            processElement.appendChild(processHeader);
            processElement.appendChild(processProgress);
            processElement.appendChild(processStatus);
            
            return processElement;
        }
        
        // Update process element
        function updateProcessElement(process) {
            const processElement = document.getElementById(`process-${process.id}`);
            
            if (processElement) {
                const processBar = processElement.querySelector('.process-bar');
                const processStatus = processElement.querySelector('.process-status');
                
                processBar.style.width = `${process.progress}%`;
                processStatus.textContent = `Status: ${process.status} - Progress: ${Math.round(process.progress)}%`;
                
                if (process.status === 'completed') {
                    processElement.classList.add('completed');
                }
            }
        }
        
        // Start process button click handler
        startProcessBtn.addEventListener('click', () => {
            safeExecute(() => {
                const name = processName.value.trim();
                const duration = parseInt(processDuration.value);
                
                if (!name) {
                    throw new Error('Process name cannot be empty');
                }
                
                if (isNaN(duration) || duration < 100 || duration > 10000) {
                    throw new Error('Duration must be between 100 and 10000 ms');
                }
                
                // Start the process
                const processId = processManager.startProcess(
                    name,
                    duration,
                    updateProcessElement,
                    process => {
                        // Process completed callback
                        const processElement = document.getElementById(`process-${process.id}`);
                        if (processElement) {
                            setTimeout(() => {
                                processElement.classList.add('fade-out');
                                setTimeout(() => {
                                    processElement.remove();
                                }, 500);
                            }, 1000);
                        }
                    }
                );
                
                // Create and add process element
                const process = processManager.processes.get(processId);
                const processElement = createProcessElement(process);
                processList.appendChild(processElement);
                
                // Clear input
                processName.value = '';
                
                return `Process "${name}" started`;
            }, error => {
                showError(`Process error: ${error.message}`);
            });
        });
        
        // Stop all processes button click handler
        stopAllProcessesBtn.addEventListener('click', () => {
            processManager.stopAllProcesses();
            processList.innerHTML = '';
        });
    }

    // ============ 4. CRUD OPERATIONS ============
    
    // Simple in-memory database
    const database = {
        records: new Map(),
        
        create(record) {
            if (!record.id) {
                throw new Error('Record must have an ID');
            }
            
            if (this.records.has(record.id)) {
                throw new Error(`Record with ID "${record.id}" already exists`);
            }
            
            this.records.set(record.id, { ...record, createdAt: new Date() });
            return true;
        },
        
        read(id) {
            if (!this.records.has(id)) {
                throw new Error(`Record with ID "${id}" not found`);
            }
            
            return { ...this.records.get(id) };
        },
        
        readAll() {
            return Array.from(this.records.values()).map(record => ({ ...record }));
        },
        
        update(id, updates) {
            if (!this.records.has(id)) {
                throw new Error(`Record with ID "${id}" not found`);
            }
            
            const record = this.records.get(id);
            const updatedRecord = { ...record, ...updates, updatedAt: new Date() };
            this.records.set(id, updatedRecord);
            
            return updatedRecord;
        },
        
        delete(id) {
            if (!this.records.has(id)) {
                throw new Error(`Record with ID "${id}" not found`);
            }
            
            return this.records.delete(id);
        },
        
        deleteAll() {
            this.records.clear();
            return true;
        },
        
        query(criteria) {
            return Array.from(this.records.values())
                .filter(record => {
                    for (const key in criteria) {
                        if (record[key] !== criteria[key]) {
                            return false;
                        }
                    }
                    return true;
                })
                .map(record => ({ ...record }));
        }
    };
    
    // ======== 4.1 Create Operations ========
    function setupCreateOperations() {
        const recordId = document.getElementById('record-id');
        const recordName = document.getElementById('record-name');
        const recordData = document.getElementById('record-data');
        const createRecordBtn = document.getElementById('create-record');
        const databaseDisplay = document.getElementById('database-display');
        
        // Create record button click handler
        createRecordBtn.addEventListener('click', () => {
            safeExecute(() => {
                const id = recordId.value.trim();
                const name = recordName.value.trim();
                const data = recordData.value.trim();
                
                if (!id) {
                    throw new Error('Record ID cannot be empty');
                }
                
                if (!name) {
                    throw new Error('Record name cannot be empty');
                }
                
                // Create the record
                database.create({
                    id,
                    name,
                    data
                });
                
                // Clear inputs
                recordId.value = '';
                recordName.value = '';
                recordData.value = '';
                
                // Update the display
                updateDatabaseDisplay();
                
                return `Record "${id}" created successfully`;
            }, error => {
                showError(`Create error: ${error.message}`);
            });
        });
        
        // Update database display
        function updateDatabaseDisplay() {
            databaseDisplay.innerHTML = '';
            
            const records = database.readAll();
            
            if (records.length === 0) {
                databaseDisplay.innerHTML = `
                    <div style="text-align: center; color: #888; margin-top: 20px;">
                        No records in the database.
                        <br><br>
                        Use the form to create records.
                    </div>
                `;
                return;
            }
            
            // Sort records by ID
            records.sort((a, b) => a.id.localeCompare(b.id));
            
            for (const record of records) {
                const recordElement = document.createElement('div');
                recordElement.className = 'database-record';
                
                const recordHeader = document.createElement('div');
                recordHeader.className = 'record-header';
                
                const recordIdElement = document.createElement('div');
                recordIdElement.className = 'record-id';
                recordIdElement.textContent = record.id;
                
                const recordControls = document.createElement('div');
                recordControls.className = 'record-controls';
                
                recordHeader.appendChild(recordIdElement);
                recordHeader.appendChild(recordControls);
                
                const recordContent = document.createElement('div');
                recordContent.className = 'record-content';
                recordContent.innerHTML = `
                    <div><strong>Name:</strong> ${record.name}</div>
                    <div><strong>Data:</strong> ${record.data || '<empty>'}</div>
                    <div><strong>Created:</strong> ${record.createdAt.toLocaleString()}</div>
                    ${record.updatedAt ? `<div><strong>Updated:</strong> ${record.updatedAt.toLocaleString()}</div>` : ''}
                `;
                
                recordElement.appendChild(recordHeader);
                recordElement.appendChild(recordContent);
                
                databaseDisplay.appendChild(recordElement);
            }
        }
        
        // Initialize the database display
        updateDatabaseDisplay();
        
        // Export for other functions
        return { updateDatabaseDisplay };
    }
    
    // ======== 4.2 Read Operations ========
    function setupReadOperations(displayUpdater) {
        const readId = document.getElementById('read-id');
        const readRecordBtn = document.getElementById('read-record');
        const readAllRecordsBtn = document.getElementById('read-all-records');
        const queryRecordsBtn = document.getElementById('query-records');
        const readResult = document.getElementById('read-result');
        
        // Read record button click handler
        readRecordBtn.addEventListener('click', () => {
            safeExecute(() => {
                const id = readId.value.trim();
                
                if (!id) {
                    throw new Error('Record ID cannot be empty');
                }
                
                const record = database.read(id);
                
                // Display the record
                readResult.innerHTML = '';
                
                const recordElement = document.createElement('div');
                recordElement.className = 'database-record';
                
                const recordHeader = document.createElement('div');
                recordHeader.className = 'record-header';
                
                const recordIdElement = document.createElement('div');
                recordIdElement.className = 'record-id';
                recordIdElement.textContent = record.id;
                
                recordHeader.appendChild(recordIdElement);
                
                const recordContent = document.createElement('div');
                recordContent.className = 'record-content';
                recordContent.innerHTML = `
                    <div><strong>Name:</strong> ${record.name}</div>
                    <div><strong>Data:</strong> ${record.data || '<empty>'}</div>
                    <div><strong>Created:</strong> ${record.createdAt.toLocaleString()}</div>
                    ${record.updatedAt ? `<div><strong>Updated:</strong> ${record.updatedAt.toLocaleString()}</div>` : ''}
                `;
                
                recordElement.appendChild(recordHeader);
                recordElement.appendChild(recordContent);
                
                readResult.appendChild(recordElement);
                
                return `Record "${id}" read successfully`;
            }, error => {
                readResult.innerHTML = `<div class="error">${error.message}</div>`;
            });
        });
        
        // Read all records button click handler
        readAllRecordsBtn.addEventListener('click', () => {
            safeExecute(() => {
                const records = database.readAll();
                
                if (records.length === 0) {
                    readResult.innerHTML = `
                        <div style="text-align: center; color: #888; margin-top: 20px;">
                            No records in the database.
                        </div>
                    `;
                    return `No records found in the database`;
                }
                
                // Display all records
                readResult.innerHTML = '';
                
                // Sort records by ID
                records.sort((a, b) => a.id.localeCompare(b.id));
                
                for (const record of records) {
                    const recordElement = document.createElement('div');
                    recordElement.className = 'database-record';
                    
                    const recordHeader = document.createElement('div');
                    recordHeader.className = 'record-header';
                    
                    const recordIdElement = document.createElement('div');
                    recordIdElement.className = 'record-id';
                    recordIdElement.textContent = record.id;
                    
                    recordHeader.appendChild(recordIdElement);
                    
                    const recordContent = document.createElement('div');
                    recordContent.className = 'record-content';
                    recordContent.innerHTML = `
                        <div><strong>Name:</strong> ${record.name}</div>
                        <div><strong>Data:</strong> ${record.data || '<empty>'}</div>
                        <div><strong>Created:</strong> ${record.createdAt.toLocaleString()}</div>
                        ${record.updatedAt ? `<div><strong>Updated:</strong> ${record.updatedAt.toLocaleString()}</div>` : ''}
                    `;
                    
                    recordElement.appendChild(recordHeader);
                    recordElement.appendChild(recordContent);
                    
                    readResult.appendChild(recordElement);
                }
                
                return `${records.length} records read successfully`;
            }, error => {
                readResult.innerHTML = `<div class="error">${error.message}</div>`;
            });
        });
        
        // Query records button click handler
        queryRecordsBtn.addEventListener('click', () => {
            safeExecute(() => {
                // Create a query dialog
                const queryValue = prompt('Enter search term to query records by name:');
                
                if (queryValue === null) return; // User cancelled
                
                const query = queryValue.trim();
                
                if (!query) {
                    throw new Error('Search term cannot be empty');
                }
                
                // Simple case-insensitive name search
                const records = database.readAll().filter(record => 
                    record.name.toLowerCase().includes(query.toLowerCase())
                );
                
                if (records.length === 0) {
                    readResult.innerHTML = `
                        <div style="text-align: center; color: #888; margin-top: 20px;">
                            No records found matching the query "${query}".
                        </div>
                    `;
                    return `No records found matching the query "${query}"`;
                }
                
                // Display all matching records
                readResult.innerHTML = '';
                
                // Sort records by ID
                records.sort((a, b) => a.id.localeCompare(b.id));
                
                for (const record of records) {
                    const recordElement = document.createElement('div');
                    recordElement.className = 'database-record';
                    
                    const recordHeader = document.createElement('div');
                    recordHeader.className = 'record-header';
                    
                    const recordIdElement = document.createElement('div');
                    recordIdElement.className = 'record-id';
                    recordIdElement.textContent = record.id;
                    
                    recordHeader.appendChild(recordIdElement);
                    
                    const recordContent = document.createElement('div');
                    recordContent.className = 'record-content';
                    recordContent.innerHTML = `
                        <div><strong>Name:</strong> ${record.name}</div>
                        <div><strong>Data:</strong> ${record.data || '<empty>'}</div>
                        <div><strong>Created:</strong> ${record.createdAt.toLocaleString()}</div>
                        ${record.updatedAt ? `<div><strong>Updated:</strong> ${record.updatedAt.toLocaleString()}</div>` : ''}
                    `;
                    
                    recordElement.appendChild(recordHeader);
                    recordElement.appendChild(recordContent);
                    
                    readResult.appendChild(recordElement);
                }
                
                return `${records.length} records found matching the query "${query}"`;
            }, error => {
                readResult.innerHTML = `<div class="error">${error.message}</div>`;
            });
        });
    }
    
    // ======== 4.3 Update Operations ========
    function setupUpdateOperations(displayUpdater) {
        const updateId = document.getElementById('update-id');
        const updateField = document.getElementById('update-field');
        const updateValue = document.getElementById('update-value');
        const updateRecordBtn = document.getElementById('update-record');
        const updateResult = document.getElementById('update-result');
        
        // Update record button click handler
        updateRecordBtn.addEventListener('click', () => {
            safeExecute(() => {
                const id = updateId.value.trim();
                const field = updateField.value;
                const value = updateValue.value.trim();
                
                if (!id) {
                    throw new Error('Record ID cannot be empty');
                }
                
                if (!field) {
                    throw new Error('Field cannot be empty');
                }
                
                // Create update object
                const updates = {
                    [field]: value
                };
                
                // Update the record
                const updatedRecord = database.update(id, updates);
                
                // Display the updated record
                updateResult.innerHTML = '';
                
                const recordElement = document.createElement('div');
                recordElement.className = 'database-record';
                
                const recordHeader = document.createElement('div');
                recordHeader.className = 'record-header';
                
                const recordIdElement = document.createElement('div');
                recordIdElement.className = 'record-id';
                recordIdElement.textContent = updatedRecord.id;
                
                recordHeader.appendChild(recordIdElement);
                
                const recordContent = document.createElement('div');
                recordContent.className = 'record-content';
                recordContent.innerHTML = `
                    <div><strong>Name:</strong> ${updatedRecord.name}</div>
                    <div><strong>Data:</strong> ${updatedRecord.data || '<empty>'}</div>
                    <div><strong>Created:</strong> ${updatedRecord.createdAt.toLocaleString()}</div>
                    <div><strong>Updated:</strong> ${updatedRecord.updatedAt.toLocaleString()}</div>
                `;
                
                recordElement.appendChild(recordHeader);
                recordElement.appendChild(recordContent);
                
                updateResult.appendChild(recordElement);
                
                // Clear inputs
                updateId.value = '';
                updateValue.value = '';
                
                // Update the database display
                if (displayUpdater) displayUpdater.updateDatabaseDisplay();
                
                return `Record "${id}" updated successfully`;
            }, error => {
                updateResult.innerHTML = `<div class="error">${error.message}</div>`;
            });
        });
    }
    
    // ======== 4.4 Delete Operations ========
    function setupDeleteOperations(displayUpdater) {
        const deleteId = document.getElementById('delete-id');
        const deleteRecordBtn = document.getElementById('delete-record');
        const deleteAllRecordsBtn = document.getElementById('delete-all-records');
        const deleteResult = document.getElementById('delete-result');
        
        // Delete record button click handler
        deleteRecordBtn.addEventListener('click', () => {
            safeExecute(() => {
                const id = deleteId.value.trim();
                
                if (!id) {
                    throw new Error('Record ID cannot be empty');
                }
                
                // Delete the record
                const result = database.delete(id);
                
                if (!result) {
                    throw new Error(`Failed to delete record "${id}"`);
                }
                
                // Clear input
                deleteId.value = '';
                
                // Update the database display
                if (displayUpdater) displayUpdater.updateDatabaseDisplay();
                
                deleteResult.innerHTML = `<div class="status-message status-success">Record "${id}" deleted successfully</div>`;
                
                return `Record "${id}" deleted successfully`;
            }, error => {
                deleteResult.innerHTML = `<div class="error">${error.message}</div>`;
            });
        });
        
        // Delete all records button click handler
        deleteAllRecordsBtn.addEventListener('click', () => {
            safeExecute(() => {
                if (!confirm('Are you sure you want to delete all records? This cannot be undone.')) {
                    return;
                }
                
                // Delete all records
                database.deleteAll();
                
                // Update the database display
                if (displayUpdater) displayUpdater.updateDatabaseDisplay();
                
                deleteResult.innerHTML = `<div class="status-message status-success">All records deleted successfully</div>`;
                
                return 'All records deleted successfully';
            }, error => {
                deleteResult.innerHTML = `<div class="error">${error.message}</div>`;
            });
        });
    }

    // ============ 5. ADVANCED CONCEPTS ============
    
    // ======== 5.1 Serialization Operations ========
    function setupSerializationOperations() {
        const serializeInput = document.getElementById('serialize-input');
        const serializationFormat = document.getElementById('serialization-format');
        const serializeBtn = document.getElementById('serialize-data');
        const deserializeBtn = document.getElementById('deserialize-data');
        const resultContainer = document.getElementById('serialization-result');
        
        // Currently serialized data
        let serializedData = '';
        let originalObject = null;
        
        // Serialize button click handler
        serializeBtn.addEventListener('click', () => {
            safeExecute(() => {
                const input = serializeInput.value.trim();
                const format = serializationFormat.value;
                
                if (!input) {
                    throw new Error('Input cannot be empty');
                }
                
                // Parse the input as JSON to get an object
                try {
                    originalObject = JSON.parse(input);
                } catch (e) {
                    throw new Error('Invalid JSON input. Please check your syntax.');
                }
                
                // Serialize the object according to the selected format
                serializedData = serializeObject(originalObject, format);
                
                // Display the serialized data
                resultContainer.innerHTML = '';
                
                const resultHeader = document.createElement('div');
                resultHeader.className = 'serialization-header';
                resultHeader.innerHTML = `<strong>Serialized Data (${format}):</strong>`;
                resultContainer.appendChild(resultHeader);
                
                const resultContent = document.createElement('pre');
                resultContent.className = 'serialization-content';
                resultContent.textContent = serializedData;
                resultContainer.appendChild(resultContent);
                
                return `Data serialized to ${format} format`;
            }, error => {
                resultContainer.innerHTML = `<div class="error">${error.message}</div>`;
            });
        });
        
        // Deserialize button click handler
        deserializeBtn.addEventListener('click', () => {
            safeExecute(() => {
                const format = serializationFormat.value;
                
                if (!serializedData) {
                    throw new Error('No serialized data to deserialize');
                }
                
                // Deserialize the data according to the selected format
                const deserializedObject = deserializeData(serializedData, format);
                
                // Display the deserialized object
                resultContainer.innerHTML = '';
                
                const resultHeader = document.createElement('div');
                resultHeader.className = 'serialization-header';
                resultHeader.innerHTML = `<strong>Deserialized Object:</strong>`;
                resultContainer.appendChild(resultHeader);
                
                const resultContent = document.createElement('pre');
                resultContent.className = 'serialization-content';
                resultContent.textContent = JSON.stringify(deserializedObject, null, 2);
                resultContainer.appendChild(resultContent);
                
                // Display comparison
                const comparisonHeader = document.createElement('div');
                comparisonHeader.className = 'serialization-header mt-20';
                comparisonHeader.innerHTML = `<strong>Comparison with Original:</strong>`;
                resultContainer.appendChild(comparisonHeader);
                
                const isEqual = compareObjects(originalObject, deserializedObject);
                
                const comparisonResult = document.createElement('div');
                comparisonResult.className = isEqual ? 'status-success' : 'status-error';
                comparisonResult.textContent = isEqual 
                    ? 'Objects are identical. Serialization and deserialization completed successfully.'
                    : 'Objects are different. Some data may have been lost in the process.';
                resultContainer.appendChild(comparisonResult);
                
                return `Data deserialized from ${format} format`;
            }, error => {
                resultContainer.innerHTML = `<div class="error">${error.message}</div>`;
            });
        });
        
        // Serialize an object to the specified format
        function serializeObject(obj, format) {
            switch (format) {
                case 'json':
                    return JSON.stringify(obj, null, 2);
                
                case 'xml':
                    return objectToXML(obj);
                
                case 'csv':
                    return objectToCSV(obj);
                
                default:
                    throw new Error(`Unsupported format: ${format}`);
            }
        }
        
        // Deserialize data from the specified format
        function deserializeData(data, format) {
            switch (format) {
                case 'json':
                    return JSON.parse(data);
                
                case 'xml':
                    return xmlToObject(data);
                
                case 'csv':
                    return csvToObject(data);
                
                default:
                    throw new Error(`Unsupported format: ${format}`);
            }
        }
        
        // Convert object to XML
        function objectToXML(obj) {
            function addIndent(level) {
                return ' '.repeat(level * 2);
            }
            
            function objectToXMLRecursive(obj, name, level = 0) {
                let xml = `${addIndent(level)}<${name}>`;
                
                if (obj === null) {
                    return `${xml}null</${name}>`;
                }
                
                if (typeof obj !== 'object') {
                    return `${xml}${String(obj)}</${name}>`;
                }
                
                xml += '\n';
                
                if (Array.isArray(obj)) {
                    for (let i = 0; i < obj.length; i++) {
                        xml += objectToXMLRecursive(obj[i], 'item', level + 1) + '\n';
                    }
                } else {
                    for (const key in obj) {
                        if (obj.hasOwnProperty(key)) {
                            xml += objectToXMLRecursive(obj[key], key, level + 1) + '\n';
                        }
                    }
                }
                
                xml += `${addIndent(level)}</${name}>`;
                return xml;
            }
            
            return objectToXMLRecursive(obj, 'root');
        }
        
        // Convert XML to object (simplified)
        function xmlToObject(xml) {
            // This is a very simplified XML parser
            // In a real-world scenario, you would use a proper XML parser
            
            // Extract content within root tags
            const rootMatch = xml.match(/<root>([\s\S]*)<\/root>/);
            if (!rootMatch) {
                throw new Error('Invalid XML: root tag not found');
            }
            
            const rootContent = rootMatch[1];
            
            // Parse key-value pairs
            const result = {};
            const keyPattern = /<(\w+)>([\s\S]*?)<\/\1>/g;
            let match;
            
            while ((match = keyPattern.exec(rootContent)) !== null) {
                const key = match[1];
                const value = match[2].trim();
                
                // Try to parse nested objects
                if (value.includes('<')) {
                    // Check if it's an array of items
                    if (value.includes('<item>')) {
                        result[key] = [];
                        const itemPattern = /<item>([\s\S]*?)<\/item>/g;
                        let itemMatch;
                        
                        while ((itemMatch = itemPattern.exec(value)) !== null) {
                            const itemValue = itemMatch[1].trim();
                            
                            if (itemValue.includes('<')) {
                                // Try to parse as object
                                try {
                                    const dummyXml = `<root>${itemValue}</root>`;
                                    result[key].push(xmlToObject(dummyXml));
                                } catch (e) {
                                    result[key].push(itemValue);
                                }
                            } else {
                                // Try to parse as number or boolean
                                result[key].push(parseValue(itemValue));
                            }
                        }
                    } else {
                        // Try to parse as object
                        try {
                            const dummyXml = `<root>${value}</root>`;
                            result[key] = xmlToObject(dummyXml);
                        } catch (e) {
                            result[key] = value;
                        }
                    }
                } else {
                    // Parse as primitive value
                    result[key] = parseValue(value);
                }
            }
            
            return result;
        }
        
        // Convert object to CSV (for flat objects or arrays of flat objects)
        function objectToCSV(obj) {
            if (Array.isArray(obj)) {
                // Array of objects - create CSV with headers
                if (obj.length === 0) {
                    return '';
                }
                
                // Get headers from the first object
                const headers = Object.keys(obj[0]);
                let csv = headers.join(',') + '\n';
                
                // Add rows
                for (const item of obj) {
                    const row = headers.map(header => {
                        const value = item[header];
                        return escapeCSV(value);
                    }).join(',');
                    
                    csv += row + '\n';
                }
                
                return csv;
            } else {
                // Single object - create key-value CSV
                let csv = 'key,value\n';
                
                for (const key in obj) {
                    if (obj.hasOwnProperty(key)) {
                        const value = obj[key];
                        csv += `${escapeCSV(key)},${escapeCSV(value)}\n`;
                    }
                }
                
                return csv;
            }
        }
        
        // Convert CSV to object
        function csvToObject(csv) {
            const lines = csv.split('\n').filter(line => line.trim() !== '');
            if (lines.length < 2) {
                return {};
            }
            
            const headers = lines[0].split(',');
            
            // Check if it's key-value format
            if (headers.length === 2 && headers[0] === 'key' && headers[1] === 'value') {
                const result = {};
                
                for (let i = 1; i < lines.length; i++) {
                    const [key, value] = parseCSVLine(lines[i]);
                    result[key] = parseValue(value);
                }
                
                return result;
            } else {
                // Array of objects format
                const result = [];
                
                for (let i = 1; i < lines.length; i++) {
                    const values = parseCSVLine(lines[i]);
                    const item = {};
                    
                    for (let j = 0; j < headers.length; j++) {
                        item[headers[j]] = parseValue(values[j] || '');
                    }
                    
                    result.push(item);
                }
                
                return result;
            }
        }
        
        // Parse a CSV line, handling quoted values
        function parseCSVLine(line) {
            const values = [];
            let current = '';
            let inQuotes = false;
            
            for (let i = 0; i < line.length; i++) {
                const char = line[i];
                
                if (char === '"') {
                    if (i + 1 < line.length && line[i + 1] === '"') {
                        // Escaped quote
                        current += '"';
                        i++;
                    } else {
                        // Toggle quote mode
                        inQuotes = !inQuotes;
                    }
                } else if (char === ',' && !inQuotes) {
                    // End of value
                    values.push(current);
                    current = '';
                } else {
                    current += char;
                }
            }
            
            // Add the last value
            values.push(current);
            
            return values;
        }
        
        // Escape a value for CSV
        function escapeCSV(value) {
            if (value == null) {
                return '';
            }
            
            const strValue = String(value);
            
            if (strValue.includes(',') || strValue.includes('"') || strValue.includes('\n')) {
                // Escape quotes by doubling them and wrap in quotes
                return `"${strValue.replace(/"/g, '""')}"`;
            }
            
            return strValue;
        }
        
        // Parse a value to the appropriate type
        function parseValue(value) {
            if (value === 'null') {
                return null;
            }
            
            if (value === 'true') {
                return true;
            }
            
            if (value === 'false') {
                return false;
            }
            
            if (!isNaN(Number(value))) {
                return Number(value);
            }
            
            return value;
        }
        
        // Compare two objects for equality
        function compareObjects(a, b) {
            if (a === b) {
                return true;
            }
            
            if (typeof a !== 'object' || typeof b !== 'object' || a == null || b == null) {
                return false;
            }
            
            const keysA = Object.keys(a);
            const keysB = Object.keys(b);
            
            if (keysA.length !== keysB.length) {
                return false;
            }
            
            for (const key of keysA) {
                if (!keysB.includes(key)) {
                    return false;
                }
                
                if (!compareObjects(a[key], b[key])) {
                    return false;
                }
            }
            
            return true;
        }
    }
    
    // ======== 5.2 Compression Operations ========
    function setupCompressionOperations() {
        const compressionInput = document.getElementById('compression-input');
        const compressionMethod = document.getElementById('compression-method');
        const compressBtn = document.getElementById('compress-data');
        const decompressBtn = document.getElementById('decompress-data');
        const resultContainer = document.getElementById('compression-result');
        const statsContainer = document.getElementById('compression-stats');
        
        // Currently compressed data
        let compressedData = '';
        let originalData = '';
        let currentMethod = '';
        
        // Compress button click handler
        compressBtn.addEventListener('click', () => {
            safeExecute(() => {
                originalData = compressionInput.value;
                currentMethod = compressionMethod.value;
                
                if (!originalData) {
                    throw new Error('Input cannot be empty');
                }
                
                // Compress the data according to the selected method
                const compressionResult = compressData(originalData, currentMethod);
                compressedData = compressionResult.data;
                
                // Display the compressed data
                resultContainer.innerHTML = '';
                
                const resultHeader = document.createElement('div');
                resultHeader.className = 'compression-header';
                resultHeader.innerHTML = `<strong>Compressed Data (${currentMethod}):</strong>`;
                resultContainer.appendChild(resultHeader);
                
                const resultContent = document.createElement('pre');
                resultContent.className = 'compression-content';
                resultContent.textContent = compressedData;
                resultContainer.appendChild(resultContent);
                
                // Display compression stats
                statsContainer.innerHTML = '';
                
                const originalSize = new Blob([originalData]).size;
                const compressedSize = new Blob([compressedData]).size;
                const compressionRatio = originalSize / compressedSize;
                const spaceSavings = (1 - (compressedSize / originalSize)) * 100;
                
                statsContainer.innerHTML = `
                    <div><strong>Original Size:</strong> ${originalSize} bytes</div>
                    <div><strong>Compressed Size:</strong> ${compressedSize} bytes</div>
                    <div><strong>Compression Ratio:</strong> ${compressionRatio.toFixed(2)}:1</div>
                    <div><strong>Space Savings:</strong> ${spaceSavings.toFixed(2)}%</div>
                `;
                
                return `Data compressed using ${currentMethod}`;
            }, error => {
                resultContainer.innerHTML = `<div class="error">${error.message}</div>`;
                statsContainer.innerHTML = '';
            });
        });
        
        // Decompress button click handler
        decompressBtn.addEventListener('click', () => {
            safeExecute(() => {
                if (!compressedData) {
                    throw new Error('No compressed data to decompress');
                }
                
                // Decompress the data
                const decompressedData = decompressData(compressedData, currentMethod);
                
                // Display the decompressed data
                resultContainer.innerHTML = '';
                
                const resultHeader = document.createElement('div');
                resultHeader.className = 'compression-header';
                resultHeader.innerHTML = `<strong>Decompressed Data:</strong>`;
                resultContainer.appendChild(resultHeader);
                
                const resultContent = document.createElement('pre');
                resultContent.className = 'compression-content';
                resultContent.textContent = decompressedData;
                resultContainer.appendChild(resultContent);
                
                // Update stats
                statsContainer.innerHTML += `
                    <div class="mt-10"><strong>Verification:</strong> ${
                        decompressedData === originalData
                            ? '<span class="status-success">Data matches original</span>'
                            : '<span class="status-error">Data does not match original</span>'
                    }</div>
                `;
                
                return `Data decompressed using ${currentMethod}`;
            }, error => {
                resultContainer.innerHTML = `<div class="error">${error.message}</div>`;
            });
        });
        
        // Compress data using the specified method
        function compressData(data, method) {
            switch (method) {
                case 'rle':
                    return { data: runLengthEncode(data) };
                
                case 'huffman':
                    return { data: huffmanEncode(data) };
                
                case 'lz':
                    return { data: lzCompress(data) };
                
                default:
                    throw new Error(`Unsupported compression method: ${method}`);
            }
        }
        
        // Decompress data using the specified method
        function decompressData(data, method) {
            switch (method) {
                case 'rle':
                    return runLengthDecode(data);
                
                case 'huffman':
                    return huffmanDecode(data);
                
                case 'lz':
                    return lzDecompress(data);
                
                default:
                    throw new Error(`Unsupported compression method: ${method}`);
            }
        }
        
        // Run-Length Encoding
        function runLengthEncode(data) {
            let encoded = '';
            let count = 1;
            
            for (let i = 0; i < data.length; i++) {
                // If the current character is the same as the next, increment count
                if (data[i] === data[i + 1]) {
                    count++;
                } else {
                    // Otherwise, add the count and character to the result
                    if (count >= 4) {
                        // Only use RLE for runs of 4 or more
                        encoded += `${count}${data[i]}`;
                    } else {
                        // Otherwise, just use the raw characters
                        encoded += data[i].repeat(count);
                    }
                    count = 1;
                }
            }
            
            return encoded;
        }
        
        // Run-Length Decoding
        function runLengthDecode(data) {
            let decoded = '';
            let countStr = '';
            
            for (let i = 0; i < data.length; i++) {
                const char = data[i];
                
                if (/\d/.test(char)) {
                    // If it's a digit, add it to the count
                    countStr += char;
                } else {
                    // Otherwise, it's a character
                    let count = countStr ? parseInt(countStr) : 1;
                    decoded += char.repeat(count);
                    countStr = '';
                }
            }
            
            return decoded;
        }
        
        // Huffman Encoding (simplified version)
        function huffmanEncode(data) {
            // Count frequency of each character
            const frequencies = {};
            for (const char of data) {
                frequencies[char] = (frequencies[char] || 0) + 1;
            }
            
            // Build Huffman tree (simplified as a dictionary)
            // In a real Huffman implementation, we would build a tree and traverse it
            const codes = {};
            let index = 0;
            
            for (const char in frequencies) {
                // Use binary representation of index as the code (simpler than a real Huffman tree)
                codes[char] = index.toString(2).padStart(4, '0');
                index++;
                
                if (index >= 16) {
                    break; // Limit to 16 distinct characters for simplicity
                }
            }
            
            // Encode the data
            let encoded = '';
            
            // First, add the dictionary
            for (const char in codes) {
                const charCode = char.charCodeAt(0).toString(16).padStart(4, '0');
                encoded += `${charCode}:${codes[char]};`;
            }
            
            encoded += '|'; // Dictionary/data separator
            
            // Then encode the data
            for (const char of data) {
                encoded += codes[char] || '';
            }
            
            return encoded;
        }
        
        // Huffman Decoding (simplified version)
        function huffmanDecode(data) {
            // Split into dictionary and encoded data
            const parts = data.split('|');
            if (parts.length !== 2) {
                throw new Error('Invalid Huffman encoded data');
            }
            
            const dictionaryStr = parts[0];
            const encodedData = parts[1];
            
            // Parse the dictionary
            const codeToChar = {};
            const dictionaryEntries = dictionaryStr.split(';');
            
            for (const entry of dictionaryEntries) {
                if (!entry) continue;
                
                const [charHex, code] = entry.split(':');
                if (!charHex || !code) continue;
                
                const char = String.fromCharCode(parseInt(charHex, 16));
                codeToChar[code] = char;
            }
            
            // Decode the data
            let decoded = '';
            let currentCode = '';
            
            for (const bit of encodedData) {
                currentCode += bit;
                
                if (codeToChar[currentCode]) {
                    decoded += codeToChar[currentCode];
                    currentCode = '';
                }
            }
            
            return decoded;
        }
        
        // LZ Compression (simplified version of LZ77)
        function lzCompress(data) {
            let compressed = '';
            let pos = 0;
            
            while (pos < data.length) {
                // Look for longest match in the window
                let bestLength = 0;
                let bestOffset = 0;
                const maxOffset = Math.min(255, pos); // Limit to 255 for simplicity
                const maxLength = Math.min(255, data.length - pos); // Limit to 255 for simplicity
                
                for (let offset = 1; offset <= maxOffset; offset++) {
                    let length = 0;
                    while (length < maxLength && data[pos - offset + (length % offset)] === data[pos + length]) {
                        length++;
                    }
                    
                    if (length > bestLength) {
                        bestLength = length;
                        bestOffset = offset;
                    }
                }
                
                if (bestLength >= 3) { // Only compress sequences of 3 or more
                    // Add a reference as (offset, length)
                    compressed += `(${bestOffset},${bestLength})`;
                    pos += bestLength;
                } else {
                    // Add the character as is
                    if (/[\\()]/.test(data[pos])) {
                        compressed += '\\' + data[pos]; // Escape special characters
                    } else {
                        compressed += data[pos];
                    }
                    pos++;
                }
            }
            
            return compressed;
        }
        
        // LZ Decompression
        function lzDecompress(data) {
            let decompressed = '';
            let pos = 0;
            
            while (pos < data.length) {
                if (data[pos] === '\\') {
                    // Escaped character
                    decompressed += data[pos + 1];
                    pos += 2;
                } else if (data[pos] === '(') {
                    // Reference (offset, length)
                    const match = data.substring(pos).match(/^\((\d+),(\d+)\)/);
                    if (!match) {
                        throw new Error('Invalid LZ compressed data');
                    }
                    
                    const offset = parseInt(match[1]);
                    const length = parseInt(match[2]);
                    
                    for (let i = 0; i < length; i++) {
                        decompressed += decompressed[decompressed.length - offset + (i % offset)];
                    }
                    
                    pos += match[0].length;
                } else {
                    // Literal character
                    decompressed += data[pos];
                    pos++;
                }
            }
            
            return decompressed;
        }
    }
    
    // ======== 5.3 Binary Encoding Operations ========
    function setupEncodingOperations() {
        const encodingInput = document.getElementById('encoding-input');
        const encodingMethod = document.getElementById('encoding-method');
        const encodeBtn = document.getElementById('encode-data');
        const decodeBtn = document.getElementById('decode-data');
        const resultContainer = document.getElementById('encoding-result');
        
        // Currently encoded data
        let encodedData = '';
        let originalData = '';
        let currentMethod = '';
        
        // Encode button click handler
        encodeBtn.addEventListener('click', () => {
            safeExecute(() => {
                originalData = encodingInput.value;
                currentMethod = encodingMethod.value;
                
                if (!originalData) {
                    throw new Error('Input cannot be empty');
                }
                
                // Encode the data according to the selected method
                encodedData = encodeData(originalData, currentMethod);
                
                // Display the encoded data
                resultContainer.innerHTML = '';
                
                const resultHeader = document.createElement('div');
                resultHeader.className = 'encoding-header';
                resultHeader.innerHTML = `<strong>Encoded Data (${currentMethod}):</strong>`;
                resultContainer.appendChild(resultHeader);
                
                const resultContent = document.createElement('pre');
                resultContent.className = 'encoding-content';
                resultContent.textContent = encodedData;
                resultContainer.appendChild(resultContent);
                
                return `Data encoded using ${currentMethod}`;
            }, error => {
                resultContainer.innerHTML = `<div class="error">${error.message}</div>`;
            });
        });
        
        // Decode button click handler
        decodeBtn.addEventListener('click', () => {
            safeExecute(() => {
                const input = encodingInput.value;
                currentMethod = encodingMethod.value;
                
                if (!input) {
                    throw new Error('Input cannot be empty');
                }
                
                // Decode the data
                const decodedData = decodeData(input, currentMethod);
                
                // Display the decoded data
                resultContainer.innerHTML = '';
                
                const resultHeader = document.createElement('div');
                resultHeader.className = 'encoding-header';
                resultHeader.innerHTML = `<strong>Decoded Data:</strong>`;
                resultContainer.appendChild(resultHeader);
                
                const resultContent = document.createElement('pre');
                resultContent.className = 'encoding-content';
                resultContent.textContent = decodedData;
                resultContainer.appendChild(resultContent);
                
                return `Data decoded from ${currentMethod}`;
            }, error => {
                resultContainer.innerHTML = `<div class="error">${error.message}</div>`;
            });
        });
        
        // Encode data using the specified method
        function encodeData(data, method) {
            switch (method) {
                case 'base64':
                    return btoa(unescape(encodeURIComponent(data)));
                
                case 'hex':
                    return [...data].map(c => c.charCodeAt(0).toString(16).padStart(2, '0')).join('');
                
                case 'binary':
                    return [...data].map(c => c.charCodeAt(0).toString(2).padStart(8, '0')).join(' ');
                
                case 'custom':
                    return generateCustomId(data);
                
                default:
                    throw new Error(`Unsupported encoding method: ${method}`);
            }
        }
        
        // Decode data using the specified method
        function decodeData(data, method) {
            switch (method) {
                case 'base64':
                    return decodeURIComponent(escape(atob(data)));
                
                case 'hex':
                    if (!/^[0-9A-Fa-f]+$/.test(data) || data.length % 2 !== 0) {
                        throw new Error('Invalid hexadecimal string');
                    }
                    let result = '';
                    for (let i = 0; i < data.length; i += 2) {
                        result += String.fromCharCode(parseInt(data.substr(i, 2), 16));
                    }
                    return result;
                
                case 'binary':
                    return data.split(' ')
                        .filter(binary => binary.trim() !== '')
                        .map(binary => String.fromCharCode(parseInt(binary, 2)))
                        .join('');
                
                case 'custom':
                    return decodeCustomId(data);
                
                default:
                    throw new Error(`Unsupported encoding method: ${method}`);
            }
        }
        
        // Generate a custom string ID
        function generateCustomId(data) {
            const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
            const charsetLength = charset.length;
            
            let id = '';
            
            // Convert string to a large integer
            for (let i = 0; i < data.length; i++) {
                const charCode = data.charCodeAt(i);
                id = id * charsetLength + (charCode % charsetLength);
            }
            
            // Add a simple checksum
            const checksum = data.split('').reduce((sum, char) => sum + char.charCodeAt(0), 0) % 97;
            
            return id.toString() + '-' + checksum;
        }
        
        // Decode a custom string ID (simplified - in practice this would require the original charset)
        function decodeCustomId(id) {
            // This is a placeholder since we can't fully decode without additional information
            // In practice, the encoding would need to be reversible
            
            // Extract the checksum
            const parts = id.split('-');
            if (parts.length !== 2) {
                throw new Error('Invalid custom ID format');
            }
            
            return `[Original data (ID: ${parts[0]}, Checksum: ${parts[1]})]`;
        }
    }
    
    // ======== 5.4 Transaction Operations ========
    function setupTransactionOperations() {
        const drawingColor = document.getElementById('drawing-color');
        const drawingSize = document.getElementById('drawing-size');
        const undoBtn = document.getElementById('transaction-undo');
        const redoBtn = document.getElementById('transaction-redo');
        const clearBtn = document.getElementById('transaction-clear');
        const canvas = document.getElementById('drawing-canvas');
        const historyContainer = document.getElementById('transaction-history');
        const context = canvas.getContext('2d');
        
        // Transaction management
        let actionHistory = [];
        let redoStack = [];
        let isDrawing = false;
        let lastX = 0;
        let lastY = 0;
        
        // Set up canvas and initial state
        function initCanvas() {
            // Set canvas background
            context.fillStyle = 'white';
            context.fillRect(0, 0, canvas.width, canvas.height);
            
            // Add event listeners
            canvas.addEventListener('mousedown', startDrawing);
            canvas.addEventListener('mousemove', draw);
            canvas.addEventListener('mouseup', stopDrawing);
            canvas.addEventListener('mouseout', stopDrawing);
            
            // Touch support
            canvas.addEventListener('touchstart', handleTouchStart);
            canvas.addEventListener('touchmove', handleTouchMove);
            canvas.addEventListener('touchend', stopDrawing);
            
            updateButtons();
        }
        
        // Start drawing
        function startDrawing(e) {
            isDrawing = true;
            const pos = getPosition(e);
            lastX = pos.x;
            lastY = pos.y;
            
            // Start a new transaction
            saveInitialState();
        }
        
        // Draw on canvas
        function draw(e) {
            if (!isDrawing) return;
            
            const pos = getPosition(e);
            const currentX = pos.x;
            const currentY = pos.y;
            
            context.beginPath();
            context.moveTo(lastX, lastY);
            context.lineTo(currentX, currentY);
            context.strokeStyle = drawingColor.value;
            context.lineWidth = parseInt(drawingSize.value);
            context.lineCap = 'round';
            context.stroke();
            
            lastX = currentX;
            lastY = currentY;
        }
        
        // Stop drawing
        function stopDrawing() {
            if (isDrawing) {
                isDrawing = false;
                saveFinalState();
            }
        }
        
        // Handle touch events
        function handleTouchStart(e) {
            e.preventDefault();
            if (e.touches.length === 1) {
                const touch = e.touches[0];
                const mouseEvent = new MouseEvent('mousedown', {
                    clientX: touch.clientX,
                    clientY: touch.clientY
                });
                canvas.dispatchEvent(mouseEvent);
            }
        }
        
        function handleTouchMove(e) {
            e.preventDefault();
            if (e.touches.length === 1) {
                const touch = e.touches[0];
                const mouseEvent = new MouseEvent('mousemove', {
                    clientX: touch.clientX,
                    clientY: touch.clientY
                });
                canvas.dispatchEvent(mouseEvent);
            }
        }
        
        // Get mouse position relative to canvas
        function getPosition(e) {
            const rect = canvas.getBoundingClientRect();
            return {
                x: e.clientX - rect.left,
                y: e.clientY - rect.top
            };
        }
        
        // Transaction handling
        function saveInitialState() {
            // Capture the current canvas state
            const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
            actionHistory.push({
                state: imageData,
                operation: 'Drawing started',
                color: drawingColor.value,
                size: drawingSize.value,
                timestamp: new Date().toISOString()
            });
            
            // Clear redo stack when a new action is performed
            redoStack = [];
            
            updateHistory();
            updateButtons();
        }
        
        function saveFinalState() {
            // Capture the final canvas state after drawing
            const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
            actionHistory.push({
                state: imageData,
                operation: 'Drawing completed',
                color: drawingColor.value,
                size: drawingSize.value,
                timestamp: new Date().toISOString()
            });
            
            updateHistory();
            updateButtons();
        }
        
        // Undo the last action
        function undo() {
            if (actionHistory.length <= 1) return;
            
            // Get the previous state
            const currentState = actionHistory.pop();
            redoStack.push(currentState);
            
            const previousState = actionHistory[actionHistory.length - 1];
            
            // Restore the previous state
            context.putImageData(previousState.state, 0, 0);
            
            updateHistory();
            updateButtons();
        }
        
        // Redo the last undone action
        function redo() {
            if (redoStack.length === 0) return;
            
            // Get the next state
            const nextState = redoStack.pop();
            actionHistory.push(nextState);
            
            // Restore the next state
            context.putImageData(nextState.state, 0, 0);
            
            updateHistory();
            updateButtons();
        }
        
        // Clear the canvas
        function clearCanvas() {
            // Save current state before clearing
            const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
            actionHistory.push({
                state: imageData,
                operation: 'Before clear',
                timestamp: new Date().toISOString()
            });
            
            // Clear the canvas
            context.fillStyle = 'white';
            context.fillRect(0, 0, canvas.width, canvas.height);
            
            // Save the cleared state
            const clearedImageData = context.getImageData(0, 0, canvas.width, canvas.height);
            actionHistory.push({
                state: clearedImageData,
                operation: 'Canvas cleared',
                timestamp: new Date().toISOString()
            });
            
            // Clear redo stack
            redoStack = [];
            
            updateHistory();
            updateButtons();
        }
        
        // Update transaction history display
        function updateHistory() {
            historyContainer.innerHTML = '';
            
            // Display last 5 transactions
            const start = Math.max(0, actionHistory.length - 5);
            for (let i = start; i < actionHistory.length; i++) {
                const transaction = actionHistory[i];
                const item = document.createElement('div');
                item.className = 'transaction-item';
                
				const time = new Date(transaction.timestamp).toLocaleTimeString();
                item.textContent = `${time}: ${transaction.operation}`;
                
                if (transaction.color) {
                    const colorSwatch = document.createElement('span');
                    colorSwatch.className = 'color-swatch';
                    colorSwatch.style.backgroundColor = transaction.color;
                    colorSwatch.style.display = 'inline-block';
                    colorSwatch.style.width = '10px';
                    colorSwatch.style.height = '10px';
                    colorSwatch.style.marginLeft = '5px';
                    
                    item.appendChild(colorSwatch);
                }
                
                historyContainer.appendChild(item);
            }
		}
        
        // Update button states
        function updateButtons() {
            undoBtn.disabled = actionHistory.length <= 1;
            redoBtn.disabled = redoStack.length === 0;
        }
        
        // Initialize
        initCanvas();
        
        // Add event listeners
        undoBtn.addEventListener('click', undo);
        redoBtn.addEventListener('click', redo);
        clearBtn.addEventListener('click', clearCanvas);
    }

    // ============ INITIALIZATION ============

    /**
     * Initialize the application
     */
    function init() {
        // Setup error modal close button
        const errorModal = document.getElementById('error-modal');
        const resultModal = document.getElementById('result-modal');
        const closeButtons = document.querySelectorAll('.close-btn');
        
        closeButtons.forEach(button => {
            button.addEventListener('click', function() {
                errorModal.style.display = 'none';
                resultModal.style.display = 'none';
            });
        });
		
		// Add to window event listeners in the init function
		window.addEventListener('beforeunload', function() {
		  // Explicitly clear all sensitive data structures
		  virtualFS.root.children = {};
		  database.deleteAll();
		  memoryManager.clearAll();
		  // Other data structures as needed
		});
        
        // Close modals when clicking outside
        window.addEventListener('click', function(event) {
            if (event.target === errorModal) {
                errorModal.style.display = 'none';
            }
            if (event.target === resultModal) {
                resultModal.style.display = 'none';
            }
        });
        
        // Setup navigation
        setupNavigation();
        
        // Setup all operations
        setupArrayOperations();
        setupObjectOperations();
        setupSetOperations();
        setupTreeOperations();
        setupRecursionOperations();
        setupIterationOperations();
        setupSearchOperations();
        setupBinaryOperations();
        setupFileOperations();
        setupMemoryOperations();
        setupProcessOperations();
        
        // CRUD operations - Create returns an object with updateDatabaseDisplay function
        // which is passed to the other CRUD operations
        const databaseDisplayUpdater = setupCreateOperations();
        setupReadOperations(databaseDisplayUpdater);
        setupUpdateOperations(databaseDisplayUpdater);
        setupDeleteOperations(databaseDisplayUpdater);
        
        setupSerializationOperations();
        setupCompressionOperations();
        setupEncodingOperations();
        setupTransactionOperations();
		
		// Add this to the init function in operator.js

		/**
		 * Setup session persistence
		 */
		function setupSessionPersistence() {
			// Create UI elements for persistence controls
			const navContainer = document.getElementById('main-nav');
			
			const persistenceSection = document.createElement('div');
			persistenceSection.className = 'nav-section';
			persistenceSection.innerHTML = `
				<h3>Session</h3>
				<div class="persistence-controls">
					<button id="save-session" title="Save current workspace to browser storage">Save Session</button>
					<button id="load-session" title="Load saved workspace from browser storage">Load Session</button>
					<button id="clear-session" title="Clear saved workspace data" class="button-secondary">Clear Saved Data</button>
				</div>
			`;
			
			navContainer.appendChild(persistenceSection);
			
			// Add event listeners
			const saveSessionBtn = document.getElementById('save-session');
			const loadSessionBtn = document.getElementById('load-session');
			const clearSessionBtn = document.getElementById('clear-session');
			
			saveSessionBtn.addEventListener('click', saveSessionState);
			loadSessionBtn.addEventListener('click', loadSessionState);
			clearSessionBtn.addEventListener('click', clearSessionState);
			
			// Check if there's a saved session on startup
			if (localStorage.getItem('operatorSessionMetadata')) {
				loadSessionBtn.classList.add('pulse');
				
				// Show a notification about the saved session
				const notification = document.createElement('div');
				notification.className = 'notification';
				notification.innerHTML = `
					<div class="notification-content">
						<p>You have a saved workspace. Would you like to restore it?</p>
						<div class="notification-actions">
							<button id="restore-session">Restore</button>
							<button id="dismiss-notification">Dismiss</button>
						</div>
					</div>
				`;
				document.body.appendChild(notification);
				
				document.getElementById('restore-session').addEventListener('click', () => {
					loadSessionState();
					document.body.removeChild(notification);
				});
				
				document.getElementById('dismiss-notification').addEventListener('click', () => {
					document.body.removeChild(notification);
				});
				
				// Auto-hide after 10 seconds
				setTimeout(() => {
					if (document.body.contains(notification)) {
						document.body.removeChild(notification);
					}
				}, 10000);
			}
		}

		/**
		 * Save the current session state to localStorage with encryption
		 */
		function saveSessionState() {
			try {
				// Collect all state
				const sessionData = {
					version: '1.0',
					timestamp: new Date().toISOString(),
					virtualFS: virtualFS,
					database: {
						records: Array.from(database.records.entries())
					},
					memorySlots: memoryManager ? memoryManager.memorySlots : {}
				};
				
				// Convert to JSON and encrypt (simple encryption for demo)
				const jsonData = JSON.stringify(sessionData);
				const encryptedData = encryptData(jsonData);
				
				// Split into chunks if needed (localStorage has size limits)
				const chunks = chunkString(encryptedData, 1024 * 1024); // 1MB chunks
				
				// Store metadata
				localStorage.setItem('operatorSessionMetadata', JSON.stringify({
					version: '1.0',
					timestamp: new Date().toISOString(),
					chunks: chunks.length,
					size: encryptedData.length
				}));
				
				// Store chunks
				chunks.forEach((chunk, index) => {
					localStorage.setItem(`operatorSessionChunk_${index}`, chunk);
				});
				
				// Show success message
				showSuccessMessage('Session saved successfully');
			} catch (error) {
				console.error('Error saving session:', error);
				showError('Failed to save session: ' + error.message);
			}
		}

		/**
		 * Load session state from localStorage
		 */
		function loadSessionState() {
			try {
				// Check if there's a saved session
				const metadataStr = localStorage.getItem('operatorSessionMetadata');
				if (!metadataStr) {
					showError('No saved session found');
					return;
				}
				
				// Parse metadata
				const metadata = JSON.parse(metadataStr);
				
				// Retrieve and combine chunks
				let encryptedData = '';
				for (let i = 0; i < metadata.chunks; i++) {
					const chunk = localStorage.getItem(`operatorSessionChunk_${i}`);
					if (!chunk) {
						throw new Error(`Missing session data chunk ${i}`);
					}
					encryptedData += chunk;
				}
				
				// Decrypt data
				const jsonData = decryptData(encryptedData);
				const sessionData = JSON.parse(jsonData);
				
				// Confirm before loading
				if (!confirm(`Do you want to load the saved session from ${new Date(metadata.timestamp).toLocaleString()}? This will replace your current workspace.`)) {
					return;
				}
				
				// Restore state
				
				// 1. Restore virtual file system
				virtualFS = sessionData.virtualFS;
				
				// 2. Restore database
				database.deleteAll(); // Clear current data
				sessionData.database.records.forEach(([id, record]) => {
					database.records.set(id, record);
				});
				
				// 3. Restore memory slots
				if (memoryManager) {
					memoryManager.memorySlots = sessionData.memorySlots;
				}
				
				// Update all displays
				renderFileTree();
				if (databaseDisplayUpdater) {
					databaseDisplayUpdater.updateDatabaseDisplay();
				}
				updateMemoryDisplay();
				
				// Show success message
				showSuccessMessage('Session loaded successfully');
			} catch (error) {
				console.error('Error loading session:', error);
				showError('Failed to load session: ' + error.message);
			}
		}

		/**
		 * Clear saved session state
		 */
		function clearSessionState() {
			if (confirm('Are you sure you want to delete your saved workspace? This cannot be undone.')) {
				try {
					// Get metadata to find all chunks
					const metadataStr = localStorage.getItem('operatorSessionMetadata');
					if (metadataStr) {
						const metadata = JSON.parse(metadataStr);
						
						// Remove all chunks
						for (let i = 0; i < metadata.chunks; i++) {
							localStorage.removeItem(`operatorSessionChunk_${i}`);
						}
						
						// Remove metadata
						localStorage.removeItem('operatorSessionMetadata');
					}
					
					showSuccessMessage('Saved session data cleared');
				} catch (error) {
					console.error('Error clearing session:', error);
					showError('Failed to clear session: ' + error.message);
				}
			}
		}

		/**
		 * Simple encryption function (for demonstration purposes)
		 * In a production environment, use a proper encryption library
		 */
		function encryptData(data) {
			// Demo encryption - XOR with a key
			const key = 'OPERATOR_SYSTEM_KEY';
			let result = '';
			
			for (let i = 0; i < data.length; i++) {
				const charCode = data.charCodeAt(i) ^ key.charCodeAt(i % key.length);
				result += String.fromCharCode(charCode);
			}
			
			// Convert to base64 for safer storage
			return btoa(result);
		}

		/**
		 * Simple decryption function (for demonstration purposes)
		 */
		function decryptData(encryptedData) {
			// Decode from base64
			const encoded = atob(encryptedData);
			const key = 'OPERATOR_SYSTEM_KEY';
			let result = '';
			
			for (let i = 0; i < encoded.length; i++) {
				const charCode = encoded.charCodeAt(i) ^ key.charCodeAt(i % key.length);
				result += String.fromCharCode(charCode);
			}
			
			return result;
		}

		/**
		 * Split a string into chunks of specified size
		 */
		function chunkString(str, size) {
			const chunks = [];
			for (let i = 0; i < str.length; i += size) {
				chunks.push(str.substring(i, i + size));
			}
			return chunks;
		}

		/**
		 * Show a success message
		 */
		function showSuccessMessage(message) {
			const notification = document.createElement('div');
			notification.className = 'notification success-notification';
			notification.innerHTML = `
				<div class="notification-content">
					<p>${message}</p>
				</div>
			`;
			document.body.appendChild(notification);
			
			// Auto-hide after 3 seconds
			setTimeout(() => {
				if (document.body.contains(notification)) {
					notification.classList.add('fade-out');
					setTimeout(() => {
						if (document.body.contains(notification)) {
							document.body.removeChild(notification);
						}
					}, 300);
				}
			}, 3000);
		}

		// Make sure to call the setup function in the init function
		setupSessionPersistence();
    }

    // Wait for DOM to be fully loaded before initializing
    document.addEventListener('DOMContentLoaded', init);
})();