const MAX_FILE_SIZE = 25 * 1024 * 1024; // 25MB

let accumulatedFiles = [];

function initFileUpload() {
    const fileInput = document.getElementById('file-input');
    const preview = document.getElementById('file-preview');
    const uploadZone = document.getElementById('upload-zone');
    const mainForm = document.getElementById('main-form');
    
    if (!fileInput || !preview || !uploadZone) return;
    
    accumulatedFiles = [];
    
    fileInput.addEventListener('change', function() {
        let hasOversized = false;
        
        Array.from(this.files).forEach((file) => {
            const isDuplicate = accumulatedFiles.some(f => f.name === file.name && f.size === file.size);
            if (isDuplicate) return;
            
            if (file.size > MAX_FILE_SIZE) {
                hasOversized = true;
                addPreviewItem(file, true);
            } else {
                accumulatedFiles.push(file);
                addPreviewItem(file, false);
            }
        });
        
        updateFileInput();
        
        if (hasOversized) {
            alert('Một số file quá lớn (>25MB). Vui lòng giảm kích thước ảnh hoặc chọn file khác.');
        }
    });
    
    uploadZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.classList.add('border-primary', 'bg-primary/5');
    });
    
    uploadZone.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.classList.remove('border-primary', 'bg-primary/5');
    });
    
    uploadZone.addEventListener('drop', function(e) {
        e.preventDefault();
        this.classList.remove('border-primary', 'bg-primary/5');
        
        let hasOversized = false;
        Array.from(e.dataTransfer.files).forEach((file) => {
            const isDuplicate = accumulatedFiles.some(f => f.name === file.name && f.size === file.size);
            if (isDuplicate) return;
            
            if (file.size > MAX_FILE_SIZE) {
                hasOversized = true;
                addPreviewItem(file, true);
            } else {
                accumulatedFiles.push(file);
                addPreviewItem(file, false);
            }
        });
        
        updateFileInput();
        
        if (hasOversized) {
            alert('Một số file quá lớn (>25MB). Vui lòng giảm kích thước ảnh hoặc chọn file khác.');
        }
    });
    
    if (mainForm) {
        mainForm.addEventListener('submit', function(e) {
            for (let i = 0; i < accumulatedFiles.length; i++) {
                if (accumulatedFiles[i].size > MAX_FILE_SIZE) {
                    e.preventDefault();
                    alert('Một số file quá lớn (>25MB). Vui lòng xóa hoặc giảm kích thước ảnh trước khi lưu.');
                    return false;
                }
            }
            return true;
        });
    }
}

function addPreviewItem(file, isOversized) {
    const preview = document.getElementById('file-preview');
    if (!preview) return;
    
    const div = document.createElement('div');
    div.className = 'relative';
    div.setAttribute('data-filename', file.name);
    div.setAttribute('data-filesize', file.size);
    
    if (isOversized) {
        div.innerHTML = `
            <div class="w-full h-32 bg-red-100 rounded-lg flex items-center justify-center">
                <i class="fas fa-exclamation-triangle text-red-500 text-2xl"></i>
            </div>
            <span class="absolute bottom-0 left-0 right-0 bg-red-500 text-white text-xs p-1 text-center rounded-b-lg truncate">${file.name} (quá lớn - ${(file.size/1024/1024).toFixed(1)}MB)</span>
        `;
        preview.appendChild(div);
    } else {
        const reader = new FileReader();
        reader.onload = function(e) {
            div.innerHTML = `
                <img src="${e.target.result}" alt="Preview" class="w-full h-32 object-cover rounded-lg">
                <span class="absolute bottom-0 left-0 right-0 bg-black/50 text-white text-xs p-1 text-center rounded-b-lg truncate">${file.name}</span>
                <button type="button" onclick="removeFile('${file.name}', ${file.size})" class="absolute top-1 right-1 w-6 h-6 bg-red-500 hover:bg-red-600 text-white rounded-full flex items-center justify-center text-sm shadow-lg">
                    <i class="fas fa-times"></i>
                </button>
            `;
            preview.appendChild(div);
        };
        reader.readAsDataURL(file);
    }
}

function removeFile(filename, filesize) {
    accumulatedFiles = accumulatedFiles.filter(f => !(f.name === filename && f.size === filesize));
    
    const preview = document.getElementById('file-preview');
    if (preview) {
        const items = preview.querySelectorAll('[data-filename]');
        items.forEach(item => {
            if (item.getAttribute('data-filename') === filename && 
                parseInt(item.getAttribute('data-filesize')) === filesize) {
                item.remove();
            }
        });
    }
    
    updateFileInput();
}

function updateFileInput() {
    const fileInput = document.getElementById('file-input');
    if (!fileInput) return;
    
    const dt = new DataTransfer();
    accumulatedFiles.forEach(file => {
        dt.items.add(file);
    });
    fileInput.files = dt.files;
}

function clearAllFiles() {
    accumulatedFiles = [];
    const preview = document.getElementById('file-preview');
    if (preview) {
        preview.innerHTML = '';
    }
    updateFileInput();
}

function addImageField() {
    const container = document.getElementById('images-container');
    if (!container) return;
    
    const div = document.createElement('div');
    div.className = 'flex items-center space-x-3 image-row';
    div.innerHTML = `
        <input type="url" name="images[]" class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent" placeholder="https://example.com/image.jpg">
        <button type="button" onclick="this.parentElement.remove()" class="text-red-600 hover:text-red-800 p-2">
            <i class="fas fa-times"></i>
        </button>
    `;
    container.appendChild(div);
}

function addVideoField() {
    const container = document.getElementById('videos-container');
    if (!container) return;
    
    const div = document.createElement('div');
    div.className = 'p-4 bg-gray-50 rounded-lg video-row';
    div.innerHTML = `
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <input type="url" name="video_urls[]" class="px-4 py-2 border border-gray-300 rounded-lg" placeholder="URL embed YouTube">
            <input type="text" name="video_titles_vi[]" class="px-4 py-2 border border-gray-300 rounded-lg" placeholder="Tiêu đề (VI)">
            <div class="flex items-center space-x-2">
                <input type="text" name="video_titles_en[]" class="flex-1 px-4 py-2 border border-gray-300 rounded-lg" placeholder="Tiêu đề (EN)">
                <button type="button" onclick="this.closest('.video-row').remove()" class="text-red-600 p-2"><i class="fas fa-times"></i></button>
            </div>
        </div>
    `;
    container.appendChild(div);
}

document.addEventListener('DOMContentLoaded', initFileUpload);
