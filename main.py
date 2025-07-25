import streamlit as st
import anki
from openai import OpenAI
import colorama
import pandas as pd
import numpy as np
import requests

english_levels = ["Beginner", "Elementary", "Intermediate", "Upper Intermediate", "Advanced", "Proficient"]
selected_level = st.selectbox(
    "Select your English level:",
    english_levels,
    index=None,
    placeholder="Choose your level...",
)

st.write("You selected:", selected_level)
