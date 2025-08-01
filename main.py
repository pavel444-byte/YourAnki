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

def generate_anki_deck_with_ai(level: str, topic: str, cards_count: int, custom_text: str = "") -> tuple[str, str]:
    """
    Комбо-функция: генерирует карточки через ИИ + создаёт Anki-файл.
    
    Возвращает:
    - путь к .apkg файлу
    - сырой текст карточек (для отображения)
    """

    prompt = f"""
    You are an English vocabulary card generator for Anki.
Your task is to generate cards in the following format:
Word | Meaning: [simple definition]. Example: [usage of word in sentence].

For example:
(Front For Anki) 
Village 
---------------------------------------------------------------------------
___________________________________________________________________________
 Meaning: Village is a very small town. Example: I live in my small village.
(Back For Anki)
Generate {cards_count} cards for the topic "{topic}" at the level "{level}".
."""

    response = client.chat.completions.create(
        model="moonshotai/kimi-k2",
        messages=[{"role": "user", "content": prompt}],
    )

    cards_text = response.choices[0].message.content or ""

    model = genanki.Model(
        model_id=1607392319,
        name='Simple Model',
        fields=[
            {'name': 'Front'},
            {'name': 'Back'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Front}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
            },
        ])

    import uuid
    deck_id = int(uuid.uuid4().int >> 96)
    deck = genanki.Deck(deck_id, f"English {level} - {topic}")

    for line in cards_text.splitlines():
        if ':' in line:
            front, back = line.split(':', 1)
            deck.add_note(genanki.Note(model=model, fields=[front.strip(), back.strip()]))

    file_name = f"anki_{level}_{topic}.apkg"
    genanki.Package(deck).write_to_file(file_name)

    return file_name, cards_text

    

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

cards_count = st.number_input(
    "How many cards do you want to generate?",
    min_value=1,
    max_value=100,
    value=10,  # Default value
    step=1,
)


st.write("This is end but you can write example for your card here:")


if st.button("Generate Anki Cards"):
    if not selected_level or not selected_topic:
        st.error("Please select both level and topic.")
    else:
        with st.spinner("Generating cards using AI and preparing Anki deck..."):
            anki_file, raw_cards = generate_anki_deck_with_ai(selected_level, selected_topic, cards_count)
            st.success("✅ Done! Anki deck is ready.")
            st.code(raw_cards, language="markdown")
            with open(anki_file, "rb") as f:
                st.download_button("📥 Download Anki", f, file_name=anki_file, mime="application/apkg")
                st.write("You can now import this file into Anki to start studying your new flashcards.")
                st.write("Do you have issues or questions? Please, [create an issue on GitHub](https://github.com/pavel444-byte/YourAnki/issues)")
