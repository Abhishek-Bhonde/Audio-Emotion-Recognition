import numpy as np
from keras.models import load_model
from flask import Flask, render_template, request
import librosa

model = load_model('audio.h5')

emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Pleasant Surprise', 'Sad']

app = Flask(__name__, template_folder="template", static_folder="static")

@app.route('/')
def index():
    return render_template('index.html', prediction='', error='')

@app.route('/recognize-emotion', methods=['POST'])
def recognize_emotion():
    if 'audio' not in request.files:
        return render_template('index.html', prediction='', error='No audio file provided')

    audio_file = request.files['audio']

    if audio_file.filename == '':
        return render_template('index.html', prediction='', error='No selected audio file')

    try:
        y, sr = librosa.load(audio_file, duration=3, offset=0.5)
        mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
        mfcc = np.expand_dims(mfcc, axis=0)
        mfcc = np.expand_dims(mfcc, axis=2)

        prediction = model.predict(mfcc)
        predicted_label = np.argmax(prediction)
        predicted_emotion = emotions[predicted_label]

        return render_template('index.html', prediction=predicted_emotion, error='')

    except Exception as e:
        return render_template('index.html', prediction='', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)

