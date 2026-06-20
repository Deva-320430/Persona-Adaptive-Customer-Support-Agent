# Security Best Practices

## API Key Management
- Never share API keys via email, chat, or support tickets — support staff will never ask for a full key
- Rotate keys at least every 90 days
- Use separate keys for development and production environments
- Restrict keys by IP allowlist where possible (available on Professional+ plans)

## Account Security
- Enable two-factor authentication (2FA) via Settings > Security
- Review active sessions periodically under Settings > Security > Active Sessions
- Logging out of all devices is available as an emergency action if account compromise is suspected

## Reporting a Suspected Compromise
If a customer suspects their account has been compromised:
1. Immediately force-invalidate all sessions (do this before anything else)
2. Require a password reset on next login
3. Review recent account activity logs with the customer for unrecognized actions
4. Rotate any API keys associated with the account
5. This entire flow should be escalated to the security team for review, even after immediate containment steps are taken, since root cause (e.g. phishing, credential reuse) needs investigation

## Data Privacy
- Customer data is encrypted at rest (AES-256) and in transit (TLS 1.2+)
- Data deletion requests are processed within 30 days per our data retention policy
- We do not sell customer data to third parties
