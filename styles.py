import streamlit as st

def apply_styles():
    """Apply custom styles to the Streamlit app."""
    st.markdown("""
        <style>
        .stButton > button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border-radius: 5px;
            border: none;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        .stProgress > div > div > div > div {
            background-color: #4CAF50;
        }
        .stDataFrame {
            margin-top: 20px;
            margin-bottom: 20px;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 30px;
        }
        .stAlert {
            padding: 10px;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)
