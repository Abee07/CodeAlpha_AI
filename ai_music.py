import glob
import numpy as np
import tensorflow as tf
from music21 import converter, instrument, note, chord, stream
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# --- STEP 1: READ A SUBFOLDER OF MIDI FILES ---
notes = []
subfolder_name = "my_songs" 

# This links the paths together to target only that specific subfolder
folder_path = f"C:\\Users\\Abhinaya\\OneDrive\\Documents\\CodeAlpha_AI\\CodeAlpha_music\\{subfolder_name}\\*.mid"
midi_files = glob.glob(folder_path)

if len(midi_files) == 0:
    print(f"❌ ERROR: No MIDI files found in the subfolder: '{subfolder_name}'!")
    print("Please check the folder name spelling and make sure it has .mid files inside.")
    exit()

print(f"📂 Found {len(midi_files)} MIDI files inside '{subfolder_name}'. Reading them now...")

# Loop through every single file in the subfolder
for file in midi_files:
    try:
        print(f"Parsing: {file}")
        midi = converter.parse(file)
        
        parts = instrument.partitionByInstrument(midi)
        if parts: 
            notes_to_parse = parts.parts.recurse()
        else: 
            notes_to_parse = midi.flat.notes

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))
                
    except Exception as e:
        print(f"⚠️ Skipping file {file} due to an error: {e}")

print(f"\n✅ SUCCESS! Gathered a total of {len(notes)} musical events.")

# --- STEP 2: PREPARE THE DATA FOR THE AI ---
# Get all unique sounds (notes and chords)
pitches = sorted(list(set(notes)))
n_vocab = len(pitches)

# Create dictionaries to map notes to numbers and back
note_to_int = {note: number for number, note in enumerate(pitches)}
int_to_note = {number: note for number, note in enumerate(pitches)}

# Slice the music into windows (Look at 30 notes to predict the 31st)
sequence_length = 30
network_input = []
network_output = []

for i in range(0, len(notes) - sequence_length):
    seq_in = notes[i:i + sequence_length]
    seq_out = notes[i + sequence_length]
    network_input.append([note_to_int[char] for char in seq_in])
    network_output.append(note_to_int[seq_out])

n_patterns = len(network_input)

# Format the math data for the LSTM network
X = np.reshape(network_input, (n_patterns, sequence_length, 1))
X = X / float(n_vocab)  # Normalize data between 0 and 1
Y = tf.keras.utils.to_categorical(network_output, num_classes=n_vocab)


# --- STEP 3: BUILD THE DEEP LEARNING MODEL ---
print("Building the neural network...")
model = Sequential([
    LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True),
    Dropout(0.3),
    LSTM(256),
    Dropout(0.3),
    Dense(n_vocab, activation='softmax')
])

model.compile(loss='categorical_crossentropy', optimizer='adam')


# --- STEP 4: TRAIN THE AI ---
print("Training the AI on your file patterns...")
# Run for 30 epochs to build a basic understanding. Use 100+ epochs for better music.
model.fit(X, Y, epochs=100, batch_size=64)


# --- STEP 5: GENERATE A NEW SONG ---
print("Generating new musical sequences...")
# Start with a random seed sequence from your own MIDI data
start_idx = np.random.randint(0, len(network_input)-1)
pattern = network_input[start_idx]
prediction_output = []

# Ask the AI to write 100 new notes
for note_index in range(100):
    prediction_input = np.reshape(pattern, (1, len(pattern), 1))
    prediction_input = prediction_input / float(n_vocab)
    
    # Predict the probabilities for the next note
    prediction = model.predict(prediction_input, verbose=0)
    
    # Use creative sampling instead of just picking the highest score
    prediction = np.log(prediction + 1e-7) / 1.0
    exp_preds = np.exp(prediction)
    prediction = exp_preds / np.sum(exp_preds)
    index = np.random.choice(range(n_vocab), p=prediction[0])
    
    result = int_to_note[index]
    prediction_output.append(result)
    
    # Slide our data window forward by 1 note
    pattern.append(index)
    pattern = pattern[1:len(pattern)]


# --- STEP 6: CONVERT NUMBERS BACK TO MIDI FILE ---
print("Saving your new song to disk...")
output_notes = []

for pattern in prediction_output:
    # If the note is a chord (multiple notes played together)
    if ('.' in pattern) or pattern.isdigit():
        notes_in_chord = pattern.split('.')
        chord_notes = []
        for current_note in notes_in_chord:
            new_note = note.Note(int(current_note))
            new_note.storedInstrument = instrument.Piano()
            chord_notes.append(new_note)
        new_chord = chord.Chord(chord_notes)
        output_notes.append(new_chord)
    # If it is a single note
    else:
        new_note = note.Note(pattern)
        new_note.storedInstrument = instrument.Piano()
        output_notes.append(new_note)

# Save the notes list into a new MIDI file
midi_stream = stream.Stream(output_notes)
midi_stream.write('midi', fp='ai_generated_output.mid')

print("🎉 DONE! Look for 'ai_generated_output.mid' in your script folder.")

