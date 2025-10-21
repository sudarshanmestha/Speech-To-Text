import streamlit as st
import whisper
import datetime
import re
import os
from tempfile import NamedTemporaryFile

model = whisper.load_model("tiny") # Change to "base", "small", etc. as needed

def format_time(seconds):
    return str(datetime.timedelta(seconds=int(seconds)))

def split_sentences(text):
    return re.split(r'(?<=[.?!])\s+', text.strip())

st.title("🎙️ Audio Transcriber")
st.write("Upload an audio file and transcribe with speaker labeling and timestamps.")

audio_file = st.file_uploader("Upload Audio", type=["mp3", "wav", "m4a"])

if audio_file:
    with NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(audio_file.read())
        tmp_path = tmp_file.name

    st.info("Transcribing... please wait ⏳")
    result = model.transcribe(tmp_path)

    transcript_lines = []

    for i, seg in enumerate(result["segments"]):
        start = format_time(seg["start"])
        end = format_time(seg["end"])
        text = seg["text"].strip()
        speaker = "Interviewer" if "?" in text or text.lower().startswith((
            "can you", "what", "how", "tell me", "do you", "did you", "why", "please", "explain", "have you", "could you"
        )) else "Candidate"

        for sentence in split_sentences(text):
            formatted_line = f"[{start} - {end}] {speaker}: {sentence}"
            st.markdown(f"**{formatted_line}**")
            transcript_lines.append(formatted_line)

    # Save transcript to a text file in the project folder
    output_path = os.path.join(os.getcwd(), "transcript_output.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        for line in transcript_lines:
            f.write(line + "\n")

    st.success(f"Transcript saved to {output_path}")

st.markdown("---")
st.caption("Built with ❤️ by Jana")
