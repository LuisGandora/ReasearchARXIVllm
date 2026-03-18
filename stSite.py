import streamlit as st
#import GeminiBot as gb

#gemini_bot gb = geminiBot()

st.set_page_config(page_title="AI Researcher", layout="centered")

st.title("AI Researcher (Sponsored by ARXIV jk)")

st.header("How does our bot works?")
st.text_area("Our Gemini AI Bot accepts one research topic and then scours ARXIV using their API (https://info.arxiv.org/help/api/basics.html) Utilizing that one research topic, our AI bot will search for relevent papers and generate research ideas for you to use" )

user_input = st.chat_input("Input a research topic here: ")

#for debugging:
if(user_input):
    st.write(user_input + " HelloWorld")

# if(user_input):
    # gb.run_agent command

