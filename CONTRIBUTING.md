# Contributing

Thanks for your interest in improving this lab project.

## Ground Rules

- Keep all testing and simulation activity in authorized, isolated lab environments.
- Never commit secrets, credentials, or sensitive internal data.
- Keep pull requests focused to one logical change.

## Development Workflow

1. Create a branch from main.
2. Make your change in small, reviewable commits.
3. Update documentation and evidence when detection logic changes.
4. Run local checks before opening a pull request.
5. Open a pull request using the repository template.

## Branch and Commit Conventions

- Branch names:
  - feat/<short-description>
  - fix/<short-description>
  - docs/<short-description>
  - chore/<short-description>
- Commit style:
  - feat: add threshold tuning notes
  - fix: correct event field name
  - docs: update walkthrough screenshots
  - chore: improve repo hygiene

## Pull Request Expectations

Include the following:

- What changed
- Why it changed
- Validation evidence (query output, screenshots, or logs)
- Any security considerations

## Security Requirements

- Use environment variables for tokens and passwords.
- Redact screenshots and outputs before publishing.
- If you discover a vulnerability, follow SECURITY.md.
