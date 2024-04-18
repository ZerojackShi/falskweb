document.addEventListener('DOMContentLoaded', function() {
    const fileList = document.getElementById('file-list');
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input-drop');
    
    dropZone.addEventListener('dragover', function(event) {
        event.preventDefault();
        dropZone.classList.add('highlight');
    });

    // Remove highlight when dragging leaves drop zone
    dropZone.addEventListener('dragleave', function(event) {
        event.preventDefault();
        dropZone.classList.remove('highlight');
    });

    // Handle dropped files
    dropZone.addEventListener('drop', function(event) {
        event.preventDefault();
        dropZone.classList.remove('highlight');
        const files = event.dataTransfer.files;
        handleFiles(files, fileList); // Pass fileList as an argument
    });

    // Click event for file input
    dropZone.addEventListener('click', function() {
        fileInput.click();
    });
    fileInput.addEventListener('change', function(event) {
        const files = event.target.files;
        handleFiles(files, fileList); // Pass fileList as an argument
    });
});

function handleFiles(files, fileList) {
    if (!files || files.length === 0) {
        return;
    }

    Array.from(files).forEach(function(file) {
        const li = document.createElement('li');
        const filename = document.createElement('span');
        filename.textContent = file.name;
        li.appendChild(filename);

        const progress = document.createElement('div');
        progress.className = 'progress';
        const progressBar = document.createElement('div');
        progressBar.className = 'progress-bar';
        progress.appendChild(progressBar);
        li.appendChild(progress);

        const downloadLink = document.createElement('a');
        downloadLink.href = '#';
        downloadLink.textContent = 'Download';
        downloadLink.style.display = 'none';
        li.appendChild(downloadLink);

        fileList.appendChild(li);

        // Simulated upload function
        uploadFile(file, progressBar, downloadLink);
    });
}

function uploadFile(file, progressBar, downloadLink) {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload', true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

    xhr.upload.onprogress = function(event) {
        if (event.lengthComputable) {
            const progress = (event.loaded / event.total) * 100;
            progressBar.style.width = `${progress}%`;
        }
    };

    xhr.onload = function() {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            const files = response.files;
            files.forEach(function(fileInfo) {
                if (fileInfo.filename === file.name) {
                    const uuid_filename = fileInfo.uuid_filename;
                    const filename = fileInfo.filename;
                    // 文件上传完成后的处理
                    downloadLink.href = `/download/${uuid_filename}/${filename}`;
                    downloadLink.style.display = 'block';
                    downloadLink.setAttribute('target', '_blank');
                }
            });
        }
    };

    const formData = new FormData();
    formData.append('file', file);
    xhr.send(formData);
}
