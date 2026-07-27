# Security

## Educational history note

Previous commits in this repository were early educational experiments and may show
patterns that are unsuitable for secure software. The current tree intentionally
replaces those patterns. History has not been rewritten, so anyone reviewing old
commits should treat them as obsolete and avoid copying their implementation.

## Current controls

- Only fictional, synthetic portfolio content is accepted.
- API credentials are read only from the process environment.
- No credential entry field, password retrieval, sensitive database output, or raw
  provider-error display exists.
- Input length, knowledge-file size, chunk length, and retrieval count are bounded.
- Empty questions and obvious hidden-configuration requests are rejected.
- Retrieved text is labeled untrusted in optional model instructions.
- Responses are grounded in retrieved context and include source references.
- CI uses read-only repository permissions and does not call external AI services.
- The container runs as a non-root user.

These are defense-in-depth measures, not proof against prompt injection or other
attacks.

## Data policy

Do not add real company names, branding, operational terminology, customer or
employee information, real addresses, phone numbers, payment data, credentials,
access codes, or confidential information. Do not submit sensitive user input.

## Known limitations

This portfolio has no accounts, authentication, authorization, rate limits,
conversation persistence, security monitoring, content moderation, or production
support process. Dependency scans find known issues only and can produce false
negatives. Retrieval quality and generated answers are not guaranteed.

Please report a suspected vulnerability privately to the repository owner rather
than including sensitive details in a public issue.
