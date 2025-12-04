const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB

function initFileUpload() {
    const fileInput = document.getElementById('file-input');
    const preview = document.getElementById('file-preview');
    const uploadZone = document.getElementById('upload-zone');
    const mainForm = document.getElementById('main-form');
    
    if (!fileInput || !preview || !uploadZone) return;
    
    fileInput.addEventListener('change', function() {
        preview.innerHTML = '';
        let hasOversized = false;
        
        Array.from(this.files).forEach((file) => {
            if (file.size > MAX_FILE_SIZE) {
                hasOversized = true;
                const div = document.createElement('div');
                div.className = 'relative';
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
                    const div = document.createElement('div');
                    div.className = 'relative';
                    div.innerHTML = `
                        <img src="${e.target.result}" alt="Preview" class="w-full h-32 object-cover rounded-lg">
                        <span class="absolute bottom-0 left-0 right-0 bg-black/50 text-white text-xs p-1 text-center rounded-b-lg truncate">${file.name}</span>
                    `;
                    preview.appendChild(div);
                };
                reader.readAsDataURL(file);
            }
        });
        
        if (hasOversized) {
            alert('Một số file quá lớn (>5MB). Vui lòng giảm kích thước ảnh hoặc chọn file khác.');
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
        fileInput.files = e.dataTransfer.files;
        fileInput.dispatchEvent(new Event('change'));
    });
    
    if (mainForm) {
        mainForm.addEventListener('submit', function(e) {
            const files = fileInput.files;
            for (let i = 0; i < files.length; i++) {
                if (files[i].size > MAX_FILE_SIZE) {
                    e.preventDefault();
                    alert('Một số file quá lớn (>5MB). Vui lòng xóa hoặc giảm kích thước ảnh trước khi lưu.');
                    return false;
                }
            }
            return true;
        });
    }
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
