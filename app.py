import streamlit as st
from bokeh.plotting import figure, output_file, show
import note_seq
from note_seq.protobuf import music_pb2
from scipy.io.wavfile import write
import numpy as np
import os
import pandas as pd
import requests
import subprocess

filepath = 'Tests_music/'
songs = os.listdir(filepath)

def api_call(song_file):
    subprocess.call([
        'curl', '-X', 'POST',
        'https://image-name-2b76463dxa-uc.a.run.app/uploadfile/', "-H",
        'accept: application/json', "-H", 'Content-Type: multipart/form-data',
        "-F", f'file=@{filepath}{song_file};type=audio/mid'
    ])
    print(f'{filepath}{song_file}')


def filter_midi(songs):
    midis = []
    for song in songs:
        if song.endswith('mid'):
            midis.append(song)
    return midis

songs = filter_midi(songs)

dict_song = {}

def midi_to_wav(song):
    sequence = note_seq.midi_file_to_note_sequence(song)
    p = note_seq.plot_sequence(sequence, show_figure=False)
    note_seq.sequence_proto_to_midi_file(sequence, song)
    array = note_seq.synthesize(sequence, 44100)
    length_array = int(len(array) / 5)
    s = song[:-3] + 'wav'
    write(s, 44100, array.astype(np.float32)[:length_array])
    return s, p

for i in songs:
    dict_song[i] = [*midi_to_wav(filepath + i)]


st.title('Deep Music')
st.image('image_interface/vinyl-records_istock.png', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

selection = st.selectbox('Select a song', songs)
print(selection)
print(api_call(selection))

st.write(note_seq.__version__)
st.bokeh_chart(dict_song[selection][1], use_container_width=True)

audio_file = open(dict_song[selection][0], 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/ogg')


# while selection == 'beeth9-3.mid':
#     audio_file = open(dict_song['beeth9-3.mid'], 'rb')
#     audio_bytes = audio_file.read()
#     st.audio(audio_bytes, format='audio/ogg')
