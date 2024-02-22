from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
from django.shortcuts import render
from .models import ImageModel

# Load the model
model = load_model("model/keras_model.h5", compile=False)

# Load the labels
class_names = open("model/labels.txt", "r").readlines()
def index(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        # Create the array of the right shape to feed into the keras model
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # Open and process the image
        with Image.open(image) as img:
            img = ImageOps.fit(img, (224, 224), Image.Resampling.LANCZOS)
            image_array = np.asarray(img)
            normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
            data[0] = normalized_image_array

        # Predict using the model
        prediction = model.predict(data)
        class_names_with_scores = [(class_name.split(' ', 1)[1], confidence) for class_name, confidence in zip(class_names, prediction[0])]

        # Save the image to the model
        image_model = ImageModel.objects.create(image=image)

        # Pass the prediction, confidence scores, and image URL to the template
        context = {
            'class_names_with_scores': class_names_with_scores,
            'image_url': image_model.image.url  # Get the URL of the saved image
        }
        return render(request, 'index.html', context)
    
    return render(request, 'index.html', {})
    