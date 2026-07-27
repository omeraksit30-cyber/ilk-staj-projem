from restaurant_support_assistant.knowledge import load_knowledge_base


def test_fictional_knowledge_base_loads(knowledge_path):
    chunks = load_knowledge_base(
        knowledge_path, max_file_size=100_000, max_chunk_length=1_500
    )
    assert len(chunks) >= 8
    assert all(chunk.text and len(chunk.text) <= 1_500 for chunk in chunks)
    assert "fictional" in knowledge_path.read_text(encoding="utf-8").lower()
