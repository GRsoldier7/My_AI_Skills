# Acceptance checklist

- Source identity, capture/as-of times, metric definitions and dependency hosts are visible.
- Correct numbers, preserved leading zeros/dates, missing/invalid columns and row limits.
- Empty, loading, stale, network failure, denied/expired auth and truncated-query states.
- Every control works by pointer and keyboard; focus and labels visible.
- Desktop and 320–390px screenshots inspected; no accidental overflow.
- Accessible table/text equivalents; reduced motion; print behavior when applicable.
- Export content matches visible data and is safe to open in a spreadsheet.
- Untrusted HTML/code is rendered as text; no leaked secrets or private fixtures.
- Offline mode makes zero requests; live mode uses only approved endpoints.
- Secure embed fallback works; authorization is server-enforced and read-only.
- Actual-host tests and simulated checks are reported separately.
