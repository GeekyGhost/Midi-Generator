import tempfile
import os
import gradio as gr
import numpy as np
import random
from music21 import stream, chord, note, midi, environment
from music21 import tempo as tempo_module
from music21 import duration

def diatonic_chords(key):
    scale = ["C", "D", "E", "F", "G", "A", "B"]
    tonic_index = scale.index(key.capitalize())
    chords = []
    for i in range(7):
        chords.append(chord.Chord([scale[(tonic_index + i) % 7], scale[(tonic_index + i + 2) % 7], scale[(tonic_index + i + 4) % 7]]))
    return chords

def substitute_chord(chords, index, new_chord):
    chords[index] = chord.Chord(new_chord)

def modulation(chords, key1, key2):
    diatonic_chords_key2 = diatonic_chords(key2)
    for i in range(len(chords)):
        if chords[i].root.name == key1:
            substitute_chord(chords, i, diatonic_chords_key2[i % 7].pitches)
            
def generate_progression(key, substitutions, modulations):
    chords = diatonic_chords(key)
    if substitutions:
        substitute_chord(chords, 2, ["G", "B-", "D", "F"])
        substitute_chord(chords, 4, ["F", "A-", "C", "E"])
    if modulations:
        modulation(chords, key, "G")
        modulation(chords, "G", "D")
        modulation(chords, "D", key)
    return chords

def create_midi_file(key, substitutions, modulations, tempo, song_duration):
    s = stream.Stream()

    # Check if tempo is a valid integer; if not, set to 120
    try:
        tempo = int(tempo)
    except ValueError:
        tempo = 120

    # Set the tempo
    tempo_obj = tempo_module.MetronomeMark(number=tempo)
    s.insert(0, tempo_obj)

    beats_per_minute = tempo
    beats_per_second = beats_per_minute / 60

    note_durations = ["whole", "half", "quarter", "eighth", "16th", "32nd"]
    note_duration_values = {"whole": 4, "half": 2, "quarter": 1, "eighth": 0.5, "16th": 0.25, "32nd": 0.125}
    
    total_duration = 0

    while total_duration < song_duration:
        # Follow the diatonic chord progression for chord progressions
        chords = generate_progression(key, substitutions, modulations)

        for c in chords:
            # Randomly choose a note duration type
            note_duration_type = random.choice(note_durations)
            note_duration_value = note_duration_values[note_duration_type]

            c.duration = duration.Duration(note_duration_type)
            s.append(c)

            total_duration += note_duration_value * 60 / tempo

    midi_file = midi.translate.streamToMidiFile(s)
    midi_data = midi_file.writestr()

    return midi_data

def play_midi(inputs):
    key, substitutions, modulations, tempo, song_duration = inputs
    midi_data = create_midi_file(key, substitutions, modulations, tempo, song_duration)
    return midi_data

def generate_midi(key, substitutions, modulations, tempo, song_duration):
    midi_data = play_midi(inputs = (key, substitutions, modulations, tempo, song_duration))
    # Save MIDI data to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".midi") as temp_file:
        temp_file.write(midi_data)
        temp_file_path = temp_file.name

    return temp_file_path


chord_options = [
    "C", "D", "E", "F", "G", "A", "B"
]

song_duration_input = gr.inputs.Slider(minimum=30, maximum=240, step=1, default=120, label="Song Duration (seconds)")

iface = gr.Interface(
    fn=generate_midi,
    inputs=[
        gr.components.Dropdown(choices=chord_options, label="Key"),
        gr.inputs.Checkbox(label="Use Chord Substitutions"),
        gr.inputs.Checkbox(label="Use Modulations"),
        gr.inputs.Number(default=120, label="Tempo (BPM)"),
        song_duration_input
    ],
    outputs=gr.outputs.File(label="Generated MIDI"),
    title="MIDI Generator",
    description="Generate a random MIDI file based on the key and settings you select.",
    examples=[["C", True, False, 120, 120]]
)

iface.launch()

