// Utility function to convert base64 to file
function base64ToFile(dataURI, fileName) {
    var byteString = atob(dataURI.split(',')[1]);
    var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
    
    var ab = new ArrayBuffer(byteString.length);
    var ia = new Uint8Array(ab);
    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    
    return new File([ab], fileName, {type: mimeString});
}

// Utility function to mimic DataTransfer object for file input
function createFileList(...files) {
    const dataTransfer = new DataTransfer();
    files.forEach(file => {
        dataTransfer.items.add(file);
    });
    return dataTransfer.files;
}

function openCamera() {
    document.getElementById('captureImage').addEventListener('click', () => {
        const cameraWindowUrl = '{% url "webcam" %}';
        const cameraWindow = window.open(cameraWindowUrl, 'cameraPopup', 'width=800,height=600');

        // Post-capture callback
        window.onmessage = (event) => {
            if (event.origin !== window.location.origin) {
                alert('Origin not allowed');
                return;
            }

            const { action, imageData } = event.data;
            if (action === 'captured') {
                // Convert Base64 image to File Object and set it as the value of the file input
                const imageFile = base64ToFile(imageData, "capturedImage.jpg");
                document.getElementById('imageInput').files = createFileList(imageFile);
                submitForm()
            }
        };
    });
}