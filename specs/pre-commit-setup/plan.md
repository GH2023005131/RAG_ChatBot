# Pre-commit & CI Setup — Implementation Plan

## Step 1: Tool Configuration

Configure ruff, mypy, pyrefly, pytest, and coverage in `pyproject.toml`.

## Step 2: Pre-commit Hooks

Add hooks for ruff, mypy, pyrefly, pyupgrade, bandit, detect-secrets, pytest.

## Step 3: CI Pipeline

Create `.gitlab-ci.yml` with lint, format, type_check, security, dependency_audit, changelog, test, and coverage stages.

## Step 4: Changelog Automation

Configure `cliff.toml` for conventional commit parsing and changelog generation.

## Dependencies

- pre-commit, ruff, mypy, pyrefly, pyupgrade, bandit, detect-secrets, pip-audit, pytest, pytest-cov, git-cliff

## Risks

- Tool version compatibility
- CI runner availability
