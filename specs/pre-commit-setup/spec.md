# Pre-commit & CI Setup

## Summary

Set up automated quality checks via pre-commit hooks and GitLab CI pipeline.

## Requirements

- Linting: ruff
- Formatting: ruff-format
- Type checking: mypy + pyrefly
- Security: bandit + detect-secrets
- Dependency audit: pip-audit
- Testing: pytest with coverage reporting
- Changelog automation: git-cliff
- All checks run in GitLab CI pipeline

## Technical Approach

Use pre-commit framework with hooks from public repos. Configure tools via `pyproject.toml`. GitLab CI runs the same checks in parallel stages.

## Acceptance Criteria

- [x] 8 pre-commit hooks configured and passing
- [x] GitLab CI pipeline with 10 jobs across 7 stages
- [x] All tool configs in `pyproject.toml`
- [x] Changelog generation with `cliff.toml`

## Files

- `.pre-commit-config.yaml`
- `.gitlab-ci.yml`
- `pyproject.toml`
- `cliff.toml`
