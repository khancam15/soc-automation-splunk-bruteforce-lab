# Security Policy

## Scope and Intended Use

This repository is for authorized cybersecurity lab use only.

- Use only in isolated, controlled environments.
- Do not target production, public, or third-party systems.
- Do not use real user credentials or sensitive organizational data.

## Supported Security Practices

The project follows these baseline practices:

- Secrets are excluded from version control.
- Lab credentials should be rotated after demos.
- Evidence should be reviewed for sensitive data before publishing.
- Detection and automation changes should be peer reviewed via pull requests.

## Reporting a Vulnerability

If you discover a security issue in this repository:

1. Do not open a public issue containing exploit details.
2. Report privately to the repository owner via GitHub profile contact.
3. Include reproduction steps, affected files, and suggested remediation.

## Sensitive Data Handling

Before committing:

- Remove or redact API tokens, passwords, hostnames, and private IPs where needed.
- Review screenshots and logs for credentials or internal details.
- Confirm generated case notes do not include prohibited data.

## Responsible Disclosure Expectations

- Provide reasonable time for remediation before public disclosure.
- Share only the minimum necessary technical detail to verify the issue.
