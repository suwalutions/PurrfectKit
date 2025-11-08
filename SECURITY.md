# Security Policy — PurrfectKit

We take security **extremely seriously**.

## Supported Versions

| Version   | Security Updates | Notes                         |
|-----------|------------------|-------------------------------|
| `>=0.2.0` | Yes              | All versions on PyPI          |
| `<0.2.0`  | No               | Too ancient for modern cats   |

> We patch **all maintained versions** within **24 hours** of a confirmed vulnerability.

## Reporting a Vulnerability

**DO NOT open public issues for security bugs.**

A message on GitHub:
[@KHARAPSY](https://github.com/KHARAPSY) (private message)

### What we promise:
- **Response within 6 hours** (even on weekends — cats don’t sleep)
- **Fix within 24 hours** for critical issues
- **Public credit** in release notes (unless you prefer anonymity)

### What to include:
- Package version
- Steps to reproduce
- Exploit code (if any)
- Impact (RCE? Data leak? DoS?)
- Your name/handle (for credit)

### Security Features:
- All OCR engines run in isolated Docker containers by default
- No network calls unless explicitly enabled
- Secrets scanned with `detect-secrets` on every commit
- Dependencies locked with `uv lock`
- CI runs `bandit` + `safety` on every push

### Disclosure Policy
1. You report → we respond in ≤6h
2. We fix → you test → we merge
3. We release patch → same day
4. We credit you → forever
