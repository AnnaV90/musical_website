import streamlit as st


st.title('Deep Music')

st.image('image_interface/vinyl-records_istock.png', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

st.selectbox('Select note', ['A', 'B', 'C'])

audio_file = open('Tests_music/live.wav', 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/ogg')
