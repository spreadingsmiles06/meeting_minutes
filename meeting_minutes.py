import streamlit as st
import tempfile
import os
from streamlit_mic_recorder import mic_recorder, speech_to_text
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import docx
import io

def save_audio_to_tempfile(audio_bytes):
  # Same as original function

def transcribe_audio(audio_file_path):
  # You'll need a speech recognition service here. Replace this with your preferred solution.

def meeting_minutes(transcription):
  # Here, we'll use Gemini 1.5 Pro for summarization and analysis
  model_name = "google/gemini-1.5-pro"
  tokenizer = AutoTokenizer.from_pretrained(model_name)
  model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

  # Prepare the input
  inputs = tokenizer([transcription], return_tensors="pt")

  # Generate outputs for different sections of the meeting minutes
  abstract_summary_output = model.generate(**inputs)
  abstract_summary = tokenizer.decode(abstract_summary_output[0], skip_special_tokens=True)

  key_points_output = model.generate(**inputs, prompt="Summarize the key points discussed in the meeting.")
  key_points = tokenizer.decode(key_points_output[0], skip_special_tokens=True)

  action_items_output = model.generate(**inputs, prompt="Identify any action items assigned during the meeting.")
  action_items = tokenizer.decode(action_items_output[0], skip_special_tokens=True)

  sentiment_output = model.generate(**inputs, prompt="Analyze the overall sentiment of the meeting discussion (positive, negative, or neutral).")
  sentiment = tokenizer.decode(sentiment_output[0], skip_special_tokens=True)

  return {
      'abstract_summary': abstract_summary,
      'key_points': key_points,
      'action_items': action_items,
      'sentiment': sentiment
  }

def save_as_docx(minutes, filename):
  # Same as original function

def generate_docx_bytes(minutes):
  # Same as original function

def app():
  st.title("Meeting Minutes Generator")

  # Get Gemini API key (assuming you have a mechanism to store/retrieve it securely)
  # Replace with your method of obtaining the API key
  gemini_api_key = st.text_input("Enter your Gemini API Key:", type="password", key="gemini_api_key_input")

  # Record audio using the microphone
  st.write("Record the meeting:")
  audio_bytes = mic_recorder(start_prompt="Start Recording", stop_prompt="Stop Recording", key='recorder')

  if audio_bytes:
      try:
          # Save the audio to a temporary file
          audio_file_path = save_audio_to_tempfile(audio_bytes)

          # Transcribe the audio (replace with your solution)
          transcription_text = transcribe_audio(audio_file_path)

          # Display the transcription text
          st.subheader("Transcription")
          st.write(transcription_text)

          # Generate meeting minutes using Gemini
          minutes = meeting_minutes(transcription_text)

          # Display the meeting minutes
          st.header("Meeting Minutes")

          # Abstract Summary
          st.subheader("Abstract Summary")
          st.write(minutes['abstract_summary'])

          # Key Points
          st.subheader("Key Points")
          for point in minutes['key_points'].split('\n'):
              st.write(f"- {point.strip()}")

          # Action Items
          st.subheader("Action Items")
          for item in minutes['action_items'].split('\n'):
              st.write(f"- {item.strip()}")

          # Sentiment
          st.subheader("Sentiment of Meeting")
          st.write(minutes['sentiment'])

          # Generate the Word document as a byte stream
          docx_bytes = generate_docx_bytes(minutes)

          # Download button
          st.download_button(
              label="Download Meeting Minutes",
              data=docx_bytes.getvalue(),
              file_name="Meeting_Minutes.docx",
              mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document
