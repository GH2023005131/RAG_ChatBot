---
title: "Pre-commit & CI Setup"
status: implemented
priority: high
---

## Summary

Set up automated quality checks via pre-commit hooks and GitLab CI.

## Requirements

- Linting: ruff
- Formatting: ruff-format
- Type checking: mypy + pyrefly
- Security: bandit + detect-secrets
- Dependency audit: pip-audit
- Testing: pytest with coverage
- Changelog automation: git-cliff
- All checks run in GitLab CI pipeline

## Implementation

- `.pre-commit-config.yaml` — 8 hooks
- `.gitlab-ci.yml` — 10 CI jobs across 7 stages
- `pyproject.toml` — Tool configurations
- `cliff.toml` — Changelog generation config

## Files

- `.pre-commit-config.yaml`
- `.gitlab-ci.yml`
- `pyproject.toml`
- `cliff.toml`
