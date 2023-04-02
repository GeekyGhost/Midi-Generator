import random
import tkinter as tk
from tkinter import filedialog
from midiutil.MidiFile import MIDIFile

def create_midi_file():
    midi = MIDIFile(2)

        # Define the Circle of Fifths
    circle_of_fifths = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Db', 'Ab', 'Eb', 'Bb', 'F']
    circle_of_fifths_minor = ['Am', 'Em', 'Bm', 'F#m', 'C#m', 'G#m', 'D#m', 'Bbm', 'Fm', 'Cm', 'Gm', 'Dm']

    # Choose a random key from the Circle of Fifths
    key_index = random.randint(0, len(circle_of_fifths) - 1)
    key = circle_of_fifths[key_index]
    minor_key = circle_of_fifths_minor[key_index]

    # Define the I, IV, V, and vi chords for the chosen key
    chords_major = [circle_of_fifths[key_index], 
                    circle_of_fifths[(key_index + 3) % 12], 
                    circle_of_fifths[(key_index + 5) % 12]]

    chords_minor = [circle_of_fifths_minor[key_index],
                    circle_of_fifths_minor[(key_index + 3) % 12],
                    circle_of_fifths_minor[(key_index + 5) % 12]]

    # Create a chord progression
    progression = chords_major + [random.choice(chords_minor)]

    midi.addTrackName(0, 0, "Right Hand")
    midi.addTrackName(1, 0, "Left Hand")
    midi.addTempo(0, 0, 120)

    right_notes = [60, 62, 64, 65, 67, 69, 71]
    left_notes = [48, 50, 52, 53, 55, 57, 59]

    try:
        duration = float(duration_entry.get())
    except ValueError:
        duration = 1  # Default duration

    total_time = 0
    initial_right_chord = random.choice(right_notes)
    initial_left_chord = random.choice(left_notes)

    while total_time < duration:
        note = initial_right_chord + random.choice([-2, -1, 0, 1, 2])
        midi.addNote(0, 0, note, total_time, 1, 100)
        total_time += 1

    total_time = 0

    while total_time < duration:
        note = initial_left_chord + random.choice([-2, -1, 0, 1, 2])
        midi.addNote(1, 0, note, total_time, 1, 100)
        total_time += 1

    file_path = filedialog.asksaveasfilename(defaultextension=".mid", filetypes=[("MIDI files", "*.mid")])

    if file_path:
        with open(file_path, "wb") as output_file:
            midi.writeFile(output_file)

# Create the tkinter window and configure it
window = tk.Tk()
window.title("MIDI File Generator")
window.geometry("300x150")

# Add an entry to input the desired duration
duration_label = tk.Label(window, text="Duration (seconds):")
duration_label.pack()
duration_entry = tk.Entry(window)
duration_entry.pack()

# Add a button to create the MIDI file
create_button = tk.Button(window, text="Create MIDI File", command=create_midi_file)
create_button.pack(pady=20)

# Run the tkinter main loop
window.mainloop()
