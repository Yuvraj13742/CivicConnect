// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const imagePreview = document.getElementById('imagePreview');
const previewImg = document.getElementById('previewImg');
const fileName = document.getElementById('fileName');
const changeBtn = document.getElementById('changeBtn');
const submitBtn = document.getElementById('submitBtn');
const resultSection = document.getElementById('resultSection');
const resultContent = document.getElementById('resultContent');
const newReportBtn = document.getElementById('newReportBtn');

// Category information
const categoryInfo = {
    'Roads': {
        icon: '🛣️',
        description: 'This appears to be a road-related issue such as potholes, damaged pavement, or road signage problems.',
        action: 'This will be forwarded to the Roads & Transportation Department for assessment and repair.'
    },
    'Water': {
        icon: '💧',
        description: 'This looks like a water-related issue such as leaks, drainage problems, or water quality concerns.',
        action: 'This will be sent to the Water Management Department for immediate attention.'
    },
    'Electricity': {
        icon: '⚡',
        description: 'This appears to be an electrical issue such as power outages, damaged power lines, or streetlight problems.',
        action: 'This will be escalated to the Electrical Services Department for safety assessment and repair.'
    },
    'Waste': {
        icon: '🗑️',
        description: 'This looks like a waste management issue such as overflowing bins or illegal dumping.',
        action: 'This will be reported to the Waste Management Department for cleanup and resolution.'
    },
    'Safety': {
        icon: '⚠️',
        description: 'This appears to be a safety-related issue that could pose risks to public wellbeing.',
        action: 'This will be immediately forwarded to the Public Safety Department for urgent attention.'
    },
    'Other': {
        icon: '📋',
        description: 'This appears to be a general municipal issue that doesn\'t fit into specific categories.',
        action: 'This will be reviewed by the General Services Department for appropriate action.'
    }
};

let selectedFile = null;

// Event Listeners
uploadArea.addEventListener('click', () => fileInput.click());
uploadArea.addEventListener('dragover', handleDragOver);
uploadArea.addEventListener('dragleave', handleDragLeave);
uploadArea.addEventListener('drop', handleDrop);
fileInput.addEventListener('change', handleFileSelect);
browseBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    fileInput.click();
});
changeBtn.addEventListener('click', () => {
    resetUpload();
});
submitBtn.addEventListener('click', handleSubmit);
newReportBtn.addEventListener('click', resetUpload);

// Drag and Drop Handlers
function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

// File Selection Handler
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

// File Processing
function handleFile(file) {
    // Validate file type
    if (!file.type.startsWith('image/')) {
        showError('Please select an image file (JPG, PNG, GIF).');
        return;
    }

    // Validate file size (10MB limit)
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
        showError('File size must be less than 10MB.');
        return;
    }

    selectedFile = file;
    displayImagePreview(file);
    hideError();
}

// Display Image Preview
function displayImagePreview(file) {
    const reader = new FileReader();
    
    reader.onload = (e) => {
        previewImg.src = e.target.result;
        fileName.textContent = `File: ${file.name} (${formatFileSize(file.size)})`;
        
        uploadArea.style.display = 'none';
        imagePreview.style.display = 'block';
        submitBtn.disabled = false;
    };
    
    reader.readAsDataURL(file);
}

// Format File Size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Submit Handler
async function handleSubmit() {
    if (!selectedFile) {
        showError('Please select an image first.');
        return;
    }

    setLoading(true);
    hideError();

    try {
        const formData = new FormData();
        formData.append('file', selectedFile);

        const response = await fetch('/api/predict', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            displayResult(result);
        } else {
            showError(result.error || 'An error occurred while analyzing the image.');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Unable to connect to the service. Please check if the ML model server is running.');
    } finally {
        setLoading(false);
    }
}

// Display Result
function displayResult(result) {
    const category = result.predicted_category;
    const info = categoryInfo[category] || categoryInfo['Other'];
    
    resultContent.innerHTML = `
        <div class="result-category">
            ${info.icon} ${category}
        </div>
        <div class="result-filename">
            File: ${result.filename}
        </div>
        <div class="result-description">
            <h4>Issue Assessment</h4>
            <p>${info.description}</p>
        </div>
        <div class="result-description">
            <h4>Next Steps</h4>
            <p>${info.action}</p>
        </div>
    `;
    
    resultSection.style.display = 'block';
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

// Loading State
function setLoading(loading) {
    const btnText = submitBtn.querySelector('.btn-text');
    const spinner = submitBtn.querySelector('.loading-spinner');
    
    if (loading) {
        btnText.textContent = 'Analyzing...';
        spinner.style.display = 'inline';
        submitBtn.disabled = true;
    } else {
        btnText.textContent = 'Analyze Issue';
        spinner.style.display = 'none';
        submitBtn.disabled = false;
    }
}

// Reset Upload
function resetUpload() {
    selectedFile = null;
    fileInput.value = '';
    uploadArea.style.display = 'block';
    imagePreview.style.display = 'none';
    resultSection.style.display = 'none';
    submitBtn.disabled = true;
    hideError();
    
    // Scroll to top
    document.querySelector('.hero').scrollIntoView({ behavior: 'smooth' });
}

// Error Handling
function showError(message) {
    hideError();
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    const uploadCard = document.querySelector('.upload-card');
    uploadCard.insertBefore(errorDiv, uploadCard.firstChild);
}

function hideError() {
    const existingError = document.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('CivicConnect Frontend Initialized');
    
    // Check if backend is running
    fetch('/api/health')
        .then(response => response.json())
        .then(data => {
            console.log('Backend status:', data.message);
        })
        .catch(error => {
            console.warn('Backend connection check failed:', error);
        });
});