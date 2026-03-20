import os
import time
import streamlit as st

import gemini_bot as gb #gemini bot we made

#Streamlit secrets are basically streamlits env format, in the website it is given but in this local project
#You need to create a .streamlit/secrets.toml
#Load secrets from secrets.toml
os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_KEY"]
os.environ["Project_Id"] = st.secrets["PROJECTID"]

researchAgent = gb.googleChat()

st.set_page_config(page_title="AI Researcher", layout="centered")

st.title("AI Researcher (Powered by ARXIV)")

st.header("How does our bot works?")
st.write("Our Gemini AI Bot accepts one research topic and then scours ARXIV using their API (https://info.arxiv.org/help/api/basics.html) Utilizing that one research topic, our AI bot will search for relevent papers and generate research ideas for you to use" )
st.write("---------------------")
user_input = st.chat_input("Input a research topic to generate new ideas from prexisting papers: ")

try:
    start = time.perf_counter()
    response = researchAgent.run_agent(user_input)
    end = time.perf_counter()
    st.write(f"AI: {response}")
    st.write("---------------------")
    st.write(f"Total time to run: {end-start}")
except Exception as e:
    st.write(f"Error with trying to run agent {str(e)}")

