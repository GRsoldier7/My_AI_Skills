# Authenticated live APIs

Prefer an approved same-origin authenticated API. The backend authenticates the
viewer, authorizes each dataset/row/field, runs predefined parameterized queries
with read-only credentials, and returns only the allowed results. Cross-origin
services require an explicit allowed-origin policy; CORS is not authorization.

Public frontend configuration may contain approved endpoint URLs and non-secret
client IDs. Client secrets, database strings, service-account files and reusable
API keys stay server-side. Sign-in uses the organization's approved flow. Keep
short-lived user tokens in memory where feasible; do not persist auth in exported
HTML, browser URLs, logs or localStorage by default.

Define freshness, query timeout, maximum rows/bytes and refresh intervals per
source. Avoid automatic polling until the user has chosen a budget and interval.
Bound result sizes; reject unknown query identifiers and unexpected response
shapes. A denied/failed refresh must show failure and last-success time, not new
synthetic success. Source strings must never become HTML or executable code.

Keep synthetic fixtures for successful, empty, stale, unauthorized, forbidden,
timeout, malformed and truncated responses. Infrastructure creation and real
tenant credentials are outside a reusable library example.
