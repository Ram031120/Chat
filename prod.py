import streamlit as st
import os
import pandas as pd
import google.generativeai as genai

# Load API Key directly
genai.configure(api_key="your_actual_api_key_here")  # Replace with your actual Gemini API key

# Function to read data from files
def load_data_from_folder(folder_path):
    data_frames = {}
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if file.endswith(".csv"):
            data_frames[file] = pd.read_csv(file_path)
        elif file.endswith(".xlsx"):
            data_frames[file] = pd.read_excel(file_path)
    return data_frames

# Function to process user query
def generate_response(user_input, data_frames):
    context = ""
    for file, df in data_frames.items():
        context += f"Data from {file}:\n{df.head().to_string()}\n"
    
    prompt = f"""
    You are an AI chatbot designed to assist merchandisers and production personnel. 
    Use a friendly and helpful tone. 
    Given the following data:
    {context}
    Answer the user's query: {user_input}
    """
    
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    
    return response.text.strip()

# Streamlit UI
st.title("Merchandising & Production Chatbot")

folder_path = "/Users/anil/Dropbox/My Mac (Anil-MacBook-Air.local)/Desktop/Teck packs"

if st.button("Load Data"):
    data = load_data_from_folder(folder_path)
    st.session_state["data"] = data
    st.success("Data loaded successfully!")

if "data" in st.session_state:
    user_input = st.text_input("Ask a question about the data:")
    if st.button("Get Response"):
        response = generate_response(user_input, st.session_state["data"])
        st.write("Response:", response)
