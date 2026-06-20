# API Authentication Troubleshooting

## Overview
All API requests require a Bearer token in the `Authorization` header:
`Authorization: Bearer <your_api_key>`

## Common 401 Unauthorized Causes

**Expired token**
- Access tokens expire after 24 hours
- Refresh tokens expire after 30 days of inactivity
- Solution: call `/auth/refresh` with a valid refresh token to get a new access token

**Invalid or revoked API key**
- Keys are revoked immediately if flagged for suspicious activity (e.g. requests from new geographic regions at high volume)
- Solution: regenerate the key from Account Settings > API Keys

**Clock drift**
- Requests signed with HMAC will fail if the client's system clock is more than 5 minutes out of sync with server time
- Solution: sync system clock via NTP

**Missing or malformed Authorization header**
- Header must use exact format `Bearer <token>` with a single space
- Common mistake: including quotes around the token, or prefixing with "Token" instead of "Bearer"

## Rate Limiting (429 errors)
- Default rate limit: 100 requests/minute per API key
- Enterprise tier: 1000 requests/minute
- Rate limit headers returned: `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## Escalation Criteria
If a customer reports 401 errors despite a valid, unexpired token and correct header format, this indicates a possible backend auth service issue and should be escalated to the platform engineering on-call.
