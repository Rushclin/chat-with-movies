import os
import tempfile
import streamlit as st
from embedchain import App

def embedchain_bot(db_path, api_key):
    return App.from_config(
        config={
            "llm": {"provider": "openai", "config": {"api_key": api_key}},
            "vectordb": {"provider": "chroma", "config": {"dir": db_path}},
            "embedder": {"provider": "openai", "config": {"api_key": api_key}},
        }
    )

st.title("Chat with MOVIES")

openai_access_token = "sk-proj-HYN6sPRhauxZCjhqjaWwT3BlbkFJvFmZYKHPM6DCvIDVOgsE"

pdf_file_path = "./data_test.pdf"

if openai_access_token:
    db_path = tempfile.mkdtemp()
    app = embedchain_bot(db_path, openai_access_token)

    try:
        with open(pdf_file_path, "rb") as pdf_file:
            pdf_content = pdf_file.read()
            st.write("Le fichier PDF a été chargé avec succès.")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
                f.write(pdf_content)
                app.add(f.name, data_type="pdf_file")
            os.remove(f.name)
            st.success("Fichier PDF ajouté à la base de connaissances !")
    except FileNotFoundError:
        st.write("Le fichier PDF spécifié n'existe pas dans le répertoire.")

    prompt = st.text_input("Ask a question about the PDF")

    if prompt:
        answer = app.chat(prompt)
        st.write(answer)
