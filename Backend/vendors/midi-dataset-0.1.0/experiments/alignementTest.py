import matplotlib 
matplotlib.use('Agg') 

import numpy as np
import librosa
import pretty_midi
import joblib
import os
import align_midi
import sys
sys.path.append('..')
import itertools
import json
import alignment_utils

BASE_DATA_PATH = '../data/'
MIDI_PATH = 'clean_midi'
DATASETS = ['cal10k', 'cal500', 'uspop2002', 'msd']
OUTPUT_FOLDER = 'clean_midi_aligned'
AUDIO_FS = 22050
AUDIO_HOP = 512
MIDI_FS = 11025
MIDI_HOP = 256
NOTE_START = 36
N_NOTES = 48


def align_one_file(audio_filename, midi_filename, audio_features_filename=None,
                   midi_features_filename=None, output_midi_filename=None,
                   output_diagnostics_filename=None):
    '''
    Helper function for aligning a MIDI file to an audio file.

    :parameters:
        - audio_filename : str
            Full path to an audio file.
        - midi_filename : str
            Full path to a midi file.
        - audio_features_filename : str or NoneType
            Full path to pre-computed features for the audio file.
            If the file doesn't exist, features will be computed and saved.
            If None, force re-computation of the features and don't save.
        - midi_features_filename : str
            Full path to pre-computed features for the midi file.
            If the file doesn't exist, features will be computed and saved.
            If None, force re-computation of the features and don't save.
        - output_midi_filename : str or NoneType
            Full path to where the aligned .mid file should be written.
            If None, don't output.
        - output_diagnostics_filename : str or NoneType
            Full path to a file to write out diagnostic information (similarity
            matrix, best path, etc) in a .npz file.  If None, don't output.
    '''
    try:
        m = pretty_midi.PrettyMIDI(midi_filename)
    except Exception as e:
        print 'Could not parse {}: {}'.format(
            os.path.split(midi_filename)[1], e)
        return

    cache_midi_cqt = False

    # Cache MIDI CQT
    if midi_features_filename is None or \
            not os.path.exists(midi_features_filename):
        cache_midi_cqt = True
    else:
        try:
            # If a feature file was provided and exists, read it in
            features = np.load(midi_features_filename)
            midi_sync_gram = features['sync_gram']
            midi_beats = features['beats']
            midi_tempo = features['bpm']
        # If there was a problem reading, force re-cration
        except:
            cache_midi_cqt = True

    if cache_midi_cqt:
        # Generate synthetic MIDI CQT
        try:
            midi_audio = alignment_utils.fast_fluidsynth(m, MIDI_FS)
            midi_gram = librosa.cqt(
                midi_audio, sr=MIDI_FS, hop_length=MIDI_HOP,
                fmin=librosa.midi_to_hz(NOTE_START), n_bins=N_NOTES)
            midi_beats, midi_tempo = alignment_utils.midi_beat_track(m)
            midi_sync_gram = alignment_utils.post_process_cqt(
                midi_gram, librosa.time_to_frames(
                    midi_beats, sr=MIDI_FS, hop_length=MIDI_HOP))
        except Exception as e:
            print "Error creating CQT for {}: {}".format(
                os.path.split(midi_filename)[1], e)
            return
        if midi_features_filename is not None:
            try:
                # Write out
                check_subdirectories(midi_features_filename)
                np.savez_compressed(
                    midi_features_filename, sync_gram=midi_sync_gram,
                    beats=midi_beats, bpm=midi_tempo)
            except Exception as e:
                print "Error writing npz for {}: {}".format(
                    os.path.split(midi_filename)[1], e)
                return

    cache_audio_cqt = False
    features = None

    if audio_features_filename is None or \
            not os.path.exists(audio_features_filename):
        cache_audio_cqt = True
    else:
        # If a feature file was provided and exists, read it in
        try:
            features = np.load(audio_features_filename)
            audio_gram = features['gram']
        # If there was a problem reading, force re-cration
        except:
            cache_audio_cqt = True

    # Cache audio CQT
    if cache_audio_cqt:
        try:
            audio, fs = librosa.load(audio_filename, sr=AUDIO_FS)
            audio_gram = librosa.cqt(
                audio, sr=fs, hop_length=AUDIO_HOP,
                fmin=librosa.midi_to_hz(NOTE_START), n_bins=N_NOTES)
        except Exception as e:
            print "Error creating CQT for {}: {}".format(
                os.path.split(audio_filename)[1], e)
            return
        if audio_features_filename is not None:
            try:
                # Write out
                check_subdirectories(audio_features_filename)
                if features is not None:
                    np.savez_compressed(audio_features_filename,
                                        gram=audio_gram, **features)
                else:
                    np.savez_compressed(audio_features_filename,
                                        gram=audio_gram)
            except Exception as e:
                print "Error writing npz for {}: {}".format(
                    os.path.split(audio_filename)[1], e)
                return

    try:
        # Compute onset envelope from CQT (for speed)
        onset_envelope = librosa.onset.onset_strength(
            S=audio_gram, aggregate=np.median)
        _, audio_beats = librosa.beat.beat_track(
            onset_envelope=onset_envelope, bpm=midi_tempo)
        audio_sync_gram = alignment_utils.post_process_cqt(
            audio_gram, audio_beats)
    except Exception as e:
        print "Error syncing CQT for {}: {}".format(
            os.path.split(audio_filename)[1], e)
        return

    try:
        # Get similarity matrix
        similarity_matrix = 1 - np.dot(midi_sync_gram, audio_sync_gram.T)
        # Get best path through matrix
        p, q, score = align_midi.dpmod(similarity_matrix)
        # Normalize score by score by mean sim matrix value within path chunk
        score /= similarity_matrix[p.min():p.max(), q.min():q.max()].mean()
    except Exception as e:
        print "Error performing DTW for {} and {}: {}".format(
            os.path.split(audio_filename)[1],
            os.path.split(midi_filename)[1], e)
        return

    # Write out the aligned file
    if output_midi_filename is not None:
        try:
            # Adjust MIDI timing
            m_aligned = align_midi.adjust_midi(
                m, midi_beats[p], librosa.frames_to_time(audio_beats)[q])
            check_subdirectories(output_midi_filename)
            m_aligned.write(output_midi_filename)
        except Exception as e:
            print "Error writing aligned .mid for {}: {}".format(
                os.path.split(midi_filename)[1], e)
            return

    if output_diagnostics_filename is not None:
        try:
            check_subdirectories(output_diagnostics_filename)
            np.savez_compressed(
                output_diagnostics_filename, p=p, q=q, score=score,
                audio_filename=os.path.abspath(audio_filename),
                midi_filename=os.path.abspath(midi_filename),
                audio_features_filename=os.path.abspath(
                    audio_features_filename),
                midi_features_filename=os.path.abspath(midi_features_filename),
                output_midi_filename=os.path.abspath(output_midi_filename),
                output_diagnostics_filename=os.path.abspath(
                    output_diagnostics_filename))
        except Exception as e:
            print "Error writing diagnostics for {} and {}: {}".format(
                os.path.split(audio_filename)[1],
                os.path.split(midi_filename)[1], e)
            return


# Create the output dir if it doesn't exist

align_one_file("../../LegionsOfTheSerpent.wav", "../../LegionsOfTheSerpent.mid" )