class UrbanSoundAnalyzer {
    constructor() {
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const analyzeBtn = document.getElementById('analyzeBtn');
        const batchAnalyzeBtn = document.getElementById('batchAnalyzeBtn');

        uploadArea.addEventListener('click', () => fileInput.click());
        uploadArea.addEventListener('dragover', this.handleDragOver.bind(this));
        uploadArea.addEventListener('drop', this.handleDrop.bind(this));
        
        fileInput.addEventListener('change', this.handleFileSelect.bind(this));
        analyzeBtn.addEventListener('click', this.analyzeAudio.bind(this));
        batchAnalyzeBtn.addEventListener('click', this.analyzeBatch.bind(this));
    }

    handleDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        e.dataTransfer.dropEffect = 'copy';
        e.currentTarget.style.background = '#f8f9fa';
        e.currentTarget.style.borderColor = '#764ba2';
    }

    handleDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        e.currentTarget.style.background = '';
        e.currentTarget.style.borderColor = '#667eea';
        
        const files = e.dataTransfer.files;
        this.handleFiles(files);
    }

    handleFileSelect(e) {
        const files = e.target.files;
        this.handleFiles(files);
    }

    handleFiles(files) {
        const uploadArea = document.getElementById('uploadArea');
        const fileList = document.getElementById('fileList');
        
        fileList.innerHTML = '';
        
        if (files.length > 0) {
            uploadArea.style.borderColor = '#28a745';
            uploadArea.style.background = '#f8fff9';
            
            Array.from(files).forEach(file => {
                const fileItem = document.createElement('div');
                fileItem.className = 'file-item';
                fileItem.innerHTML = `
                    <i class="fas fa-file-audio"></i>
                    <span>${file.name}</span>
                    <small>(${this.formatFileSize(file.size)})</small>
                `;
                fileList.appendChild(fileItem);
            });
        }
    }

    async analyzeAudio() {
        const fileInput = document.getElementById('fileInput');
        const files = fileInput.files;
        
        if (files.length === 0) {
            this.showError('Please select an audio file to analyze');
            return;
        }

        this.showLoading();
        
        const formData = new FormData();
        formData.append('file', files[0]);

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (response.ok) {
                this.displayResults(result);
            } else {
                this.showError(result.error);
            }
        } catch (error) {
            this.showError('Analysis failed: ' + error.message);
        } finally {
            this.hideLoading();
        }
    }

    async analyzeBatch() {
        const fileInput = document.getElementById('fileInput');
        const files = fileInput.files;
        
        if (files.length === 0) {
            this.showError('Please select audio files to analyze');
            return;
        }

        this.showLoading();
        
        const formData = new FormData();
        Array.from(files).forEach(file => {
            formData.append('files', file);
        });

        try {
            const response = await fetch('/api/batch_analyze', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (response.ok) {
                this.displayBatchResults(result);
            } else {
                this.showError(result.error);
            }
        } catch (error) {
            this.showError('Batch analysis failed: ' + error.message);
        } finally {
            this.hideLoading();
        }
    }

    displayResults(result) {
        const resultsContainer = document.getElementById('resultsContainer');
        resultsContainer.innerHTML = this.generateResultsHTML(result);
        resultsContainer.style.display = 'block';
        
        this.scrollToResults();
    }

    displayBatchResults(result) {
        const resultsContainer = document.getElementById('resultsContainer');
        resultsContainer.innerHTML = this.generateBatchResultsHTML(result);
        resultsContainer.style.display = 'block';
        
        this.scrollToResults();
    }

    generateResultsHTML(result) {
        return `
            <div class="results-header">
                <h3>Analysis Results</h3>
                <p>File: ${result.filename}</p>
            </div>
            
            <div class="result-card">
                <h4>Predicted Sound Class</h4>
                <div class="prediction-result">
                    <span class="predicted-class">${result.predicted_class}</span>
                    <span class="confidence">${(result.confidence * 100).toFixed(2)}% confidence</span>
                </div>
            </div>

            <div class="result-card">
                <h4>Class Probabilities</h4>
                ${this.generateProbabilityBars(result.class_probabilities)}
            </div>

            <div class="metrics-grid">
                <div class="metric-card">
                    <h5>Noise Level</h5>
                    <div class="metric-value">${result.noise_analysis.level}</div>
                    <p>${result.noise_analysis.decibels.toFixed(2)} dB</p>
                </div>
                <div class="metric-card">
                    <h5>Spectral Centroid</h5>
                    <div class="metric-value">${result.noise_analysis.spectral_centroid_mean.toFixed(2)}</div>
                    <p>Mean frequency</p>
                </div>
                <div class="metric-card">
                    <h5>Energy</h5>
                    <div class="metric-value">${result.noise_analysis.energy_mean.toFixed(4)}</div>
                    <p>RMS energy</p>
                </div>
            </div>
        `;
    }

    generateBatchResultsHTML(result) {
        return `
            <div class="results-header">
                <h3>Urban Area Analysis</h3>
                <p>Total files analyzed: ${result.total_files}</p>
            </div>

            <div class="result-card">
                <h4>Sound Distribution</h4>
                ${this.generateDistributionChart(result.sound_distribution)}
            </div>

            <div class="result-card">
                <h4>Noise Summary</h4>
                <p>Average Decibels: <strong>${result.average_decibels.toFixed(2)} dB</strong></p>
                <p>Dominant Sounds: ${result.dominant_sounds.map(s => `${s[0]} (${s[1]})`).join(', ')}</p>
            </div>
        `;
    }

    generateProbabilityBars(probabilities) {
        let html = '';
        for (const [className, probability] of Object.entries(probabilities)) {
            const percentage = (probability * 100).toFixed(1);
            html += `
                <div class="probability-item">
                    <div class="class-name">${className}</div>
                    <div class="probability-bar">
                        <div class="probability-fill" style="width: ${percentage}%">
                            ${percentage}%
                        </div>
                    </div>
                </div>
            `;
        }
        return html;
    }

    generateDistributionChart(distribution) {
        let html = '';
        for (const [className, count] of Object.entries(distribution)) {
            html += `
                <div class="distribution-item">
                    <div class="class-name">${className}</div>
                    <div class="count">${count}</div>
                </div>
            `;
        }
        return html;
    }

    showLoading() {
        document.getElementById('loading').style.display = 'block';
    }

    hideLoading() {
        document.getElementById('loading').style.display = 'none';
    }

    showError(message) {
        alert('Error: ' + message);
    }

    scrollToResults() {
        document.getElementById('resultsContainer').scrollIntoView({
            behavior: 'smooth'
        });
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new UrbanSoundAnalyzer();
});