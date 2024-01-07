# define meta information of the app
import streamlit as st

def meta():
    st.set_page_config(page_icon="⚗️", page_title="Omnigpt", layout="wide") # or layout='centered'
    st.write("# Idea Validator for Circular Economy Business Ideas")

    # Hide the made with Streamlit footer
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Hide the specific class of deploy and connect to streamlit.io
    st.markdown(
        """
        <style>
            .st-emotion-cache-zq5wmm.ezrtsby0 {
                display: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # st.write("Relevent Keywords:", keywords)
    # new_expert = st.text_input('Add new expert:', '')
    # experts = []
    # if st.button('Add expert'):
    #     have_it = new_expert.lower() in experts
    #     'Expert has already been added!' if have_it else 'Added!'
    #     if not have_it:
    #         experts.append(new_expert)
    # st.write("Experts:", str(experts))
    # st.button("Generate Score", type="primary")
