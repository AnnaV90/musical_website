import streamlit as st
from bokeh.plotting import figure, output_file, show
import note_seq
from note_seq.protobuf import music_pb2

import ctypes.util
orig_ctypes_util_find_library = ctypes.util.find_library

def proxy_find_library(lib):
    if lib == 'fluidsynth':
        return 'libfluidsynth.so.1'
    else:
        return orig_ctypes_util_find_library(lib)

ctypes.util.find_library = proxy_find_library


st.title('Deep Music')
st.image('image_interface/vinyl-records_istock.png', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
st.selectbox('Select note', ['A', 'B', 'C'])

teapot = music_pb2.NoteSequence()
teapot.notes.add(pitch=69, start_time=0, end_time=0.5, velocity=80)
teapot.notes.add(pitch=71, start_time=0.5, end_time=1, velocity=80)
teapot.notes.add(pitch=73, start_time=1, end_time=1.5, velocity=80)
teapot.notes.add(pitch=74, start_time=1.5, end_time=2, velocity=80)
teapot.notes.add(pitch=76, start_time=2, end_time=2.5, velocity=80)
teapot.notes.add(pitch=81, start_time=3, end_time=4, velocity=80)
teapot.notes.add(pitch=78, start_time=4, end_time=5, velocity=80)
teapot.notes.add(pitch=81, start_time=5, end_time=6, velocity=80)
teapot.notes.add(pitch=76, start_time=6, end_time=8, velocity=80)
teapot.total_time = 8
teapot.tempos.add(qpm=60)
p = note_seq.plot_sequence(teapot, show_figure=False)
note_seq.sequence_proto_to_midi_file(teapot, 'test_sequence.mid')
st.bokeh_chart(p, use_container_width=True)
note_seq.play_sequence(teapot, synth=note_seq.synthesize)

# audio_file = open('test_sequence.mid', 'rb')
# audio_bytes = audio_file.read()
# st.audio(audio_bytes, format='audio/mid')

# audio_file = open('Tests_music/live.wav', 'rb')
# audio_bytes = audio_file.read()
# st.audio(audio_bytes, format='audio/ogg')
