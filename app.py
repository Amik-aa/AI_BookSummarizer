import streamlit as st
import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize
import os

# Downloading necessary NLTK resources
nltk.download('punkt')

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    return text

# Function to split text into chunks
def chunk_text(text, chunk_size=2000):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []

    for sentence in sentences:
        if len(" ".join(current_chunk)) + len(sentence) < chunk_size:
            current_chunk.append(sentence)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def summarize_text(text):
    return text[:300] + "..." 

# Streamlit UI
st.title("📚 AI-Powered Book Summarizer")
st.write("Upload a PDF book to generate a concise summary.")

# File upload
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.success("File uploaded successfully!")

    # Save uploaded file temporarily
    temp_pdf_path = "temp_uploaded_book.pdf"
    with open(temp_pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    # Extract and process text
    book_text = extract_text_from_pdf(temp_pdf_path)
    text_chunks = chunk_text(book_text)

    # Generate summaries
    summaries = [summarize_text(chunk) for chunk in text_chunks]
    final_summary = " ".join(summaries)

    # Display Summary
    st.subheader("📖 Summary")
    st.write(final_summary)

    # Clean up temporary file
    os.remove(temp_pdf_path)
