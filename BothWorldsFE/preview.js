document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.querySelector('input[type="file"]');
    const previewArea = document.getElementById('previewArea');

    fileInput.addEventListener('change', function(e) {
        const fileList = e.target.files;
        previewArea.innerHTML = ''; // Clear existing content

        Array.from(fileList).forEach((file, index) => {
            const jsonPreview = document.createElement('div');
            jsonPreview.className = 'bg-gray-200 p-2 rounded my-2';
            jsonPreview.textContent = `File ${index + 1}: ${file.name}`;
            previewArea.appendChild(jsonPreview);
        });
    });
});
