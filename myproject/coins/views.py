from django.shortcuts import render, redirect
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
from .models import ImageModel

from django.http import JsonResponse

# Load the model
model = load_model("model/keras_model.h5", compile=False)

# Load the labels
class_names = open("model/labels.txt", "r").readlines()



def index(request):
    context = {}  # Define a default context
    
    if request.method == 'POST':

        if 'reset_session' in request.POST:
            # Reset session data
            request.session['total_value'] = 0
            request.session['detections'] = []

            return redirect('index')  # Redirect to avoid resubmitting the form

        if request.FILES['image']:
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
            max_confidence_index = np.argmax(prediction[0])
            class_names_with_scores = [(class_name.split(' ', 1)[1], float(confidence)) for class_name, confidence in zip(class_names, prediction[0])]
            class_name, confidence = class_names[max_confidence_index].split(' ', 1)[1], round(float(prediction[0][max_confidence_index]), 5)

            # Calculate the total value of the detected coins
            total_value = request.session.get('total_value', 0)
            detections = request.session.get('detections', [])  
            # Update the total value based on the detected class
            if confidence >= 0.6:
                if '1 PESO' in class_name:
                    total_value += 1
                elif '5 PESO' in class_name:
                    total_value += 5
                elif '10 PESO' in class_name:
                    total_value += 10
                elif '25 CENTS' in class_name:
                    total_value += 0.25
                elif '20 PESO' in class_name:
                    total_value += 20

            # Update the session with the new total value
            request.session['total_value'] = total_value

            # Save the image to the model
            image_model = ImageModel.objects.create(image=image)

            detection_data = {
                'class_name': class_name,
                'confidence': confidence,
                'total_value': total_value,
                'image_url': image_model.image.url,
            }
            print("Adding to detections:", detection_data)
            detections.append(detection_data)
            request.session['detections'] = detections

            # Pass the detection result to the template
            context = {
                'class_names_with_scores': class_names_with_scores,
                'total_value': total_value,
                'image_url': image_model.image.url,
                'detections': detections
            }

            return render(request, 'index.html', context)   
        if request.method == 'GET':
            return redirect('index')  # Redirect to avoid resubmitting the form
    return render(request, 'index.html', context)



