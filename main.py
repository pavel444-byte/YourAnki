import os
import streamlit as st
import genanki
import anki  # This import seems to be unused, consider removing it if not needed
from openai import OpenAI
import colorama
import pandas as pd
import numpy as np
import requests
import json
import subprocess
import uuid
from dotenv import load_dotenv  
# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url="https://openrouter.ai/api/v1")


# Initialize Streamlit app
st.set_page_config(page_title="Anki Card Generator", page_icon=":book:", layout="wide")
st.title("Anki Card Generator")
st.write("Welcome to the Anki Card Generator! This app helps you create Anki flashcards based on your English learning level and topics of interest.")







english_levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
st.write("Note: For more infromation about english levels, please visit [this link](https://en.wikipedia.org/wiki/Common_European_Framework_of_Reference_for_Languages).")
selected_level = st.selectbox(
    "Select your English level:",
    english_levels,
    index=None,
    placeholder="Choose your level...",
)

st.write("You selected:", selected_level)

english_topics = ["Math", "Technology", "Politics", "Family", "Kids", "Animals", "Food", "Travel", "Health", "Education"]
selected_topic = st.selectbox(
    "Select a topic to learn about:",
    english_topics,
    index=None,
    placeholder="Choose a topic...",
)
st.write("You selected:", selected_topic)
anki_file_type = "apkg"
anki_file_name = f"anki_{selected_level}_{selected_topic}.{anki_file_type}"
st.write("Anki file name:", anki_file_name)




st.write("This is end but you can write example for your card here:")
example_text = st.text_area("Example text for your card:", height=200)

st.button("Generate Anki Cards", key="generate_cards")
if st.button("Generate Anki Cards"):
    if selected_level and selected_topic == None:
        st.error("Please select both your English level and a topic.")
    else:
        st.success("Generating Anki cards...")
        # Here you would call your function to generate the Anki cards
        # For example:
        # generate_anki_cards(selected_level, selected_topic, example_text)
        generate_anki()
def generate_anki():

    model = ""




