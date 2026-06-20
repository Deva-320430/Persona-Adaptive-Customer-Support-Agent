# Network Troubleshooting

## Connectivity Checklist
1. Confirm the customer can reach `status.example.com` (rules out a total outage)
2. Check if the issue is specific to one network (corporate firewall/proxy blocking our domains)
3. Confirm required domains/ports are allowlisted: `api.example.com:443`, `ws.example.com:443`

## Common Network Issues

**Requests timing out**
- Check if customer is behind a corporate proxy that may strip or modify headers
- Confirm DNS resolution is correct: `nslookup api.example.com`
- Default request timeout is 30 seconds; long-running operations should use the async job endpoint instead

**WebSocket connection drops**
- Corporate firewalls frequently block WebSocket upgrade requests even when HTTPS works fine
- Recommend falling back to polling mode via `?transport=polling` query parameter as a workaround
- Persistent drops every ~60 seconds usually indicate an idle timeout on a load balancer or proxy between the customer and us

**SSL/TLS certificate errors**
- Verify customer's system date/time is correct (common cause of false cert errors)
- We rotate TLS certificates automatically; no customer action needed for routine rotation
- If error persists and is reproducible, escalate to platform engineering as a potential certificate misconfiguration on our end
