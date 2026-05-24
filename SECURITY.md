# Security Policy

## Please report privately

**Do not open public GitHub issues** for:

- Security vulnerabilities (injection, auth bypass, data exposure, etc.)
- Exposed secrets or API keys found in the repo or deployments
- Authentication or session issues that could affect users

Public issues make it easier for others to exploit problems before a fix is ready.

## Contact

Email: **tranguyeenn2007@gmail.com**

Please include **`[ShelfTxt Security]`** in the subject line so the report is easy to find.

Example:

```txt
[ShelfTxt Security] Exposed API key in deployment config
```

## What to include

When possible:

- What you found and where (URL, file path, commit)
- Steps to reproduce
- Impact you believe it has
- Your timezone if you are open to follow-up questions

You should receive an acknowledgment within a reasonable timeframe. Critical issues will be prioritized.

## Scope

ShelfTxt is a personal library app with a CSV-backed API and hosted frontend. Reports about misconfiguration on your own fork, or social engineering, are still welcome but may be out of scope for this repo.

## Safe harbor

Good-faith security research that avoids harming users or destroying data will not be pursued as hostile action. Please do not test against production without permission.

## Supported versions

Security fixes apply to the default branch (`main`) and the live deployment described in [docs/deployment.md](docs/deployment.md). Older forks are unsupported.
