import tempfile
import os
import gradio as gr
import numpy as np
import random
from music21 import stream, chord, note, midi, environment
from music21 import tempo as tempo_module
from music21 import duration

def circle_of_fifths(chords):
    circle = ["C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#", "F"]
    chord_indices = [circle.index(ch) for ch in chords]
    progression = [circle[(idx + 7) % len(circle)] for idx in chord_indices]
    return progression

def create_midi_file(chords, tempo, song_duration):
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
        # Follow the Circle of Fifths for chord progressions
        chords = circle_of_fifths(chords)

        for chord_name in chords:
            # Randomly choose a note duration type
            note_duration_type = random.choice(note_durations)
            note_duration_value = note_duration_values[note_duration_type]

            c = chord.Chord(chord_name)
            c.duration = duration.Duration(note_duration_type)
            s.append(c)

            total_duration += note_duration_value * 60 / tempo

    return s

def play_midi(chords, tempo, song_duration):
    midi_stream = create_midi_file(chords, tempo, song_duration)
    midi_file = midi.translate.streamToMidiFile(midi_stream)
    midi_data = midi_file.writestr()

    return midi_data

def generate_midi(chord1, chord2, chord3, chord4, tempo, song_duration):
    chords = [chord1, chord2, chord3, chord4]
    midi_data = play_midi(chords, tempo, song_duration)

    # Save MIDI data to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".midi") as temp_file:
        temp_file.write(midi_data)
        temp_file_path = temp_file.name

    return temp_file_path

chord_options = [
    "C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#", "F"
]

song_duration_input = gr.inputs.Slider(minimum=30, maximum=240, step=1, default=120, label="Song Duration (seconds)")

iface = gr.Interface(
    fn=generate_midi,
    inputs=[
        gr.components.Dropdown(choices=chord_options, label="Chord 1"),
        gr.components.Dropdown(choices=chord_options, label="Chord 2"),
        gr.components.Dropdown(choices=chord_options, label="Chord 3"),
        gr.components.Dropdown(choices=chord_options, label="Chord 4"),
        gr.inputs.Number(default=120, label="Tempo (BPM)"),
        song_duration_input
    ],
    outputs=gr.outputs.File(label="Generated MIDI"),
    title="MIDI Generator",
    description="Generate a random MIDI file based on the chords and tempo you select.",
    examples=[["C", "Am", "F", "G", 120, 120]]
)

iface.launch()
