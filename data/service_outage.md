# Service Outage Procedures

## Status Page
All outages are posted to status.example.com within 5 minutes of detection, with severity classified as:
- **Minor**: degraded performance, no data loss, affects under 5% of users
- **Major**: feature unavailable, affects 5-50% of users
- **Critical**: full service outage or data integrity risk, affects over 50% of users

## SLA Commitments
- 99.5% uptime guaranteed for Professional and Enterprise plans
- Credits issued automatically for downtime exceeding SLA: 1 day of service credit per hour of qualifying downtime
- Starter plan has no formal SLA but outages are still tracked and communicated

## What to Tell Customers During an Active Outage
- Acknowledge the issue without speculating on root cause
- Direct them to the status page for live updates
- Do not provide an ETA unless one has been officially confirmed by engineering and posted to the status page
- For Enterprise customers asking about business impact, reference the SLA credit policy above

## Post-Outage
- A post-mortem is published within 5 business days for any Major or Critical incident
- Customers significantly impacted should be proactively informed of SLA credits rather than waiting for them to ask

## Escalation Criteria
Any customer reporting data loss (not just unavailability) during an outage must be escalated immediately to the incident commander, regardless of plan tier.
