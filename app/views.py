from .king import img_check_from_video
from django.shortcuts import render
def classify_image(request):
    prediction = img_check_from_video()

    if prediction:
        # Return the prediction to the template
        return render(request, 'result.html', {'prediction': prediction})
    else:
        return render(request, 'result.html', {'message': 'No defects found or video error'})