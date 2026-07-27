# Testing

The suite is deterministic, local, and designed not to contact OpenAI or any external
service.

```bash
python -m pytest
ruff check .
ruff format --check .
python -m pip_audit
docker build -t restaurant-support-assistant .
```

Coverage includes knowledge loading, deterministic ranking, relevant and unrelated
questions, validation bounds, retrieval-count limits, automatic local mode, safe
provider failure, source references, prompt-injection-style input, and a current-tree
scan for selected real-company and credential patterns.

Optional generation uses an injected fake Responses API client. No network mocking is
needed because a real client is never created in those tests.

The security scan is a regression check, not a substitute for code review, secret
scanning, dependency maintenance, or a professional security assessment.
