import streamlit as st
import requests
import os

API_BASE_URL = "http://127.0.0.1:8000"

def upload_file(file):
    files = {"file": (file.name, file.getvalue())}
    response = requests.post(f"{API_BASE_URL}/upload/", files=files)
    return response.json()

def analyze_file(query, filename):
    data = {"query": query, "filename": filename}
    response = requests.post(f"{API_BASE_URL}/analyze/", json=data)
    return response.json()

# Streamlit UI
st.title("Document Analyser")

uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])
if uploaded_file:
    st.write(f"Uploaded file: {uploaded_file.name}")
    upload_response = upload_file(uploaded_file)
    
    if "filename" in upload_response:
        filename = upload_response["filename"]
        st.success("File uploaded successfully!")
        
        query = st.text_input("Enter your query:")
        if st.button("Analyze"):
            if query:
                response = analyze_file(query, filename)
                response_text = response.get("response", {}).get("text") or response.get("response", {}).get("choices", [{}])[0].get("message", {}).get("content", "No response received.")
                st.subheader("Response:")
                st.write(response_text)
            else:
                st.warning("Please enter a query.")
    else:
        st.error("File upload failed.")
