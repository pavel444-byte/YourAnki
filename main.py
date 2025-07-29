import streamlit as st
import anki
from openai import OpenAI
import colorama
import pandas as pd
import numpy as np
import requests

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
