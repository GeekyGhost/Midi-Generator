# Midi-Generator

#Included 2 examples of output. You'll notice it's not very good at the moment. That part hopefully comes later lol. 

#Notes: Made with significant help from chatGPT4. Running the included .bat file will create the venv and install the requirements as well as run the main .py script to launch the UI. You just have to cntrl click the link in the cmd window to launch the Gradio UI. Also there's two main scripts and you can use whichever you like, just update the .bat file with the one you want to run. Slightly different UIs and functions. 

This is a work in progress and mainly a test for something else, but working on this helps me with that lol. 

Generating Midi files randomly based on user input. Test UI and functions for a different project. 

Prerequisites
Before you can run the script, you need to make sure you have the following software installed on your Windows computer:

Python 3.7 or later
pip package manager
Git
Installation
To install the script and its dependencies, follow these steps:

Open the Command Prompt by typing cmd in the Start menu search bar and pressing Enter.
Clone the script's repository by running the following command: git clone https://github.com/GeekyGhost/Midi-Generator.git.
Navigate to the directory where the repository was cloned by running the following command: cd YOUR_REPOSITORY (replace YOUR_REPOSITORY with the name of the repository).
Install the required packages by running the following command: pip install -r requirements.txt.
Usage
To use the script, follow these steps:

Open the Command Prompt and navigate to the directory where the script is located.
Run the script by running the following command: python script_name.py (replace script_name with the name of the script file).
The GUI for the MIDI generator will open in your web browser. Use the dropdown menus to select four chords, the tempo (in BPM), and the song duration (in seconds).
Click the "Generate MIDI" button to generate a MIDI file based on your selections.
The generated MIDI file will be downloaded automatically to your Downloads folder. You can open it with any MIDI player or music production software that supports the MIDI format.
Troubleshooting
If you encounter any issues while installing or using the script, try the following:

Make sure you have installed all the required software and packages.
Check that you have an active internet connection, as the script uses the internet to download some dependencies.
If you encounter any error messages, try searching online for a solution or asking for help on a programming forum or community. Be sure to include the full error message in your search or post for better results.


The circle_of_fifths function is used to generate a chord progression based on the circle of fifths, which is a common progression in music. The create_midi_file function creates a MIDI file based on the chord progression, tempo, and song duration. The play_midi function uses the create_midi_file function to create a MIDI file and plays it. The generate_midi function takes four chords, tempo, and song duration as input, generates a MIDI file using the play_midi function, and saves it to a temporary file.

The gradio library is used to create a graphical user interface (GUI) for the MIDI generator. The GUI includes four dropdown menus for selecting chords, a number input for selecting the tempo, and a slider input for selecting the song duration. The output is a generated MIDI file, which is displayed as a file download link.
