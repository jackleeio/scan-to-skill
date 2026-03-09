# Slug Parsing Rules

Supported decoded QR payloads:

1. Plain slug
- `skill-feed`
- `scan-to-skill`

2. ClawHub URLs
- `https://clawhub.ai/skill-feed`
- `https://clawhub.ai/owner/skill-feed`
- `https://www.clawhub.com/owner/skill-feed`

3. Install command text
- `clawhub install skill-feed`

Parsing precedence:

1. If text contains `clawhub install <slug>`, use `<slug>`.
2. Else if text is URL, extract last path segment as slug.
3. Else if text matches slug pattern (`[a-z0-9][a-z0-9-]*`), use as slug.
4. Otherwise mark as unsupported and request manual confirmation.

Validation:

- Lowercase only
- `a-z`, `0-9`, `-`
- Length 2-64
