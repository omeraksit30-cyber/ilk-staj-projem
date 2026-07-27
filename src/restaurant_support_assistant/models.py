"""Domain models shared by retrieval and generation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class KnowledgeChunk:
    section: str
    text: str

    @property
    def reference(self) -> str:
        return f"Knowledge base — {self.section}"


@dataclass(frozen=True)
class RetrievedChunk:
    chunk: KnowledgeChunk
    score: float


@dataclass(frozen=True)
class Source:
    reference: str
    text: str


@dataclass(frozen=True)
class Answer:
    answer: str
    sources: tuple[Source, ...]
    used_ai: bool = False
