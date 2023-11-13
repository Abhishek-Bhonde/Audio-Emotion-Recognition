import pandas as pd
import numpy as np
import os
import tempfile
import soundfile as sf

import pickle
from tensorflow import keras
from flask import Flask, render_template, request, redirect, url_for,jsonify
import librosa
import python_speech_features

import librosa.display

model = pickle.load(open('D:/Projects/Sound Emotion Recognition/Flask/model.pkl','rb'))

labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Pleasant Surprise', 'Sad']

app = Flask(__name__, template_folder='template', static_folder='static')


def extract_mfcc(filename):
    try:
        y, sr = librosa.load(filename, duration=1, offset=0.5)
        print(filename)
        # y, sr = sf.read("Bhonde_emotion/static/OAF_base_angry.wav", dtype='float32')
        # print("Loaded audio 'y':", y)
        # print("Sampling rate 'sr':", sr)

        mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
        # mfcc = python_speech_features.base.mfcc(y, samplerate=sr, winlen=0.025, winstep=0.01, numcep=13, nfilt=26, nfft=512, lowfreq=0, highfreq=None, preemph=0.97, ceplifter=22)
        return mfcc
    except Exception as e:
        
        print("Error extracting MFCC features:", e)
        return None


@app.route('/')
def upload_form():
    return render_template('index.html', prediction='', error='')

@app.route('/recognize-emotion', methods=['POST'])
def predict_emotion():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio part'})

    audio = request.files['audio']

    if not audio:
        return jsonify({'error': 'No file selected'})

    if audio.filename == '':
        return jsonify({'error': 'No file selected'})

    temp_audio_path = 'temp_audio.wav'
    audio.save(temp_audio_path)

    try:
        mfcc_features = extract_mfcc(temp_audio_path)
        if mfcc_features is not None:
            pred_X = np.array([mfcc_features])
            pred_X = np.expand_dims(pred_X, -1)
            pred = labels[model.predict(pred_X).argmax()]
            os.remove(temp_audio_path)
            return jsonify({'emotion': pred, 'error': None})
        else:
            return jsonify({'error': 'MFCC feature extraction failed'})
    except Exception as e:
        return jsonify({'error': str(e)})
    

if __name__ == "__main__":
    app.run(debug=True, port=8000)

    
    # mfcc_features = extract_mfcc(temp_audio_path)

    # if mfcc_features is not None:
    #     pred_X = np.array([mfcc_features])
    #     pred_X = np.expand_dims(pred_X, -1)
    #     pred = labels[model.predict(pred_X).argmax()]

    #     os.remove(temp_audio_path)

    #     # return render_template('index.html', prediction=pred, error='')
    #     return jsonify({'emotion': pred, 'error': None})

    # return jsonify({'error': 'Error processing the audio file'})
