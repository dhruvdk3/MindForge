import cv2
import dlib
import os
import json
import numpy as np
import subprocess
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import time


app = Flask(__name__)
app.secret_key = 'hello'

recognizer = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

# Function to calculate the Euclidean distance between two face descriptors
def calculate_distance(descriptor1, descriptor2):
    return np.linalg.norm(np.array(descriptor1) - np.array(descriptor2))

# Function to put the display to sleep
def put_display_to_sleep():
    try:
        subprocess.run(["osascript", "-e", 'tell application "System Events" to sleep'])
        print("Display has been put to sleep.")
    except Exception as e:
        print("Error putting display to sleep:", e)

# Function to capture and store user's face data
def capture_and_store_face_data():
    # Initialize the camera
    camera = cv2.VideoCapture(0)

    # Try for a number of frames before concluding that no face is detected
    max_attempts = 20  # Adjust as needed
    attempts = 0

    while attempts < max_attempts:
        # Capture a single frame
        ret, frame = camera.read()

        if not ret:
            print("Error capturing an image.")
            continue

        # Detect faces in the captured frame
        detector = dlib.get_frontal_face_detector()
        faces = detector(frame)

        if not faces:
            attempts += 1
            continue

        # Get facial landmarks
        landmarks = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        face_descriptor = recognizer.compute_face_descriptor(frame, landmarks(frame, faces[0]))

        # Save the user's face data to a file
        with open("user_face_data.txt", "w") as file:
            for value in face_descriptor:
                file.write(str(value) + " ")

        print("Face data stored successfully.")
        break

    if attempts == max_attempts:
        print("No face detected in multiple attempts. Exiting.")
        put_display_to_sleep()

# Function to check if the user's face matches the stored data
def check_face_recognition():
    # Initialize the camera
    camera = cv2.VideoCapture(0)
    user_detected = False  # Track whether the user was last detected

    while True:
        # Capture a single frame
        ret, frame = camera.read()

        if not ret:
            print("Error capturing an image.")
            continue

        # Detect faces in the captured frame
        detector = dlib.get_frontal_face_detector()
        faces = detector(frame)

        if not faces:
            if user_detected:
                print("User not in front of the camera. Putting the display to sleep.")
                return False
                user_detected = False
            else:
                print("No face detected. Trying again...")
            continue

        # Get facial landmarks
        landmarks = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        face_descriptor = recognizer.compute_face_descriptor(frame, landmarks(frame, faces[0]))

        # Load the stored user's face data
        if os.path.exists("user_face_data.txt"):
            with open("user_face_data.txt", "r") as file:
                stored_face_data = [float(value) for value in file.read().split()]

            # Compare the stored data with the current data
            distance = calculate_distance(stored_face_data, face_descriptor)
            
            # Adjust the threshold as needed (lower values indicate a better match)
            threshold = 0.6

            if distance < threshold:
                print("Welcome back, user.")
                user_detected = True
            else:
                if user_detected:
                    print("User not recognized. Putting the display to sleep.")
                    return False
                    user_detected = False
                else:
                    print("User not recognized. Continuing face recognition...")
                continue  # Continue recognizing faces

        else:
            print("No user data found. Please run the program to capture your face data.")
            continue  # Continue recognizing faces


x = 2

@app.route('/')
def index():
    session['x'] = x
    x_value = session['x']
    return render_template('index.html', x = x_value)

@app.route('/alternative')
def alternative():
    return render_template('alternative.html')

@app.route('/detect-face', methods=['POST'])
def detect_face():
    capture_and_store_face_data()
    return redirect(url_for('index'))

@app.route('/recognize-face', methods=['POST'])
def recognize_face():
    result = check_face_recognition()
    
    if result == False:
        
        session['x'] -= 1
        time.sleep(5)
        if session['x'] == 0:
            return redirect(url_for('alternative'))
        else:
            # Call the recognize function again after 5 seconds
            return recognize_face()
    return result
recognize_route = app.route('/recognize-face', methods=['POST'])(recognize_face)

# Define a route to serve the question data as JSON
@app.route('/get_questions')
def get_questions():
    with open('data.txt', 'r') as file:
        data = json.load(file)
    for question in data:
        question['question'] = question['question'].replace('\n', '<br>')

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)

