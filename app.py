import streamlit as st
from bokeh.plotting import figure, output_file, show
import note_seq
from note_seq.protobuf import music_pb2
from scipy.io.wavfile import write
import numpy as np

MIDIFILE = 'Tests_music/i-do-like-to-be-beside-the-seaside.mid'

midi_file = MIDIFILE

sequence = note_seq.midi_file_to_note_sequence(midi_file)

p = note_seq.plot_sequence(sequence, show_figure=False)
note_seq.sequence_proto_to_midi_file(sequence, 'test_sequence.mid')


array = note_seq.synthesize(sequence, 44100)
length_array = int(len(array) / 5)
print("writing test wav")
write("test.wav", 44100, array.astype(np.float32)[:length_array])



st.title('Deep Music')
st.image('image_interface/vinyl-records_istock.png', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")


st.write(note_seq.__version__)




st.bokeh_chart(p, use_container_width=True)
note_seq.play_sequence(sequence, synth=note_seq.synthesize)



audio_file = open('test.wav', 'rb')
audio_bytes = audio_file.read()

st.audio(audio_bytes, format='audio/ogg')

second_audio_file = open('Tests_music/live.wav', 'rb')
second_audio_bytes = second_audio_file.read()

st.audio(second_audio_bytes, format='audio/ogg')
