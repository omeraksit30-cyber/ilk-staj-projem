"""Deterministic TF-IDF retrieval over bounded fictional content."""

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .models import KnowledgeChunk, RetrievedChunk

SENSITIVE_REQUEST = re.compile(
    r"\b(environment variables?|system prompt|api key|secret|password|credential|"
    r"hidden configuration|access code|filesystem path)\b",
    re.IGNORECASE,
)


class QuestionValidationError(ValueError):
    """Raised for empty, oversized, or sensitive-input requests."""


def validate_question(question: str, max_length: int) -> str:
    normalized = " ".join(question.split())
    if not normalized:
        raise QuestionValidationError("Enter a non-empty question.")
    if len(normalized) > max_length:
        raise QuestionValidationError(
            f"Question exceeds the {max_length}-character limit."
        )
    if SENSITIVE_REQUEST.search(normalized):
        raise QuestionValidationError(
            "Requests for hidden configuration, prompts, paths, or secrets "
            "are not allowed."
        )
    return normalized


class TfidfRetriever:
    def __init__(self, chunks: tuple[KnowledgeChunk, ...]) -> None:
        if not chunks:
            raise ValueError("At least one chunk is required.")
        self._chunks = chunks
        self._vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            stop_words="english",
            strip_accents="unicode",
            sublinear_tf=True,
        )
        self._matrix = self._vectorizer.fit_transform(
            f"{chunk.section} {chunk.text}" for chunk in chunks
        )

    def retrieve(self, question: str, *, top_k: int) -> tuple[RetrievedChunk, ...]:
        bounded_top_k = min(max(top_k, 1), len(self._chunks))
        query = self._vectorizer.transform([question])
        scores = cosine_similarity(query, self._matrix).ravel()
        ranked = sorted(enumerate(scores), key=lambda item: (-item[1], item[0]))[
            :bounded_top_k
        ]
        return tuple(
            RetrievedChunk(chunk=self._chunks[index], score=float(score))
            for index, score in ranked
            if score > 0
        )
