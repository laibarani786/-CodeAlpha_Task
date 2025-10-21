import streamlit as st
import os
from music21 import stream, note, midi
import random
import matplotlib.pyplot as plt

# ----------------------- PAGE CONFIG -----------------------
st.set_page_config(page_title="🎵 AI Music Generation", layout="centered")

# ----------------------- STYLING -----------------------
st.markdown("""
    <style>
        body {
            background-color: #fdfdfd;
        }
        .title {
            text-align: center;
            font-size: 40px;
            font-weight: 700;
            color: #2c3e50;
            background: -webkit-linear-gradient(45deg, #ff5f6d, #ffc371);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            text-align: center;
            color: #555;
            font-size: 18px;
            margin-bottom: 30px;
        }
        .footer {
            text-align: center;
            color: #888;
            font-size: 14px;
            margin-top: 40px;
        }
        .stButton>button {
            background-color: #ff5f6d !important;
            color: white !important;
            border-radius: 12px !important;
            border: none;
            font-size: 16px;
            font-weight: 600;
            padding: 10px 24px;
        }
        .stButton>button:hover {
            background-color: #ff7f50 !important;
            transform: scale(1.03);
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------- HEADER -----------------------
st.markdown('<p class="title">🎶 AI Music Generation Studio</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Generate melodies, visualize notes & listen instantly!</p>', unsafe_allow_html=True)
st.write("---")

# ----------------------- MIDI FOLDER HANDLING -----------------------
base_dir = os.path.dirname(os.path.abspath(__file__))
midi_folder = os.path.join(base_dir, "midi song")

if not os.path.exists(midi_folder):
    os.makedirs(midi_folder)
    st.warning("⚠️ Folder 'midi song' was missing, so I created it. Please add your .mid files inside it and refresh the app.")
    st.stop()

midi_files = [f for f in os.listdir(midi_folder) if f.endswith(".mid")]

if not midi_files:
    st.warning("⚠️ No MIDI files found in 'midi song' folder. Please add some .mid files and refresh.")
    st.stop()

# ----------------------- FILE SELECTION -----------------------
selected_file = st.selectbox("🎵 Select a MIDI song to inspire new music:", midi_files)

# ----------------------- GENERATE MUSIC -----------------------
if st.button("✨ Generate New Music"):
    st.write(f"🎧 Generating melody inspired by: **{selected_file}**")

    melody = stream.Stream()
    pitches = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    durations = [0.25, 0.5, 1.0]

    # Generate random melody
    for _ in range(24):
        n = note.Note(random.choice(pitches))
        n.quarterLength = random.choice(durations)
        melody.append(n)

    # Save generated music
    output_path = os.path.join(base_dir, "generated_music.mid")
    mf = midi.translate.streamToMidiFile(melody)
    mf.open(output_path, 'wb')
    mf.write()
    mf.close()

    st.success("✅ Music generated successfully! 🎶 Now you can visualize & listen to it below:")

    # ---------------- VISUALIZE NOTES ----------------
    fig, ax = plt.subplots(figsize=(9, 3))
    y = [pitches.index(n.name) + 1 for n in melody.notes]
    x = range(len(y))
    ax.plot(x, y, marker='o', linestyle='-', color="#ff5f6d")
    ax.set_yticks(range(1, len(pitches) + 1))
    ax.set_yticklabels(pitches)
    ax.set_xlabel("Note Index", fontsize=12)
    ax.set_ylabel("Pitch", fontsize=12)
    ax.set_title("🎼 Melody Visualization", fontsize=14, fontweight='bold')
    st.pyplot(fig)

    # ---------------- PLAYBACK + DOWNLOAD ----------------
    try:
        st.audio(output_path, format='audio/midi')
    except:
        st.warning("⚠️ Your browser may not support direct MIDI playback, but you can download it below.")

    with open(output_path, "rb") as f:
        st.download_button(
            label="⬇️ Download Generated MIDI File",
            data=f,
            file_name="generated_music.mid",
            mime="audio/midi",
            use_container_width=True
        )

st.write("---")
st.markdown('<p class="footer">Developed by Laiba 🎵 | Powered by Streamlit</p>', unsafe_allow_html=True)
