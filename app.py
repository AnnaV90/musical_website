import streamlit as st
from bokeh.plotting import figure, output_file, show
import note_seq
from note_seq.protobuf import music_pb2
import numpy as np
import os
import pandas as pd
import requests
import subprocess
from scipy.io import wavfile
import os.path
import matplotlib.pyplot as plt


def makeEvaluation(song):


    #### Eval part of the App
    st.text('Evaluate the results')
    st.write(
        '''Estimating the performance of our music maker model can appear very
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
    criteria_1 = st.slider('Melody', min_value=1.0, max_value=5.0, value=2.5, step=0.5)
    criteria_2 = st.slider('Harmony',
                           min_value=1.0,
                           max_value=5.0,
                           value=2.5,
                           step=0.5)
    criteria_3 = st.slider('Rhythm', min_value=1.0, max_value=5.0, value=2.5, step=0.5)
    criteria_4 = st.slider('Creativity',
                           min_value=1.0,
                           max_value=5.0,
                           value=2.5,
                           step=0.5)
    results_button = st.button('Results')
    # actions

    if results_button:
        average = (criteria_1 + criteria_2 + criteria_3 + criteria_4) / 4
        new_row = {
            'Melody': (criteria_1),
            'Harmony': (criteria_2),
            'Rhythm': (criteria_3),
            'Creativity': (criteria_4),
            'Average': (average)
        }
        results_data = results_data.append(new_row, ignore_index=True)
        if os.path.isfile(f'{song}_results_csv.csv'):
            results_data.to_csv(f'{song}_results_csv.csv',
                                mode='a',
                                header=False)
        else:
            results_data.to_csv(f'{song}_results_csv.csv')
        st.write(average)
        all_data = pd.read_csv(f'{song}_results_csv.csv')
        all_data.drop(all_data.columns[[0]], axis=1, inplace=True)
        ax = all_data.plot(kind='line')
        ax.set_ylabel("Rating")
        ax.set_xlabel("Ratings Over Time")
        st.table(all_data)

        st.pyplot(fig=ax.get_figure(), clear_figure=None)


st.title('Deep Music')
st.image('image_interface/vinyl-records_istock.png',
         caption=None,
         width=None,
         use_column_width=None,
         clamp=False,
         channels="RGB",
         output_format="auto")

page = st.selectbox("Choose your song", [
    "Avengers", "Daft Punk Around the World", "Happy Birthday",
    "Batman Returns", "Hans Zimmer Time","Coldplay Viva la Vida",
    "Skrillex Scary Monsters & Nice Sprites", "Autoencoder Experiments"
])
if page == "Avengers":



    st.text("Avengers Song")
    sequence = note_seq.midi_file_to_note_sequence("Tests_music/Avengers.mid")
    p = note_seq.plot_sequence(sequence, show_figure=False)

    st.bokeh_chart(p, use_container_width=True)

    st.text("Actual Song")
    audio_file = open("Tests_music/Avengers.wav", 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')

    st.text("Predicted")
    sequence = note_seq.midi_file_to_note_sequence("Prediction_music/avengers_test.mid")
    p = note_seq.plot_sequence(sequence, show_figure=False)

    st.bokeh_chart(p, use_container_width=True)
    audio_file = open("Prediction_music/avengers_test.wav", 'rb')
    audio_bytes = audio_file.read()
    makeEvaluation("Avengers")

if page == "Daft Punk Around the World":

    st.text("Daft Punk Around the World")
    sequence = note_seq.midi_file_to_note_sequence(
        "Tests_music/Daft Punk - Around The World.mid")
    p = note_seq.plot_sequence(sequence, show_figure=False)

    st.bokeh_chart(p, use_container_width=True)

    st.text("Actual Song")
    audio_file = open("Tests_music/Daft Punk - Around The World.wav", 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')

    st.text("Predicted")
    sequence = note_seq.midi_file_to_note_sequence(
        "Prediction_music/daft_test.mid")
    p = note_seq.plot_sequence(sequence, show_figure=False)

    st.bokeh_chart(p, use_container_width=True)
    audio_file = open("Prediction_music/daft_test.wav", 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')
    makeEvaluation("Daft Punk")


if page == "Happy Birthday":

    st.text("Happy Birthday")
    sequence = note_seq.midi_file_to_note_sequence(
        "Tests_music/Happy-Birthday-To-You-4.mid")
    p = note_seq.plot_sequence(sequence, show_figure=False)

    st.bokeh_chart(p, use_container_width=True)

    st.text("Actual Song")
    audio_file = open("Tests_music/Happy-Birthday-To-You-4.wav", 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')

    st.text("Predicted")
    sequence = note_seq.midi_file_to_note_sequence(
        "Prediction_music/Happy_test.mid")
    p = note_seq.plot_sequence(sequence, show_figure=False)

    st.bokeh_chart(p, use_container_width=True)
    audio_file = open("Prediction_music/Happy_test.wav", 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')
    # fig, ax = plt.subplots()
    # sample_rate, X = wavfile.read("Prediction_music/Happy_test.wav")
    # ax.specgram(X, Fs = 10)
    # st.pyplot(fig=fig, clear_figure=None)

    makeEvaluation("Happy Birthday")

if page == "Batman Returns":

    st.text("Batman Returns Game Over")
    sequence = note_seq.midi_file_to_note_sequence(
        "Tests_music/BatmanReturnsGameOver.mid")
    p = note_seq.plot_sequence(sequence, show_figure=False)

    st.bokeh_chart(p, use_container_width=True)

    st.text("Actual Song")
    audio_file = open("Tests_music/BatmanReturnsGameOver.wav", 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')

    st.text("Predicted")
    sequence = note_seq.midi_file_to_note_sequence(
        "Prediction_music/test_batman.mid")
    p = note_seq.plot_sequence(sequence, show_figure=False)

    st.bokeh_chart(p, use_container_width=True)
    audio_file = open("Prediction_music/test_batman.wav", 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')

    makeEvaluation("Batman Returns")


if page == "Hans Zimmer Time":

    st.text("Hans Zimmer Time")
    sequence = note_seq.midi_file_to_note_sequence(
        "Tests_music/Hans Zimmer - Time.mid")
    p = note_seq.plot_sequence(sequence, show_figure=False)

    st.bokeh_chart(p, use_container_width=True)

    st.text("Actual Song")
    audio_file = open("Tests_music/Hans Zimmer - Time.wav", 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')

    st.text("Predicted")
    sequence = note_seq.midi_file_to_note_sequence(
        "Prediction_music/Hans_file.mid")
    p = note_seq.plot_sequence(sequence, show_figure=False)

    st.bokeh_chart(p, use_container_width=True)
    audio_file = open("Prediction_music/Hans_file.wav", 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')

    makeEvaluation("Hans Zimmer")

if page == "Coldplay Viva la Vida":

    st.text("Coldplay Viva la Vida")
    sequence = note_seq.midi_file_to_note_sequence(
        "Tests_music/Coldplay - Viva La Vida.mid")
    p = note_seq.plot_sequence(sequence, show_figure=False)

    st.bokeh_chart(p, use_container_width=True)

    st.text("Actual Song")
    audio_file = open("Tests_music/Coldplay - Viva La Vida.wav", 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')

    st.text("Predicted")
    sequence = note_seq.midi_file_to_note_sequence(
        "Prediction_music/test2_coldplay.mid")
    p = note_seq.plot_sequence(sequence, show_figure=False)

    st.bokeh_chart(p, use_container_width=True)
    audio_file = open("Prediction_music/test2_coldplay.wav", 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')

    makeEvaluation("Coldplay")


if page == "Skrillex Scary Monsters & Nice Sprites":

    st.text("Skrillex Scary Monsters & Nice Sprites")
    sequence = note_seq.midi_file_to_note_sequence(
        "Tests_music/Skrillex - Scary Monsters & Nice Sprites.mid")
    p = note_seq.plot_sequence(sequence, show_figure=False)

    st.bokeh_chart(p, use_container_width=True)

    st.text("Actual Song")
    audio_file = open(
        "Tests_music/Skrillex - Scary Monsters & Nice Sprites.wav", 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')

    st.text("Predicted")
    sequence = note_seq.midi_file_to_note_sequence(
        "Prediction_music/skrillex_test.mid")
    p = note_seq.plot_sequence(sequence, show_figure=False)

    st.bokeh_chart(p, use_container_width=True)
    audio_file = open("Prediction_music/skrillex_test.wav", 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')
    makeEvaluation("Skrillex")


if page == "Autoencoder Experiments":

    st.text("Autoencoder Experiments")
    st.text("These are the results of the experiments made with the autoencoder")
    # sequence = note_seq.midi_file_to_note_sequence(
    #     "Prediction_music/live.mid")
    # p = note_seq.plot_sequence(sequence, show_figure=False)

    # st.bokeh_chart(p, use_container_width=True)

    st.text("Experiment #1")
    audio_file = open("Prediction_music/live.wav", 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')



    st.text("Experiment #2")

    # sequence = note_seq.midi_file_to_note_sequence("Prediction_music/random_params_live.mid")
    # p = note_seq.plot_sequence(sequence, show_figure=False)

    # st.bokeh_chart(p, use_container_width=True)

    # st.text("Experiment #1")
    audio_file = open("Prediction_music/random_params_live.wav", 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')


    st.text("Experiment #3")

    # sequence = note_seq.midi_file_to_note_sequence(
    #     "Prediction_music/random_params_3_live.mid")
    # p = note_seq.plot_sequence(sequence, show_figure=False)

    # st.bokeh_chart(p, use_container_width=True)

    # st.text("Experiment #1")
    audio_file = open("Prediction_music/random_params_3_live.wav", 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')
    makeEvaluation("Random Experiments")
