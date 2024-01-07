import os
import dotenv

import streamlit as st
from openai import OpenAI
import requests
import pandas as pd
from io import StringIO
from createexperts import * 

# os.environ["OPENAI_API_KEY"] = "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"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # if the key already exists in the environment variables, it will use that, otherwise it will use the .env file to get the key
if not OPENAI_API_KEY:
    dotenv.load_dotenv(".env")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def main():
  if 'uploaded_button_clicked' not in st.session_state:
    st.session_state['uploaded_button_clicked'] = False
  if 'messages' not in st.session_state:
    st.session_state['messages'] = []
  if 'thread' not in st.session_state:
     st.session_state['thread'] = None
  if 'assistant' not in st.session_state:
     st.session_state['assistant'] = None


  domain_expert_value = st.slider('Domain Expert', 0, 5, 2)
  engineer_value = st.slider('Software Engineer', 0, 5, 2)
  designer_value = st.slider('UX/UI Designer', 0, 5, 2)
  pm_value = st.slider('Product Manager', 0, 5, 2)
  roles = [domain_expert_value, engineer_value, designer_value, pm_value]

  uploaded_rubric = st.file_uploader("You can your own custom rubric as a text file in comma-separate value format. Otherwise the default rubric below will be used.", 
                                  type=["txt"], 
                                  accept_multiple_files=False,
                                  label_visibility='visible')
  if uploaded_rubric:
    bytes_data = uploaded_rubric.read()
    st.write(bytes_data)

    with open(os.path.join(os.getcwd(), "rubric.txt"),"wb") as f: 
        f.write(bytes_data)

  rubric_df = pd.read_csv('/Users/stellajia/Desktop/Professional/ai-earth-hack/ai_earth_hack/sample-rubric.csv')
  st.write(rubric_df)
  
  uploaded_ideas = st.file_uploader("You can upload a CSV file with ideas to be evaluated.", 
                                  type=["csv"], 
                                  accept_multiple_files=False,
                                  label_visibility='visible')
  
  
  
  if uploaded_ideas is not None:
    # Read the file with pandas
    df = pd.read_csv(uploaded_ideas, encoding='latin-1')
    short_df = df.head(5) #TOGGLE: can switch this to adjust number of ideas
    st.text('Content of uploaded CSV file: ')
    # Show the content of the CSV file
    st.write(short_df)
    
  # Evaluate the CSV file
  
    ## Sample rubric
    sample_rubric = """
    Originality, Idea has common elements with no unique differentiation. (1), Idea shows some novel thinking and differentiation. (2), Idea is largely original, showing significant new thinking. (3), Idea is completely unique demonstrating groundbreaking thinking. (4)
    Feasibility, Idea has significant practical or technical obstacles. (1), Idea is somewhat practical but faces notable challenges. (2), Idea is fairly practical with manageable challenges. (3), Idea is highly practical and can be implemented smoothly. (4)
    Impact, Idea has a limited or unclear impact. (1), Idea has a moderate impact with some tangible benefits. (2), Idea has a significant impact with clear benefits. (3), Idea has a transformative impact with far-reaching benefits. (4)
    Development & Research, Idea is underdeveloped with minimal research or supporting data. (1), Idea is somewhat developed with some research or supporting data. (2), Idea is well-developed with substantial research or supporting data. (3), Idea is fully developed with extensive research or supporting data. (4)
    Scalability, Idea shows little to no potential for growth or adaptation. (1), Idea shows some potential for growth or adaptation. (2), Idea shows considerable potential for growth or adaptation. (3), Idea shows extensive potential for growth or adaptation. (4)
    """
    st.text('Ideas evaluated: ')
    new_df = process_dataframe_with_evaluation(short_df, sample_rubric, OPENAI_API_KEY)
    st.dataframe(new_df)

  
                          
