"""Streamlit entry point for the Restaurant Support Knowledge Assistant."""

from pathlib import Path

import streamlit as st

from restaurant_support_assistant.config import Settings
from restaurant_support_assistant.generation import answer_question
from restaurant_support_assistant.knowledge import (
    KnowledgeBaseError,
    load_knowledge_base,
)
from restaurant_support_assistant.retrieval import (
    QuestionValidationError,
    TfidfRetriever,
    validate_question,
)

APP_ROOT = Path(__file__).resolve().parent


@st.cache_resource
def build_retriever(settings: Settings) -> TfidfRetriever:
    chunks = load_knowledge_base(
        APP_ROOT / "data" / "knowledge_base.md",
        max_file_size=settings.max_knowledge_base_bytes,
        max_chunk_length=settings.max_chunk_length,
    )
    return TfidfRetriever(chunks)


def main() -> None:
    settings = Settings()
    st.set_page_config(page_title="Restaurant Support Knowledge Assistant")
    st.title("Restaurant Support Knowledge Assistant")
    st.caption("Educational portfolio software using fictional information only.")
    st.warning(
        "Answers may be incomplete or incorrect. Do not use this application for "
        "real restaurant operations or sensitive information."
    )

    try:
        retriever = build_retriever(settings)
    except KnowledgeBaseError:
        st.error("The fictional knowledge base could not be loaded safely.")
        return

    mode = (
        "Optional AI-assisted mode" if settings.ai_enabled else "Local retrieval mode"
    )
    st.info(f"Active mode: {mode}")
    question = st.text_area(
        "Ask about the fictional restaurant support information",
        max_chars=settings.max_question_length,
        placeholder="For example: What is the reservation policy?",
    )

    if st.button("Find answer", type="primary"):
        try:
            normalized = validate_question(question, settings.max_question_length)
            result = answer_question(normalized, retriever, settings)
        except QuestionValidationError as exc:
            st.error(str(exc))
            return

        st.subheader("Answer")
        st.write(result.answer)
        if result.sources:
            st.subheader("Retrieved source sections")
            for source in result.sources:
                with st.expander(source.reference):
                    st.write(source.text)


if __name__ == "__main__":
    main()
