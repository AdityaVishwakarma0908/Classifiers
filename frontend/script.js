// --- NAVIGATION LOGIC ---
const navButtons = document.querySelectorAll('.nav-btn');
const views = document.querySelectorAll('.view-section');

navButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all buttons and views
        navButtons.forEach(b => b.classList.remove('active'));
        views.forEach(v => v.classList.remove('active'));

        // Add active class to clicked button
        btn.classList.add('active');

        // Show the corresponding view
        const targetId = btn.getAttribute('data-target');
        document.getElementById(targetId).classList.add('active');
    });
});


// --- DIGIT CLASSIFIER LOGIC ---
const grid = document.getElementById('pixelGrid');
const clearBtn = document.getElementById('clearBtn');
const predictBtn = document.getElementById('predictBtn');
const resultSpan = document.getElementById('predictionResult');

let pixels = new Array(784).fill(0);
let isDrawing = false;

// 1. Generate the 28x28 grid
function createGrid() {
    grid.innerHTML = '';
    for (let i = 0; i < 784; i++) {
        const cell = document.createElement('div');
        cell.classList.add('pixel');
        cell.dataset.index = i;
        
        cell.addEventListener('mousedown', (e) => {
            isDrawing = true;
            paint(parseInt(e.target.dataset.index));
        });
        cell.addEventListener('mouseenter', (e) => {
            if (isDrawing) paint(parseInt(e.target.dataset.index));
        });
        
        grid.appendChild(cell);
    }
}

window.addEventListener('mouseup', () => isDrawing = false);
grid.addEventListener('mouseleave', () => isDrawing = false);

// 2. Paint logic
function paint(index) {
    const row = Math.floor(index / 28);
    const col = index % 28;

    for (let r = -1; r <= 1; r++) {
        for (let c = -1; c <= 1; c++) {
            const newRow = row + r;
            const newCol = col + c;
            
            if (newRow >= 0 && newRow < 28 && newCol >= 0 && newCol < 28) {
                const newIndex = newRow * 28 + newCol;
                
                const isCenter = (r === 0 && c === 0);
                const colorValue = isCenter ? 255 : 128;
                
                if (pixels[newIndex] < colorValue) {
                    pixels[newIndex] = colorValue;
                    const cell = grid.children[newIndex];
                    cell.style.backgroundColor = `rgb(${colorValue}, ${colorValue}, ${colorValue})`;
                }
            }
        }
    }
}

// 3. Clear Canvas
clearBtn.addEventListener('click', () => {
    pixels.fill(0);
    Array.from(grid.children).forEach(cell => {
        cell.style.backgroundColor = 'black';
    });
    resultSpan.innerText = '--';
});

// 4. Send to FastAPI
predictBtn.addEventListener('click', async () => {
    resultSpan.innerText = 'Thinking...';

    try {
        const response = await fetch('http://127.0.0.1:8000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pixels: pixels }) 
        });

        const data = await response.json();

        if (data.success) {
            resultSpan.innerText = data.prediction;
        } else {
            resultSpan.innerText = 'Error';
            console.error(data.error);
        }
    } catch (error) {
        resultSpan.innerText = 'Server Offline';
    }
});

// Initialize on load
createGrid();