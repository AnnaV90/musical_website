import streamlit as st
from bokeh.plotting import figure, output_file, show
import note_seq
from note_seq.protobuf import music_pb2
import numpy as np
import os
import pandas as pd
import requests
import subprocess
from songConverter import convert_many_midis_to_wav, song_predict, midi_to_wav, api_call

import os.path



SONG_FLAG = False
if SONG_FLAG == False:
    filepath = 'Tests_music/'
    prediction_path = 'Prediction_music/'
    songs = os.listdir(filepath)
    predicted_songs = os.listdir(prediction_path)

# song_dict = {}
# sequence = note_seq.midi_file_to_note_sequence(filepath + "Awakening1.mid")
# p = note_seq.plot_sequence(sequence, show_figure=False)

# song_dict["Awakening1.mid"] = [filepath + "Awakening1" + ".wav", p]


# prediction_dict = {}
# sequence2 = note_seq.midi_file_to_note_sequence(prediction_path + "Awakening1.mid")
# p2 = note_seq.plot_sequence(sequence2, show_figure=False)

# prediction_dict["Awakening1.mid"] = [prediction_path + "Awakening1.wav", p2]
# # print(prediction_dict)


if SONG_FLAG == False:
    song_dict = convert_many_midis_to_wav(filepath, songs)
    prediction_dict = convert_many_midis_to_wav(prediction_path,
                                                predicted_songs)
    print(song_dict)
    print("------")
    print(prediction_dict)
    midis_only = []
    for i in songs:
        if i.endswith(".mid"):
            midis_only.append(i)

    SONG_FLAG = True




st.title('Deep Music')
st.image('image_interface/vinyl-records_istock.png', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

st.set_option('deprecation.showfileUploaderEncoding', False)

uploaded_file = st.file_uploader("Choose a midi file", type="mid")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

    with open(f'Tests_music/{uploaded_file.name}', 'wb') as test_midi:
        test_midi.write(bytes_data)
    try:
        midi_to_wav(f'Tests_music/{uploaded_file.name}')
        api_call(f'Tests_music/{uploaded_file.name}')
        midi_to_wav(f'Prediction_music/{uploaded_file.name}')
        SONG_Flag = False

    except:
        wave_name = uploaded_file.name[:-3] + "wav"
        if os.path.exists(f"Tests_music/{uploaded_file.name}"):
            os.remove(f"Tests_music/{uploaded_file.name}")
        if os.path.exists(f"Tests_music/{wave_name}"):
            os.remove(f"Tests_music/{wave_name}")
        if os.path.exists(f"Prediction_music/{uploaded_file.name}"):
            os.remove(f"Prediction_music/{uploaded_file.name}")
        if os.path.exists(f"Prediction_music/{wave_name}"):
            os.remove(f"Prediction_music/{wave_name}")
        st.write("Uploading midi file failed - format not supported yet")

selection = st.selectbox('Select a song', midis_only)


# print(selection)
# print(api_call(selection))

st.write(note_seq.__version__)
st.bokeh_chart(song_dict[selection][1], use_container_width=True)

audio_file = open(song_dict[selection][0], 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/ogg')



# st.bokeh_chart(dict_predict[selection][1], use_container_width=True)
st.bokeh_chart(prediction_dict[selection][1], use_container_width=True)

audio_file = open(prediction_dict[selection][0], 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/ogg')


# while selection == 'beeth9-3.mid':
#     audio_file = open(dict_song['beeth9-3.mid'], 'rb')
#     audio_bytes = audio_file.read()
#     st.audio(audio_bytes, format='audio/ogg')



title = st.text_input(
    'Step 1', 'Select a song and predict the following sequence of note')
# app.py code
st.text_input('Step 2', 'Evaluate the results')
st.write('''Estimating the performance of our music maker model can appear very
         subjective. It is very hard to find quantitative metrics to judge
         music creativity.
        So, we defined some criteria or rules in order to rank our musical
        prediction.
        - Melody: Does it sound like real music?
        - Harmony: Is it nice to your ears?
        - Rhythm: How is the dynamic?
        - Creativity: Do you like the music?''')
st.write('Please rate the generated tracks here:')
# data
results_data = pd.DataFrame(
    columns=['Melody', 'Harmony', 'Rhythm', 'Creativity', 'Average'])
# widgets
table = st.empty()
criteria_1 = st.slider('Melody', min_value=1, max_value=5, value=1, step=1)
criteria_2 = st.slider('Harmony', min_value=1, max_value=5, value=1, step=1)
criteria_3 = st.slider('Rhythm', min_value=1, max_value=5, value=1, step=1)
criteria_4 = st.slider('Creativity', min_value=1, max_value=5, value=1, step=1)
results_button = st.button('Results')
# actions

if results_button:
    average = (criteria_1 + criteria_2 + criteria_3 + criteria_4) / 4
    new_row = {
        'Melody': str(criteria_1),
        'Harmony': str(criteria_2),
        'Rhythm': str(criteria_3),
        'Creativity': str(criteria_4),
        'Average': str(average)
    }
    results_data = results_data.append(new_row, ignore_index=True)
    if os.path.isfile('raw_data/results_csv.csv'):
        results_data.to_csv('raw_data/results_csv.csv', mode='a', header=False)
    else:
        results_data.to_csv('raw_data/results_csv.csv')
    st.write(average)
    st.table(results_data)
