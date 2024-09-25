from transformers import pipeline
from PIL import Image
import cv2

# Initialize the pipeline once
pipe = pipeline("zero-shot-image-classification", model="TonyStarkD99/CLIP-Crop_Disease")

def img_check_from_video():
    # Define candidate labels for classification
    candidate_labels = ["healthy", "defect"]

    # Open a connection to the drone's video stream
    video_feed = cv2.VideoCapture('http://192.168.53.115:8080/video')  # Change this URL to your drone feed

    # Variable to hold the prediction
    prediction = None

    if not video_feed.isOpened():
        print("Error: Unable to open video stream")
        return None

    frame_count = 0
    max_frames = 20  # Number of frames to process before stopping

    while video_feed.isOpened() and frame_count < max_frames:
        ret, frame = video_feed.read()

        if ret:
            # Convert the frame (numpy array) to PIL Image
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Perform the classification
            results = pipe(images=image, candidate_labels=candidate_labels)

            # Get the label with the highest score
            predicted_class = max(results, key=lambda x: x['score'])
            label = predicted_class['label']
            score = predicted_class['score']

            # If a defect is found, return the prediction immediately
            if label == "healthy":
                prediction = {
                    'label': label,
                    'score': score,
                }
                break  # Stop once a defect is found
            if label == "defect":
                prediction = {
                    'label': label,
                    'score': score,
                }
                break  # Stop once a defect is found
            
            frame_count += 1
        else:
            break

    # Release the video feed
    video_feed.release()

    # Return the final prediction
    return prediction
