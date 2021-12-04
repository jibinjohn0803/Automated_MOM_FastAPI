
import os
import numpy as np
import pandas as pd
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import pickle
#import cv2
import librosa
from tensorflow.keras.models import load_model
from transformers import pipeline


# load model
classes = ['Neutral','Calm','Happy','Sad','Angry','Fear','Disgust','Surprise']

# load model
model = load_model('Model_CNN.h5')
model.compile(loss = "categorical_crossentropy",
             optimizer = "rmsprop",
             metrics = ["accuracy"])
scaler = pickle.load(open('scaler.pkl','rb'))
# speech recognition
# create a speech recognition object
r = sr.Recognizer()
# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text
def noise(data):
    noise_amp = 0.035*np.random.uniform()*np.amax(data)
    data = data + noise_amp*np.random.normal(size=data.shape[0])
    return data

def stretch(data, rate=0.8):
    return librosa.effects.time_stretch(data, rate)

def shift(data):
    shift_range = int(np.random.uniform(low=-5, high = 5)*1000)
    return np.roll(data, shift_range)

def pitch(data, sampling_rate, pitch_factor=0.7):
    return librosa.effects.pitch_shift(data, sampling_rate, pitch_factor)


def extract_features(data,sample_rate):
	# ZCR
	result = np.array([])
	zcr = np.mean(librosa.feature.zero_crossing_rate(y=data).T, axis=0)
	result = np.hstack((result, zcr))  # stacking horizontally

	# Chroma_stft
	stft = np.abs(librosa.stft(data))
	chroma_stft = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
	result = np.hstack((result, chroma_stft))  # stacking horizontally

	# MFCC
	mfcc = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate).T, axis=0)
	result = np.hstack((result, mfcc))  # stacking horizontally

	# Root Mean Square Value
	rms = np.mean(librosa.feature.rms(y=data).T, axis=0)
	result = np.hstack((result, rms))  # stacking horizontally

	# MelSpectogram
	mel = np.mean(librosa.feature.melspectrogram(y=data, sr=sample_rate).T, axis=0)
	result = np.hstack((result, mel))  # stacking horizontally

	return result


def get_features(path):
	# duration and offset are used to take care of the no audio in start and the ending of each audio files as seen above.
	data, sample_rate = librosa.load(path, duration=2.5, offset=0.6)

	# without augmentation
	res1 = extract_features(data,sample_rate)
	result = np.array(res1)

	# data with noise
	noise_data = noise(data)
	res2 = extract_features(noise_data,sample_rate)
	result = np.vstack((result, res2))  # stacking vertically

	# data with stretching and pitching
	new_data = stretch(data)
	data_stretch_pitch = pitch(new_data, sample_rate)
	res3 = extract_features(data_stretch_pitch,sample_rate)
	result = np.vstack((result, res3))  # stacking vertically
	return result

def predictMOM(fileLoc):
	print("Inside predictMOM",fileLoc)
	if os.path.exists(fileLoc):
		print("Path exists at location : {}".format(fileLoc))
	else:
		print("Path does not exists")
		raise Exception("Path does not exists at location : {}".format(fileLoc))
	audio = get_features(fileLoc)
	audio_df = pd.DataFrame(audio)
	audio = scaler.transform(audio_df)
	audio = np.expand_dims(audio, axis=2)
	p = model.predict(audio)[0]
	output = np.argmax(p)
	print(output)
	output = classes[output]
	print(output)
	x = get_large_audio_transcription(fileLoc)
	summary1 = str(x)
	summarization = pipeline("summarization")
	original_text = summary1
	summary_text = summarization(original_text)[0]['summary_text']
	resultSummaryText = summary_text
	resultSentimentText = output
	resultFullText = summary1
	return resultSummaryText, resultSentimentText, resultFullText
