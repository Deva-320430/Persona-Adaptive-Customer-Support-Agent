# Deployment Guide

## Supported Deployment Methods
- Managed cloud (default): fully hosted, automatic updates
- Self-hosted via Docker: customer manages infrastructure, monthly update images provided
- On-premise (Enterprise only): air-gapped deployment with quarterly update packages

## Docker Deployment Steps
1. Pull the latest image: `docker pull example/platform:latest`
2. Configure environment variables in `.env` (DATABASE_URL, API_SECRET, REDIS_URL required)
3. Run migrations: `docker run example/platform:latest migrate`
4. Start the service: `docker compose up -d`
5. Verify health check at `/health` returns 200

## Common Deployment Issues

**Container fails to start**
- Check that all required environment variables are set
- Verify the database is reachable from the container network
- Check logs with `docker logs <container_id>` for the specific startup error

**Migrations fail partway through**
- Do not retry migrations blindly; this can corrupt schema state
- Restore from the pre-migration backup, then contact support with the migration log before retrying

**Custom middleware / third-party integration questions (e.g. SAP Ariba, custom SSO providers)**
- These integrations are not covered in standard documentation and vary heavily by customer environment
- Information not found in this knowledge base for highly custom integration requests; these should be escalated to a solutions engineer
