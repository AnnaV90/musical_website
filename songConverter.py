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


class ProcessSongs():

    def __init__(self, songs_directory):
        self.file_path = songs_directory
        self.songs = os.listdir(self.file_path)
        self.midis = self.filter_midi(self.songs)
        # self.api_call("Avengers.mid", "Tests_music/")

    def api_call(self, song_file, directory, length=500, randomness=1):
        """api call -> takes in a song filepath and uses the api
            to write it out in a directory"""
        print(song_file)
        if song_file.split("/")[1] in os.listdir(directory):
            print("removing previously predicted song")
            print("song_file: ")
            print(song_file.split("/")[1])
            os.remove(directory + song_file.split("/")[1])

        file_data = subprocess.Popen([
            'curl', '-X', 'POST',
            f'https://api-image-3-2b76463dxa-ew.a.run.app/uploadfile/?prediction_length={length}&randomness={randomness}',
            "-H", 'accept: application/json', "-H",
            'Content-Type: multipart/form-data', "-F",
            f'file=@{song_file};type=audio/mid'
        ], stdout=subprocess.PIPE)

        (out, err) = file_data.communicate()
        # song_file = song_file.split("/")[1]
        print(out)
        print(err)
        with open(f'{directory}/{song_file}', 'wb') as test_midi:
            test_midi.write(out)


    def filter_midi(self, songs):
        midis = []
        for song in songs:
            if song.endswith('mid'):
                midis.append(song)
        return midis




    def midi_to_wav(self, song):
        sequence = note_seq.midi_file_to_note_sequence(song)
        p = note_seq.plot_sequence(sequence, show_figure=False)
        if str(song[:-3] + 'wav') in songs and str(song[:-3] +
                                                'wav') in predicted_songs:

            return str(song[:-3] + 'wav'), p

        note_seq.sequence_proto_to_midi_file(sequence, song)
        array = note_seq.synthesize(sequence, 22000)
        length_array = int(len(array))
        s = song[:-3] + 'wav'
        write(s, 22000, array.astype(np.float32)[:length_array])
        return s, p


    def convert_many_midis_to_wav(self, fp, songs_path):
        """path of many midis in a list"""
        dict_song = {}
        midis = self.filter_midi(songs_path)
        for i in midis:
            try:
                dict_song[i] = [*self.midi_to_wav(fp + i)]
            except:
                # os.remove(f"{fp}{i}")
                # os.remove(f"{filepath}{i}")
                print(f"Converting {i} failed :S")
        return dict_song


    def song_predict(self, fp, songs_path, length=500, randomness=1):
        midis = self.filter_midi(songs_path)
        for song in midis:
            self.api_call(fp + song, length, randomness)


if __name__ == "__main__":
    processing_songs = ProcessSongs(filepath)
    for song in predicted_songs:
        try:
            processing_songs.midi_to_wav(prediction_path + song)
        except:
            print(song)
