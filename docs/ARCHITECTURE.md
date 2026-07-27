# Architecture

## Purpose and boundaries

The application is a small educational retrieval system for fictional restaurant
support content. `app.py` owns presentation. The
`restaurant_support_assistant` package owns configuration, bounded knowledge parsing,
retrieval, domain models, and grounded answer generation.

## Request flow

1. `Settings` reads typed process-environment values and enforces ranges.
2. `load_knowledge_base` checks file size, decodes UTF-8, splits Markdown sections,
   and rejects paragraphs that exceed the configured chunk bound.
3. `TfidfRetriever` builds an in-memory TF-IDF matrix and ranks chunks with cosine
   similarity. Stable score/index ordering makes retrieval deterministic.
4. `validate_question` normalizes whitespace, rejects empty or oversized questions,
   and blocks direct requests for hidden configuration or secrets.
5. `answer_question` applies a relevance threshold. With insufficient context it
   returns an explicit refusal to infer details.
6. Local mode displays grounded text and references. Optional AI mode supplies only
   bounded context and the question to the Responses API. Any provider exception is
   suppressed and local output is used.

## Trust boundaries

User questions and knowledge-base text are untrusted. Neither can authorize access to
environment values, prompts, paths, or secrets. The only optional secret is read by
the OpenAI SDK from typed process configuration and is never included in a model
prompt or output.

The knowledge base is bundled static data, not a content-management system. There is
no database, authentication, authorization, user account, or conversation storage.
