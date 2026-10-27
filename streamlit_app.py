import hashlib
import logging
import uuid
from pathlib import Path

import streamlit as st

from app.document_service import prepare_embeddings
from app.pipeline import prepare_chunks
from app.search import ask_question


st.set_page_config(
    page_title="EvidenceDesk",
    page_icon=":material/menu_book:",
    layout="wide",
)

st.title("EvidenceDesk")
st.write("Upload a PDF, ask questions, and inspect the supporting passages.")

# Keep document preparation and answers across page reruns.
st.session_state.setdefault("workspace_id", uuid.uuid4().hex)
st.session_state.setdefault("selected_document", None)
st.session_state.setdefault("prepared_chunks", None)
st.session_state.setdefault("active_embeddings", None)
st.session_state.setdefault("result", None)

uploaded_file = st.file_uploader(
    "Choose a text-based PDF",
    type=["pdf"],
    max_upload_size=5,
    key="document_upload",
)

if uploaded_file is None:
    st.session_state["selected_document"] = None
    st.session_state["prepared_chunks"] = None
    st.session_state["active_embeddings"] = None
    st.session_state["result"] = None

    st.info("Upload a PDF to begin.")
    st.stop()


pdf_bytes = uploaded_file.getvalue()

# Check the file size in Python as well.
if len(pdf_bytes) > 5 * 1024 * 1024:
    st.error("Please use a PDF smaller than 5 MB.")
    st.stop()

# Identify the document using its contents and filename.
document_id = hashlib.sha256(
    pdf_bytes + uploaded_file.name.encode("utf-8")
).hexdigest()

# Selecting a different document clears the previous answer and active search.
if st.session_state["selected_document"] != document_id:
    st.session_state["selected_document"] = document_id
    st.session_state["prepared_chunks"] = None
    st.session_state["active_embeddings"] = None
    st.session_state["result"] = None

document_folder = (
    Path("data/uploads")
    / st.session_state["workspace_id"]
    / document_id
)

embeddings_path = document_folder / "embedded_chunks.json"

st.caption(f"Selected document: {uploaded_file.name}")


# This button performs local processing only.
if st.button("1. Read PDF and preview chunks"):
    try:
        document_folder.mkdir(parents=True, exist_ok=True)

        # Use a fixed disk filename rather than trusting an uploaded path.
        pdf_path = document_folder / "document.pdf"
        pdf_path.write_bytes(pdf_bytes)

        chunks = prepare_chunks(pdf_path)

        for chunk in chunks:
            chunk["document_name"] = uploaded_file.name

        # Keep the learning demo small before making paid requests.
        if len(chunks) > 60:
            raise ValueError(
                "This demo supports up to 60 chunks. Please use a shorter PDF."
            )

        st.session_state["prepared_chunks"] = chunks

    except Exception:
        logging.exception("PDF preparation failed")
        st.error(
            "Could not prepare this PDF. Use a readable, text-based "
            "document that produces no more than 60 chunks."
        )


chunks = st.session_state["prepared_chunks"]

if chunks is not None:
    st.success(f"Prepared {len(chunks)} chunks. No embedding API calls yet.")

    with st.expander("Preview the first chunk"):
        st.text(chunks[0]["text"])

    st.caption(
        "Creating embeddings sends the extracted text to OpenAI "
        "and uses API credit. Completed matching chunks are reused."
    )

    # Paid preparation happens only after this explicit click.
    if st.button("2. Create embeddings", key=f"embed_{document_id}"):
        try:
            with st.spinner("Preparing searchable embeddings..."):
                records = prepare_embeddings(chunks, embeddings_path)

            if len(records) != len(chunks):
                raise ValueError("Document preparation is incomplete")

            st.session_state["active_embeddings"] = str(embeddings_path)
            st.session_state["result"] = None

        except Exception:
            logging.exception("Embedding preparation failed")
            st.error(
                "Embedding preparation failed. Check the terminal for details. "
                "Completed records were saved; you can retry."
            )


active_path = st.session_state["active_embeddings"]

if active_path is None:
    st.info("Read the PDF, then create its embeddings to enable questions.")
    st.stop()

st.success("This document is ready for questions.")

with st.form("question_form"):
    question = st.text_input(
        "Your question",
        placeholder="What does this document say about accidents?",
        max_chars=1000,
    )
    submitted = st.form_submit_button("Find answer")


if submitted:
    st.session_state["result"] = None

    if not question.strip():
        st.warning("Enter a question first.")
    elif len(question) > 1000:
        st.warning("Please keep the question under 1,000 characters.")
    else:
        try:
            with st.spinner("Finding evidence and generating an answer..."):
                result = ask_question(
                    question,
                    embeddings_path=Path(active_path),
                )

            st.session_state["result"] = result

        except Exception:
            logging.exception("Question answering failed")
            st.error(
                "The request could not be completed. "
                "Check the terminal for details."
            )


result = st.session_state["result"]

if result is not None:
    st.subheader("Question")
    st.write(result["question"])

    st.subheader("Answer")
    st.write(result["answer"])

    st.subheader("Retrieved evidence")
    st.caption(
        "Similarity is not a confidence percentage. "
        "Check the passages to verify the answer."
    )

    for source in result["sources"]:
        label = (
            f"[Source {source['source_number']}] "
            f"{source['document_name']} | "
            f"Page {source['page_number']} | "
            f"Chunk {source['chunk_number']}"
        )

        with st.expander(label):
            st.text(source["text"])
            st.caption(f"Similarity: {source['score']:.4f}")