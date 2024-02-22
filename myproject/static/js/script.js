// coindetection/static/coindetection/script.js

let model, labelContainer, maxPredictions;

// Load the image model
async function init() {
    if (model) {
        model.dispose(); // Dispose of the previous model
        labelContainer.innerHTML = ""; // Clear previous predictions
    }

    const URL = "https://teachablemachine.withgoogle.com/models/SPQDJ9ipW/";
    const modelURL = URL + "model.json";
    const metadataURL = URL + "metadata.json";

    model = await tmImage.load(modelURL, metadataURL);
    maxPredictions = model.getTotalClasses();

    labelContainer = document.getElementById("label-container");
}

// Predict the uploaded image
async function predict() {
    if (!model) {
        console.error("Model not loaded yet.");
        return;
    }

    const imageUpload = document.getElementById("imageUpload");
    const file = imageUpload.files[0];
    const img = document.createElement("img");
    const reader = new FileReader();

    reader.onload = async function(e) {
        img.src = e.target.result;
        img.width = 200; // Set image width for display
        img.height = 200; // Set image height for display
        document.body.appendChild(img); // Append image to the body for display

        const prediction = await model.predict(img);
        labelContainer.innerHTML = ""; // Clear previous predictions
        for (let i = 0; i < maxPredictions; i++) {
            const classPrediction =
                prediction[i].className + ": " + prediction[i].probability.toFixed(2);
            const div = document.createElement("div");
            div.innerHTML = classPrediction;
            labelContainer.appendChild(div);
        }
    };

    reader.readAsDataURL(file); // Read uploaded image as data URL
}
