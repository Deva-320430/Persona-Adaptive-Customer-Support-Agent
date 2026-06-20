# User Management Guide

## Roles and Permissions
- **Admin**: full account access, billing, can add/remove users
- **Manager**: can manage team members and view reports, no billing access
- **Member**: standard access to core features, no admin functions

## Adding Users
1. Admin navigates to Settings > Team > Invite Member
2. Enter email address; an invite link is sent (valid for 7 days)
3. New user sets their own password upon accepting the invite
4. Seats are billed immediately upon invite acceptance, not upon sending the invite

## Removing Users
- Removing a user immediately revokes all active sessions
- Data created by the removed user (reports, configs) remains in the account, ownership transfers to the account Admin
- Seat count updates at the next billing cycle, not immediately (no prorated refund for early removal)

## Common Issues

**Invite link expired**
- Resend a new invite; old links cannot be reactivated

**User can't see a feature they should have access to**
- Check their role matches the feature's required permission level
- Some features are plan-gated (e.g. advanced analytics is Professional+ only) regardless of role
