import subprocess
import os
import note_seq
from note_seq.protobuf import music_pb2
import numpy as np
from scipy.io.wavfile import write

filepath = 'Tests_music/'
prediction_path = 'Prediction_music/'
songs = os.listdir(filepath)
predicted_songs = os.listdir(prediction_path)


def api_call(song_file):
    file_data = subprocess.Popen([
        'curl', '-X', 'POST',
        'https://image-name-2b76463dxa-ew.a.run.app/uploadfile/', "-H",
        'accept: application/json', "-H", 'Content-Type: multipart/form-data',
        "-F", f'file=@{song_file};type=audio/mid'
    ],
                                 stdout=subprocess.PIPE)
    (out, err) = file_data.communicate()
    song_file = song_file.split("/")[1]
    with open(f'Prediction_music/{song_file}', 'wb') as test_midi:
        test_midi.write(out)


def filter_midi(songs):
    midis = []
    for song in songs:
        if song.endswith('mid'):
            midis.append(song)
    return midis


songs = filter_midi(songs)
predicted_songs = filter_midi(predicted_songs)
dict_song = {}
dict_predict = {}


def midi_to_wav(song):
    sequence = note_seq.midi_file_to_note_sequence(song)
    p = note_seq.plot_sequence(sequence, show_figure=False)
    if str(song[:-3] + 'wav') in songs and str(song[:-3] + 'wav') in predicted_songs:

        return str(song[:-3] + 'wav'), p

    note_seq.sequence_proto_to_midi_file(sequence, song)
    array = note_seq.synthesize(sequence, 44100)
    length_array = int(len(array))
    s = song[:-3] + 'wav'
    write(s, 44100, array.astype(np.float32)[:length_array])
    return s, p



def convert_many_midis_to_wav(fp, songs_path):
    """path of many midis in a list"""
    dict_song = {}
    midis = filter_midi(songs_path)
    for i in midis:
        try:
            dict_song[i] = [*midi_to_wav(fp + i)]
        except:
            os.remove(f"{fp}{i}")
            os.remove(f"{filepath}{i}")
            print(f"Converting {i} failed :S")
    return dict_song


def song_predict(fp, songs_path):
    midis = filter_midi(songs_path)
    for song in midis:
        api_call(fp + song)


if __name__ == "__main__":
    # dicto = convert_many_midis_to_wav(prediction_path, songs)
    # song_predict(filepath, songs)
    # dicto = convert_many_midis_to_wav(filepath, songs)
    dicto = convert_many_midis_to_wav(filepath, songs)
    dicto = convert_many_midis_to_wav(prediction_path, songs)
