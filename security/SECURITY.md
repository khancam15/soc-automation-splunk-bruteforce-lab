# Security Practices for Lab and GitHub Deployment

This file defines the security baseline for running this lab and publishing it to GitHub.

## 1. Lab Security Practices

- Use only authorized and isolated lab environments.
- Do not test against production, public, or third-party systems.
- Use test-only accounts and non-sensitive data.
- Keep attacker and target traffic on lab-only network segments.
- Use least-privilege accounts for Splunk and automation access.

## 2. Secret and Data Protection

Before every commit and push:

- Never store passwords, API tokens, or private keys in repo files.
- Keep secrets in local environment variables only.
- Redact usernames, internal IPs, hostnames, and tokens in screenshots.
- Review query outputs and generated notes for sensitive data exposure.

## 3. Secure GitHub Deployment Practices

- Push from clean branches with reviewed changes.
- Keep commits small and descriptive.
- Verify `.gitignore` patterns are active before adding files.
- Run secret checks before push.
- Enable branch protections on `main`:
	- Require pull requests
	- Require review approval
	- Require status checks

## 4. Minimum Pre-Push Checklist

- `git status` is clean except intended files.
- No secrets in staged content.
- No accidental artifacts (`.DS_Store`, archives, temp files).
- Documentation matches current repository structure.
- Screenshots are sanitized.

## 5. Vulnerability Reporting

If a security issue is found:

1. Do not disclose exploit details publicly.
2. Report privately to the repository owner via GitHub profile contact.
3. Include affected files, reproduction steps, and impact summary.
