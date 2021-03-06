# -*- coding: utf8 -*-


# from keras.models import load_model
import tensorflow as tf
import librosa
from function.functions import *
import os
from util.file_path import *
print(tf.__version__)
print(os.getcwd())
#  static
data_path = get_data_folder()
rating_scale = 0.01
right_standard = 0.8
wrong_standard = 0.2

def sound_to_test_data(wav_file):
    y, sr = librosa.load(wav_file)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=45, hop_length=int(sr*0.01), n_fft=int(sr*0.02)).T
    update_mfcc = remove_zero(mfcc)
    final_mfcc  = make_data(update_mfcc)
    return final_mfcc


def model_result(final_mfcc):
    model = tf.keras.models.load_model(data_path + 'changjun_ver_models/2학기화자인식모델_최창준.h5')
    y_pred = model.predict(final_mfcc)
    zero_count = 0
    print(y_pred.shape)
    print(y_pred[:3])
    for i in range(len(y_pred)):
        if y_pred[i] < rating_scale:
            zero_count += 1

    return zero_count/len(y_pred)

def calculate_result(zero_percentage):
    print("zero_percentage :" , zero_percentage)
    if zero_percentage >= right_standard:
        return True, zero_percentage
    return False, zero_percentage


def execute_recognize(wav_file):
    final_mfcc = sound_to_test_data(wav_file)
    zero_percentage = model_result(final_mfcc)
    return calculate_result(zero_percentage)

wav_file = data_path + "new.wav"
execute_recognize(wav_file)
