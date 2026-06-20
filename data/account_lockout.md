# Account Lockout Policy

## Automatic Lockout Triggers
- 5 consecutive failed login attempts within 10 minutes
- Login attempts from 3+ distinct countries within 1 hour (flagged as potential credential stuffing)
- Manual lockout by account admin (for offboarded employees on team plans)

## Lockout Duration
- First lockout in 30 days: 15-minute automatic cooldown
- Second lockout in 30 days: 1-hour cooldown, email notification sent
- Third+ lockout in 30 days: account frozen, requires identity verification with support

## Identity Verification Process for Frozen Accounts
1. Customer emails support@ from the email on file
2. Support sends a verification code via SMS to the phone number on file
3. If no phone number on file, customer must provide: last 4 digits of payment method, approximate signup date, and one recent invoice number
4. Once verified, support manually unlocks the account

## Security Notes
- Never unlock an account based on email request alone without the verification steps above
- If a customer claims "my account was hacked," this requires immediate escalation — do not attempt to resolve via standard unlock procedure, as the account may need a forced password reset and session invalidation across all devices
