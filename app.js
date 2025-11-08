// ============================================
// CLASSES POUR LES ÉLÉMENTS
// ============================================

class CanvasElement {
    constructor(x, y, width, height, type) {
        this.id = Date.now() + Math.random();
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.type = type;
        this.rotation = 0;
        this.opacity = 1;
        this.fillColor = '#3b82f6';
        this.strokeColor = '#000000';
        this.strokeWidth = 2;
    }

    draw(ctx) {
        ctx.save();
        ctx.globalAlpha = this.opacity;
        ctx.translate(this.x + this.width / 2, this.y + this.height / 2);
        ctx.rotate((this.rotation * Math.PI) / 180);
        ctx.translate(-(this.x + this.width / 2), -(this.y + this.height / 2));

        this.drawShape(ctx);

        ctx.restore();
    }

    drawShape(ctx) {
        // À surcharger dans les sous-classes
    }

    contains(px, py) {
        // Vérification simple de rectangle
        return (
            px >= this.x &&
            px <= this.x + this.width &&
            py >= this.y &&
            py <= this.y + this.height
        );
    }

    toJSON() {
        return {
            id: this.id,
            x: this.x,
            y: this.y,
            width: this.width,
            height: this.height,
            type: this.type,
            rotation: this.rotation,
            opacity: this.opacity,
            fillColor: this.fillColor,
            strokeColor: this.strokeColor,
            strokeWidth: this.strokeWidth
        };
    }
}

class Rectangle extends CanvasElement {
    constructor(x, y, width, height) {
        super(x, y, width, height, 'rectangle');
    }

    drawShape(ctx) {
        ctx.fillStyle = this.fillColor;
        ctx.fillRect(this.x, this.y, this.width, this.height);

        if (this.strokeWidth > 0) {
            ctx.strokeStyle = this.strokeColor;
            ctx.lineWidth = this.strokeWidth;
            ctx.strokeRect(this.x, this.y, this.width, this.height);
        }
    }
}

class Circle extends CanvasElement {
    constructor(x, y, radius) {
        super(x, y, radius * 2, radius * 2, 'circle');
        this.radius = radius;
    }

    drawShape(ctx) {
        const centerX = this.x + this.width / 2;
        const centerY = this.y + this.height / 2;

        ctx.beginPath();
        ctx.arc(centerX, centerY, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.fillColor;
        ctx.fill();

        if (this.strokeWidth > 0) {
            ctx.strokeStyle = this.strokeColor;
            ctx.lineWidth = this.strokeWidth;
            ctx.stroke();
        }
    }

    toJSON() {
        return {
            ...super.toJSON(),
            radius: this.radius
        };
    }
}

class Triangle extends CanvasElement {
    constructor(x, y, width, height) {
        super(x, y, width, height, 'triangle');
    }

    drawShape(ctx) {
        ctx.beginPath();
        ctx.moveTo(this.x + this.width / 2, this.y);
        ctx.lineTo(this.x + this.width, this.y + this.height);
        ctx.lineTo(this.x, this.y + this.height);
        ctx.closePath();

        ctx.fillStyle = this.fillColor;
        ctx.fill();

        if (this.strokeWidth > 0) {
            ctx.strokeStyle = this.strokeColor;
            ctx.lineWidth = this.strokeWidth;
            ctx.stroke();
        }
    }
}

class Line extends CanvasElement {
    constructor(x1, y1, x2, y2) {
        super(
            Math.min(x1, x2),
            Math.min(y1, y2),
            Math.abs(x2 - x1),
            Math.abs(y2 - y1),
            'line'
        );
        this.x1 = x1;
        this.y1 = y1;
        this.x2 = x2;
        this.y2 = y2;
    }

    drawShape(ctx) {
        ctx.beginPath();
        ctx.moveTo(this.x1, this.y1);
        ctx.lineTo(this.x2, this.y2);
        ctx.strokeStyle = this.strokeColor;
        ctx.lineWidth = this.strokeWidth;
        ctx.stroke();
    }

    toJSON() {
        return {
            ...super.toJSON(),
            x1: this.x1,
            y1: this.y1,
            x2: this.x2,
            y2: this.y2
        };
    }
}

class TextElement extends CanvasElement {
    constructor(x, y, text = 'Texte') {
        super(x, y, 200, 50, 'text');
        this.text = text;
        this.fontSize = 24;
        this.fontFamily = 'Arial';
        this.bold = false;
        this.italic = false;
        this.underline = false;
    }

    drawShape(ctx) {
        let fontStyle = '';
        if (this.italic) fontStyle += 'italic ';
        if (this.bold) fontStyle += 'bold ';
        ctx.font = `${fontStyle}${this.fontSize}px ${this.fontFamily}`;
        ctx.fillStyle = this.fillColor;

        const lines = this.text.split('\n');
        lines.forEach((line, i) => {
            ctx.fillText(line, this.x, this.y + this.fontSize + (i * this.fontSize * 1.2));

            if (this.underline) {
                const textWidth = ctx.measureText(line).width;
                ctx.beginPath();
                ctx.moveTo(this.x, this.y + this.fontSize + 2 + (i * this.fontSize * 1.2));
                ctx.lineTo(this.x + textWidth, this.y + this.fontSize + 2 + (i * this.fontSize * 1.2));
                ctx.strokeStyle = this.fillColor;
                ctx.lineWidth = 1;
                ctx.stroke();
            }
        });
    }

    toJSON() {
        return {
            ...super.toJSON(),
            text: this.text,
            fontSize: this.fontSize,
            fontFamily: this.fontFamily,
            bold: this.bold,
            italic: this.italic,
            underline: this.underline
        };
    }
}

class ImageElement extends CanvasElement {
    constructor(x, y, width, height, imageData) {
        super(x, y, width, height, 'image');
        this.imageData = imageData;
        this.image = new Image();
        this.image.src = imageData;
    }

    drawShape(ctx) {
        if (this.image.complete) {
            ctx.drawImage(this.image, this.x, this.y, this.width, this.height);
        }
    }

    toJSON() {
        return {
            ...super.toJSON(),
            imageData: this.imageData
        };
    }
}

// ============================================
// APPLICATION PRINCIPALE
// ============================================

class CanvasApp {
    constructor() {
        this.canvas = document.getElementById('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.elements = [];
        this.selectedElement = null;
        this.currentTool = 'select';
        this.isDrawing = false;
        this.isDragging = false;
        this.isResizing = false;
        this.dragStartX = 0;
        this.dragStartY = 0;
        this.history = [];
        this.historyIndex = -1;

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.render();
    }

    setupEventListeners() {
        // Canvas events
        this.canvas.addEventListener('mousedown', this.handleMouseDown.bind(this));
        this.canvas.addEventListener('mousemove', this.handleMouseMove.bind(this));
        this.canvas.addEventListener('mouseup', this.handleMouseUp.bind(this));

        // Tool buttons
        document.querySelectorAll('.tool-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.tool-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.currentTool = btn.dataset.tool;

                if (this.currentTool === 'image') {
                    document.getElementById('imageInput').click();
                }
            });
        });

        // Image upload
        document.getElementById('imageInput').addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    const img = new Image();
                    img.onload = () => {
                        const maxWidth = 400;
                        const maxHeight = 400;
                        let width = img.width;
                        let height = img.height;

                        if (width > maxWidth || height > maxHeight) {
                            const ratio = Math.min(maxWidth / width, maxHeight / height);
                            width *= ratio;
                            height *= ratio;
                        }

                        const imageElement = new ImageElement(100, 100, width, height, event.target.result);
                        this.addElement(imageElement);
                    };
                    img.src = event.target.result;
                };
                reader.readAsDataURL(file);
            }
        });

        // Property inputs
        this.setupPropertyListeners();

        // Header buttons
        document.getElementById('undoBtn').addEventListener('click', () => this.undo());
        document.getElementById('redoBtn').addEventListener('click', () => this.redo());
        document.getElementById('downloadPngBtn').addEventListener('click', () => this.exportPNG());
        document.getElementById('downloadJsonBtn').addEventListener('click', () => this.exportJSON());
        document.getElementById('uploadJsonLabel').addEventListener('click', () => {
            document.getElementById('uploadJsonBtn').click();
        });
        document.getElementById('uploadJsonBtn').addEventListener('change', (e) => this.importJSON(e));

        // Delete and duplicate buttons
        document.getElementById('deleteBtn').addEventListener('click', () => this.deleteSelected());
        document.getElementById('duplicateBtn').addEventListener('click', () => this.duplicateSelected());

        // Layer order buttons
        document.getElementById('bringToFrontBtn').addEventListener('click', () => this.bringToFront());
        document.getElementById('sendToBackBtn').addEventListener('click', () => this.sendToBack());

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Delete' || e.key === 'Backspace') {
                if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
                    e.preventDefault();
                    this.deleteSelected();
                }
            }
            if (e.ctrlKey || e.metaKey) {
                if (e.key === 'z') {
                    e.preventDefault();
                    this.undo();
                }
                if (e.key === 'y') {
                    e.preventDefault();
                    this.redo();
                }
                if (e.key === 'd') {
                    e.preventDefault();
                    this.duplicateSelected();
                }
            }
        });
    }

    setupPropertyListeners() {
        const propX = document.getElementById('propX');
        const propY = document.getElementById('propY');
        const propWidth = document.getElementById('propWidth');
        const propHeight = document.getElementById('propHeight');
        const propRotation = document.getElementById('propRotation');
        const propOpacity = document.getElementById('propOpacity');
        const propFillColor = document.getElementById('propFillColor');
        const propStrokeColor = document.getElementById('propStrokeColor');
        const propStrokeWidth = document.getElementById('propStrokeWidth');
        const propText = document.getElementById('propText');
        const propFontSize = document.getElementById('propFontSize');
        const propFontFamily = document.getElementById('propFontFamily');
        const propBold = document.getElementById('propBold');
        const propItalic = document.getElementById('propItalic');
        const propUnderline = document.getElementById('propUnderline');

        propX.addEventListener('input', () => {
            if (this.selectedElement) {
                this.selectedElement.x = parseFloat(propX.value);
                this.render();
                this.saveState();
            }
        });

        propY.addEventListener('input', () => {
            if (this.selectedElement) {
                this.selectedElement.y = parseFloat(propY.value);
                this.render();
                this.saveState();
            }
        });

        propWidth.addEventListener('input', () => {
            if (this.selectedElement) {
                this.selectedElement.width = parseFloat(propWidth.value);
                if (this.selectedElement.type === 'circle') {
                    this.selectedElement.radius = this.selectedElement.width / 2;
                    this.selectedElement.height = this.selectedElement.width;
                }
                this.render();
                this.saveState();
            }
        });

        propHeight.addEventListener('input', () => {
            if (this.selectedElement && this.selectedElement.type !== 'circle') {
                this.selectedElement.height = parseFloat(propHeight.value);
                this.render();
                this.saveState();
            }
        });

        propRotation.addEventListener('input', () => {
            if (this.selectedElement) {
                this.selectedElement.rotation = parseFloat(propRotation.value);
                document.getElementById('rotationValue').textContent = propRotation.value + '°';
                this.render();
                this.saveState();
            }
        });

        propOpacity.addEventListener('input', () => {
            if (this.selectedElement) {
                this.selectedElement.opacity = parseFloat(propOpacity.value) / 100;
                document.getElementById('opacityValue').textContent = propOpacity.value + '%';
                this.render();
                this.saveState();
            }
        });

        propFillColor.addEventListener('input', () => {
            if (this.selectedElement) {
                this.selectedElement.fillColor = propFillColor.value;
                this.render();
                this.saveState();
            }
        });

        propStrokeColor.addEventListener('input', () => {
            if (this.selectedElement) {
                this.selectedElement.strokeColor = propStrokeColor.value;
                this.render();
                this.saveState();
            }
        });

        propStrokeWidth.addEventListener('input', () => {
            if (this.selectedElement) {
                this.selectedElement.strokeWidth = parseFloat(propStrokeWidth.value);
                document.getElementById('strokeWidthValue').textContent = propStrokeWidth.value + 'px';
                this.render();
                this.saveState();
            }
        });

        propText.addEventListener('input', () => {
            if (this.selectedElement && this.selectedElement.type === 'text') {
                this.selectedElement.text = propText.value;
                this.render();
                this.saveState();
            }
        });

        propFontSize.addEventListener('input', () => {
            if (this.selectedElement && this.selectedElement.type === 'text') {
                this.selectedElement.fontSize = parseFloat(propFontSize.value);
                this.render();
                this.saveState();
            }
        });

        propFontFamily.addEventListener('change', () => {
            if (this.selectedElement && this.selectedElement.type === 'text') {
                this.selectedElement.fontFamily = propFontFamily.value;
                this.render();
                this.saveState();
            }
        });

        propBold.addEventListener('click', () => {
            if (this.selectedElement && this.selectedElement.type === 'text') {
                this.selectedElement.bold = !this.selectedElement.bold;
                propBold.classList.toggle('active');
                this.render();
                this.saveState();
            }
        });

        propItalic.addEventListener('click', () => {
            if (this.selectedElement && this.selectedElement.type === 'text') {
                this.selectedElement.italic = !this.selectedElement.italic;
                propItalic.classList.toggle('active');
                this.render();
                this.saveState();
            }
        });

        propUnderline.addEventListener('click', () => {
            if (this.selectedElement && this.selectedElement.type === 'text') {
                this.selectedElement.underline = !this.selectedElement.underline;
                propUnderline.classList.toggle('active');
                this.render();
                this.saveState();
            }
        });
    }

    handleMouseDown(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        if (this.currentTool === 'select') {
            // Trouver l'élément cliqué
            const clickedElement = this.findElementAt(x, y);

            if (clickedElement) {
                this.selectElement(clickedElement);
                this.isDragging = true;
                this.dragStartX = x - clickedElement.x;
                this.dragStartY = y - clickedElement.y;
            } else {
                this.selectElement(null);
            }
        } else {
            this.isDrawing = true;
            this.dragStartX = x;
            this.dragStartY = y;
        }
    }

    handleMouseMove(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        if (this.isDragging && this.selectedElement) {
            this.selectedElement.x = x - this.dragStartX;
            this.selectedElement.y = y - this.dragStartY;
            this.updatePropertiesPanel();
            this.render();
        }
    }

    handleMouseUp(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        if (this.isDrawing) {
            this.createShape(this.dragStartX, this.dragStartY, x, y);
            this.isDrawing = false;
        }

        if (this.isDragging) {
            this.saveState();
            this.isDragging = false;
        }
    }

    createShape(startX, startY, endX, endY) {
        const width = Math.abs(endX - startX);
        const height = Math.abs(endY - startY);
        const x = Math.min(startX, endX);
        const y = Math.min(startY, endY);

        let element;

        switch (this.currentTool) {
            case 'rectangle':
                if (width > 5 && height > 5) {
                    element = new Rectangle(x, y, width, height);
                }
                break;
            case 'circle':
                if (width > 5) {
                    const radius = Math.max(width, height) / 2;
                    element = new Circle(x, y, radius);
                }
                break;
            case 'triangle':
                if (width > 5 && height > 5) {
                    element = new Triangle(x, y, width, height);
                }
                break;
            case 'line':
                if (width > 5 || height > 5) {
                    element = new Line(startX, startY, endX, endY);
                }
                break;
            case 'text':
                element = new TextElement(x, y);
                break;
        }

        if (element) {
            this.addElement(element);
        }
    }

    addElement(element) {
        this.elements.push(element);
        this.selectElement(element);
        this.saveState();
        this.render();
    }

    findElementAt(x, y) {
        // Recherche en ordre inverse pour sélectionner l'élément le plus au-dessus
        for (let i = this.elements.length - 1; i >= 0; i--) {
            if (this.elements[i].contains(x, y)) {
                return this.elements[i];
            }
        }
        return null;
    }

    selectElement(element) {
        this.selectedElement = element;
        this.updatePropertiesPanel();
        this.render();
    }

    updatePropertiesPanel() {
        const noSelection = document.getElementById('noSelection');
        const propertiesContent = document.getElementById('propertiesContent');
        const textGroup = document.getElementById('textGroup');

        if (!this.selectedElement) {
            noSelection.style.display = 'block';
            propertiesContent.style.display = 'none';
            return;
        }

        noSelection.style.display = 'none';
        propertiesContent.style.display = 'flex';

        // Mettre à jour les valeurs
        document.getElementById('propX').value = Math.round(this.selectedElement.x);
        document.getElementById('propY').value = Math.round(this.selectedElement.y);
        document.getElementById('propWidth').value = Math.round(this.selectedElement.width);
        document.getElementById('propHeight').value = Math.round(this.selectedElement.height);
        document.getElementById('propRotation').value = this.selectedElement.rotation;
        document.getElementById('rotationValue').textContent = this.selectedElement.rotation + '°';
        document.getElementById('propOpacity').value = Math.round(this.selectedElement.opacity * 100);
        document.getElementById('opacityValue').textContent = Math.round(this.selectedElement.opacity * 100) + '%';
        document.getElementById('propFillColor').value = this.selectedElement.fillColor;
        document.getElementById('propStrokeColor').value = this.selectedElement.strokeColor;
        document.getElementById('propStrokeWidth').value = this.selectedElement.strokeWidth;
        document.getElementById('strokeWidthValue').textContent = this.selectedElement.strokeWidth + 'px';

        // Afficher/masquer les propriétés de texte
        if (this.selectedElement.type === 'text') {
            textGroup.style.display = 'flex';
            document.getElementById('propText').value = this.selectedElement.text;
            document.getElementById('propFontSize').value = this.selectedElement.fontSize;
            document.getElementById('propFontFamily').value = this.selectedElement.fontFamily;

            document.getElementById('propBold').classList.toggle('active', this.selectedElement.bold);
            document.getElementById('propItalic').classList.toggle('active', this.selectedElement.italic);
            document.getElementById('propUnderline').classList.toggle('active', this.selectedElement.underline);
        } else {
            textGroup.style.display = 'none';
        }
    }

    deleteSelected() {
        if (this.selectedElement) {
            const index = this.elements.indexOf(this.selectedElement);
            if (index > -1) {
                this.elements.splice(index, 1);
                this.selectedElement = null;
                this.updatePropertiesPanel();
                this.saveState();
                this.render();
            }
        }
    }

    duplicateSelected() {
        if (this.selectedElement) {
            const json = this.selectedElement.toJSON();
            const newElement = this.createElementFromJSON({
                ...json,
                x: json.x + 20,
                y: json.y + 20,
                id: Date.now() + Math.random()
            });
            this.addElement(newElement);
        }
    }

    bringToFront() {
        if (this.selectedElement) {
            const index = this.elements.indexOf(this.selectedElement);
            if (index > -1) {
                this.elements.splice(index, 1);
                this.elements.push(this.selectedElement);
                this.saveState();
                this.render();
            }
        }
    }

    sendToBack() {
        if (this.selectedElement) {
            const index = this.elements.indexOf(this.selectedElement);
            if (index > -1) {
                this.elements.splice(index, 1);
                this.elements.unshift(this.selectedElement);
                this.saveState();
                this.render();
            }
        }
    }

    render() {
        // Effacer le canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Dessiner tous les éléments
        this.elements.forEach(element => {
            element.draw(this.ctx);
        });

        // Dessiner le rectangle de sélection
        if (this.selectedElement) {
            this.drawSelectionBox(this.selectedElement);
        }
    }

    drawSelectionBox(element) {
        this.ctx.save();
        this.ctx.strokeStyle = '#667eea';
        this.ctx.lineWidth = 2;
        this.ctx.setLineDash([5, 5]);
        this.ctx.strokeRect(element.x - 5, element.y - 5, element.width + 10, element.height + 10);

        // Dessiner les poignées de redimensionnement
        const handles = [
            { x: element.x - 5, y: element.y - 5 }, // top-left
            { x: element.x + element.width + 5, y: element.y - 5 }, // top-right
            { x: element.x - 5, y: element.y + element.height + 5 }, // bottom-left
            { x: element.x + element.width + 5, y: element.y + element.height + 5 }, // bottom-right
        ];

        this.ctx.fillStyle = '#667eea';
        handles.forEach(handle => {
            this.ctx.fillRect(handle.x - 4, handle.y - 4, 8, 8);
        });

        this.ctx.restore();
    }

    saveState() {
        const state = JSON.stringify(this.elements.map(e => e.toJSON()));

        // Supprimer les états futurs si on est au milieu de l'historique
        this.history = this.history.slice(0, this.historyIndex + 1);

        this.history.push(state);
        this.historyIndex++;

        // Limiter l'historique à 50 états
        if (this.history.length > 50) {
            this.history.shift();
            this.historyIndex--;
        }

        this.updateUndoRedoButtons();
    }

    undo() {
        if (this.historyIndex > 0) {
            this.historyIndex--;
            this.loadState(this.history[this.historyIndex]);
            this.updateUndoRedoButtons();
        }
    }

    redo() {
        if (this.historyIndex < this.history.length - 1) {
            this.historyIndex++;
            this.loadState(this.history[this.historyIndex]);
            this.updateUndoRedoButtons();
        }
    }

    updateUndoRedoButtons() {
        document.getElementById('undoBtn').disabled = this.historyIndex <= 0;
        document.getElementById('redoBtn').disabled = this.historyIndex >= this.history.length - 1;
    }

    loadState(stateJSON) {
        const state = JSON.parse(stateJSON);
        this.elements = state.map(json => this.createElementFromJSON(json));
        this.selectedElement = null;
        this.updatePropertiesPanel();
        this.render();
    }

    createElementFromJSON(json) {
        let element;

        switch (json.type) {
            case 'rectangle':
                element = new Rectangle(json.x, json.y, json.width, json.height);
                break;
            case 'circle':
                element = new Circle(json.x, json.y, json.radius);
                break;
            case 'triangle':
                element = new Triangle(json.x, json.y, json.width, json.height);
                break;
            case 'line':
                element = new Line(json.x1, json.y1, json.x2, json.y2);
                break;
            case 'text':
                element = new TextElement(json.x, json.y, json.text);
                element.fontSize = json.fontSize;
                element.fontFamily = json.fontFamily;
                element.bold = json.bold;
                element.italic = json.italic;
                element.underline = json.underline;
                break;
            case 'image':
                element = new ImageElement(json.x, json.y, json.width, json.height, json.imageData);
                break;
        }

        if (element) {
            element.id = json.id;
            element.rotation = json.rotation;
            element.opacity = json.opacity;
            element.fillColor = json.fillColor;
            element.strokeColor = json.strokeColor;
            element.strokeWidth = json.strokeWidth;
        }

        return element;
    }

    exportPNG() {
        // Créer un canvas temporaire avec fond blanc
        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = this.canvas.width;
        tempCanvas.height = this.canvas.height;
        const tempCtx = tempCanvas.getContext('2d');

        // Remplir avec du blanc
        tempCtx.fillStyle = '#ffffff';
        tempCtx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);

        // Dessiner tous les éléments
        this.elements.forEach(element => {
            element.draw(tempCtx);
        });

        // Télécharger
        const link = document.createElement('a');
        link.download = 'descary-design.png';
        link.href = tempCanvas.toDataURL();
        link.click();
    }

    exportJSON() {
        const data = {
            version: '1.0',
            canvasWidth: this.canvas.width,
            canvasHeight: this.canvas.height,
            elements: this.elements.map(e => e.toJSON())
        };

        const json = JSON.stringify(data, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);

        const link = document.createElement('a');
        link.download = 'descary-design.json';
        link.href = url;
        link.click();

        URL.revokeObjectURL(url);
    }

    importJSON(e) {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (event) => {
            try {
                const data = JSON.parse(event.target.result);

                if (data.canvasWidth && data.canvasHeight) {
                    this.canvas.width = data.canvasWidth;
                    this.canvas.height = data.canvasHeight;
                }

                this.elements = data.elements.map(json => this.createElementFromJSON(json));
                this.selectedElement = null;
                this.updatePropertiesPanel();
                this.saveState();
                this.render();
            } catch (error) {
                alert('Erreur lors de l\'importation du fichier JSON');
                console.error(error);
            }
        };
        reader.readAsText(file);

        // Reset input
        e.target.value = '';
    }
}

// ============================================
// INITIALISATION
// ============================================

let app;

document.addEventListener('DOMContentLoaded', () => {
    app = new CanvasApp();
});
