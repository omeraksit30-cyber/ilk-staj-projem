"""Bounded parser for the fictional Markdown knowledge base."""

import re
from pathlib import Path

from .models import KnowledgeChunk


class KnowledgeBaseError(ValueError):
    """Raised when knowledge-base input is missing or unsafe to process."""


def _bounded_parts(text: str, limit: int) -> list[str]:
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    result: list[str] = []
    current = ""
    for paragraph in paragraphs:
        if len(paragraph) > limit:
            raise KnowledgeBaseError(
                "A knowledge-base paragraph exceeds the chunk limit."
            )
        candidate = f"{current}\n\n{paragraph}".strip()
        if current and len(candidate) > limit:
            result.append(current)
            current = paragraph
        else:
            current = candidate
    if current:
        result.append(current)
    return result


def load_knowledge_base(
    path: Path, *, max_file_size: int, max_chunk_length: int
) -> tuple[KnowledgeChunk, ...]:
    try:
        size = path.stat().st_size
    except OSError as exc:
        raise KnowledgeBaseError("The knowledge base is unavailable.") from exc
    if size <= 0 or size > max_file_size:
        raise KnowledgeBaseError("The knowledge-base size is outside safe limits.")

    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise KnowledgeBaseError("The knowledge base cannot be read.") from exc

    sections = re.split(r"(?m)^##\s+", content)
    chunks: list[KnowledgeChunk] = []
    for raw_section in sections[1:]:
        title, _, body = raw_section.partition("\n")
        title = " ".join(title.split())
        if not title or not body.strip():
            continue
        for index, part in enumerate(_bounded_parts(body, max_chunk_length), start=1):
            suffix = f" (part {index})" if len(body.strip()) > max_chunk_length else ""
            chunks.append(KnowledgeChunk(section=f"{title}{suffix}", text=part))
    if not chunks:
        raise KnowledgeBaseError("The knowledge base contains no usable sections.")
    return tuple(chunks)
