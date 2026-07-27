import re
from pathlib import Path

TEXT_SUFFIXES = {
    ".md",
    ".py",
    ".toml",
    ".yml",
    ".yaml",
    ".example",
    ".dockerignore",
    ".gitignore",
}
EXCLUDED_PARTS = {".git", ".pytest_cache", ".ruff_cache", "__pycache__"}
REAL_COMPANY_NAMES = (
    "mcdon" + "ald",
    "burger" + " king",
    "star" + "bucks",
    "k" + "fc",
)
CREDENTIAL_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"(?i)(password|api[_ -]?key)\s*[:=]\s*[\"'][^\"']+[\"']"),
)


def current_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        if path.name in {".dockerignore", ".gitignore", ".env.example"}:
            yield path
        elif path.suffix in TEXT_SUFFIXES:
            yield path


def test_real_company_names_and_credentials_are_absent():
    root = Path(__file__).parents[1]
    for path in current_text_files(root):
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        assert not any(name in lowered for name in REAL_COMPANY_NAMES), path
        assert not any(pattern.search(text) for pattern in CREDENTIAL_PATTERNS), path
