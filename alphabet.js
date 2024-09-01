let colorSequence = [];

function hexToID(hex) {
    return parseInt(hex.replace('#', ''), 16) + 1;
}

function idToHex(id) {
    let hex = (id - 1).toString(16).padStart(6, '0');
    return `#${hex}`;
}

function calculateCompoundedGridID(colorSequence) {
    const concatenatedIDString = colorSequence.map(color => hexToID(color)).join('');
    const compoundedID = BigInt(concatenatedIDString);
    return compoundedID;
}

function calculateGridDimensions(numTiles) {
    const sideLength = Math.ceil(Math.sqrt(numTiles));
    return { rows: sideLength, cols: sideLength };
}

function updateGrid() {
    const tileColor = document.getElementById('tile-color').value;
    const tileSize = parseInt(document.getElementById('tile-size').value);

    if (isNaN(tileSize) || tileSize <= 0) {
        alert("Please enter a valid number for tile size.");
        return;
    }

    const gridContainer = document.getElementById('grid-container');
    gridContainer.innerHTML = ''; 
    colorSequence = []; 

    const numTiles = 1; // Start with a single tile
    const { rows, cols } = calculateGridDimensions(numTiles);

    gridContainer.style.gridTemplateRows = `repeat(${rows}, ${tileSize}px)`;
    gridContainer.style.gridTemplateColumns = `repeat(${cols}, ${tileSize}px)`;

    for (let i = 0; i < rows * cols; i++) {
        const tile = document.createElement('div');
        tile.className = 'tile';
        tile.style.backgroundColor = tileColor;
        tile.style.width = `${tileSize}px`;
        tile.style.height = `${tileSize}px`;
        colorSequence.push(tileColor); // Add the initial color to the colorSequence array

        tile.addEventListener('click', () => {
            const newColor = prompt("Enter new hex color (e.g., #00ff00):", tile.style.backgroundColor);
            if (newColor) {
                tile.style.backgroundColor = newColor;
                colorSequence[i] = newColor; // Update the specific color in the array
                updateColorList(); // Reflect the update in the list and compounded ID
            }
        });
        gridContainer.appendChild(tile);
    }

    updateColorList(); // Reflect the grid update in the color list and compounded ID
}

function updateColorList() {
    const colorList = document.getElementById('color-list');
    colorList.innerHTML = ''; 
    colorSequence.forEach((color, index) => {
        const listItem = document.createElement('li');
        listItem.textContent = `ID ${hexToID(color)}: ${color}`;
        colorList.appendChild(listItem);
    });

    const compoundedGridID = calculateCompoundedGridID(colorSequence);
    const gridIdElement = document.getElementById('grid-id');
    gridIdElement.textContent = `Compounded Grid ID: ${compoundedGridID}`;
}

function regenerateGrid(colorSequenceFromID) {
    const tileSize = parseInt(document.getElementById('tile-size').value);
    if (isNaN(tileSize) || tileSize <= 0) {
        alert("Please enter a valid number for tile size.");
        return;
    }

    const numTiles = colorSequenceFromID.length;
    const { rows, cols } = calculateGridDimensions(numTiles);

    const gridContainer = document.getElementById('grid-container');
    gridContainer.innerHTML = ''; 

    gridContainer.style.gridTemplateRows = `repeat(${rows}, ${tileSize}px)`;
    gridContainer.style.gridTemplateColumns = `repeat(${cols}, ${tileSize}px)`;

    colorSequence = colorSequenceFromID; // Update colorSequence array

    colorSequence.forEach((color, i) => {
        const tile = document.createElement('div');
        tile.className = 'tile';
        tile.style.backgroundColor = color;
        tile.style.width = `${tileSize}px`;
        tile.style.height = `${tileSize}px`;

        tile.addEventListener('click', () => {
            const newColor = prompt("Enter new hex color (e.g., #00ff00):", tile.style.backgroundColor);
            if (newColor) {
                tile.style.backgroundColor = newColor;
                colorSequence[i] = newColor; // Update colorSequence array
                updateColorList(); // Reflect the update in the list and compounded ID
            }
        });
        gridContainer.appendChild(tile);
    });

    updateColorList(); // Reflect the grid update in the color list and compounded ID
}

document.getElementById('update-grid').addEventListener('click', updateGrid);

document.getElementById('download-colors').addEventListener('click', function() {
    const compoundedGridID = calculateCompoundedGridID(colorSequence);
    const fileContent = colorSequence.map((color, index) => `ID ${hexToID(color)}: ${color}`).join('\n');
    const fullContent = `Compounded Grid ID: ${compoundedGridID}\n\n${fileContent}`;
    const blob = new Blob([fullContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'color_sequence.txt';
    a.click();

    URL.revokeObjectURL(url);
});

document.getElementById('generate-grid-by-id').addEventListener('click', function() {
    const compoundedIDString = document.getElementById('compounded-id-input').value;
    
    const tileIDs = compoundedIDString.match(/\d{1,7}/g); // Assuming IDs are up to 7 digits long
    if (!tileIDs) {
        alert('Invalid Compounded Grid ID.');
        return;
    }

    const colorSequenceFromID = tileIDs.map(id => idToHex(parseInt(id)));
    regenerateGrid(colorSequenceFromID);
});
