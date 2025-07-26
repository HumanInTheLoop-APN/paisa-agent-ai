# MCP Context Forge Gateway - Docker Compose Setup

This directory contains Docker Compose configuration for running the [MCP Context Forge Gateway](https://github.com/IBM/mcp-context-forge) in a containerized environment.

## Overview

The MCP Context Forge Gateway serves as a central management point for tools, resources, and prompts that can be accessed by MCP-compatible LLM applications. It provides:

- **Gateway Management**: Central hub for MCP servers
- **Authentication**: JWT-based authentication system
- **Web UI**: Admin interface for managing servers and tools
- **API**: RESTful API for programmatic access
- **Persistence**: Database storage for configuration and data

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- At least 1GB of available memory
- Port 4444 available on your host

### Basic Setup

1. **Create data directory** (for database persistence):

   ```bash
   mkdir -p data
   ```

2. **Configure environment variables**:

   ```bash
   # Copy the example environment file
   cp env.example .env

   # Edit the .env file with your desired settings
   # At minimum, change the JWT_SECRET_KEY and BASIC_AUTH_PASSWORD
   ```

3. **Start the gateway**:

   ```bash
   docker compose up -d
   ```

4. **Verify it's running**:

   ```bash
   curl http://localhost:4444/health
   # Expected: {"status":"ok"}
   ```

5. **Access the web UI**:
   - Open http://localhost:4444 in your browser
   - Login with the credentials from your `.env` file

## Configuration

### Environment Variables

The gateway is configured via environment variables in the `.env` file. Copy `env.example` to `.env` and modify the values as needed.

#### Essential Configuration

| Variable                       | Description                | Default                              |
| ------------------------------ | -------------------------- | ------------------------------------ |
| `HOST`                         | Host to bind to            | `0.0.0.0`                            |
| `PORT`                         | Port to listen on          | `4444`                               |
| `JWT_SECRET_KEY`               | Secret for JWT tokens      | `my-secret-key-change-in-production` |
| `BASIC_AUTH_USER`              | Admin username             | `admin`                              |
| `BASIC_AUTH_PASSWORD`          | Admin password             | `changeme`                           |
| `DATABASE_URL`                 | Database connection string | `sqlite:////data/mcp.db`             |
| `MCPGATEWAY_UI_ENABLED`        | Enable web UI              | `true`                               |
| `MCPGATEWAY_ADMIN_API_ENABLED` | Enable admin API           | `true`                               |

#### Security Variables (Change These!)

```bash
# Generate a strong JWT secret
JWT_SECRET_KEY=your-very-long-random-secret-key-here

# Set a strong admin password
BASIC_AUTH_PASSWORD=your-strong-password-here
```

### Database Options

**SQLite (Default)**: Simple file-based database, good for development

```bash
DATABASE_URL=sqlite:////data/mcp.db
```

**PostgreSQL**: Production-ready database (uncomment in docker-compose.yaml)

```bash
DATABASE_URL=postgresql://postgres:mysecretpassword@postgres:5432/mcp
```

### Security Considerations

⚠️ **Important**: Change these default values for production:

1. **JWT Secret**: Generate a strong random key
2. **Admin Password**: Use a strong password
3. **Database Password**: If using PostgreSQL

## Usage Examples

### Generate JWT Token

```bash
# Generate a token for API access
docker exec mcpgateway python3 -m mcpgateway.utils.create_jwt_token \
  --username admin \
  --exp 10080 \
  --secret "$(grep JWT_SECRET_KEY .env | cut -d'=' -f2)"
```

### API Access

```bash
# Set your token
export MCPGATEWAY_BEARER_TOKEN="your-jwt-token-here"

# List servers
curl -H "Authorization: Bearer $MCPGATEWAY_BEARER_TOKEN" \
  http://localhost:4444/servers

# List tools
curl -H "Authorization: Bearer $MCPGATEWAY_BEARER_TOKEN" \
  http://localhost:4444/tools
```

### Add MCP Server

```bash
# Add a server via API
curl -X POST \
  -H "Authorization: Bearer $MCPGATEWAY_BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-server",
    "description": "My MCP Server",
    "transport": "http",
    "url": "http://localhost:8080"
  }' \
  http://localhost:4444/servers
```

## Advanced Configuration

### Using PostgreSQL

1. Uncomment the PostgreSQL service in `docker-compose.yaml`
2. Update the `DATABASE_URL` in your `.env` file:
   ```bash
   DATABASE_URL=postgresql://postgres:mysecretpassword@postgres:5432/mcp
   ```
3. Set PostgreSQL environment variables in your `.env`:
   ```bash
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=mysecretpassword
   POSTGRES_DB=mcp
   ```
4. Restart the stack:
   ```bash
   docker compose down
   docker compose up -d
   ```

### Using Redis (for queueing)

1. Uncomment the Redis service in `docker-compose.yaml`
2. Set the `REDIS_URL` in your `.env` file:
   ```bash
   REDIS_URL=redis://redis:6379/0
   ```
3. Restart the stack

### SSL/HTTPS Setup

For production HTTPS, you can use a reverse proxy like nginx or traefik:

```yaml
# Add to docker-compose.yaml
nginx:
  image: nginx:alpine
  ports:
    - "443:443"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf:ro
    - ./ssl:/etc/nginx/ssl:ro
  depends_on:
    - mcpgateway
```

## Management Commands

### Start/Stop

```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# Restart services
docker compose restart

# View logs
docker compose logs -f mcpgateway
```

### Maintenance

```bash
# Update to latest image
docker compose pull
docker compose up -d

# Backup database
docker exec mcpgateway cp /data/mcp.db /data/mcp.db.backup

# Clean up volumes (⚠️ destroys data)
docker compose down -v
```

### Health Checks

```bash
# Check service health
docker compose ps

# Test gateway health
curl http://localhost:4444/health

# Check database connectivity
docker exec mcpgateway python3 -c "
import sqlalchemy
from mcpgateway.database import get_database_url
engine = sqlalchemy.create_engine(get_database_url())
print('Database connection: OK')
"
```

## Troubleshooting

### Common Issues

**Port already in use**:

```bash
# Check what's using port 4444
lsof -i :4444
# or
netstat -anp | grep 4444
```

**Permission denied**:

```bash
# Fix data directory permissions
sudo chown -R $USER:$USER data/
chmod 755 data/
```

**Container won't start**:

```bash
# Check logs
docker compose logs mcpgateway

# Check container status
docker compose ps
```

**Database connection issues**:

```bash
# For PostgreSQL, check if it's running
docker compose logs postgres

# For SQLite, check file permissions
ls -la data/
```

**Environment variable issues**:

```bash
# Check if .env file exists
ls -la .env

# Verify environment variables are loaded
docker compose exec mcpgateway env | grep MCP
```

### Logs and Debugging

```bash
# Follow gateway logs
docker compose logs -f mcpgateway

# Check all service logs
docker compose logs

# Access container shell
docker compose exec mcpgateway /bin/sh

# Check environment variables
docker compose exec mcpgateway env | grep MCP
```

## Integration Examples

### With Claude Desktop

Add to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "mcpgateway-wrapper": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "--network=host",
        "-i",
        "-e",
        "MCP_SERVER_CATALOG_URLS=http://localhost:4444/servers/UUID_OF_SERVER_1",
        "-e",
        "MCP_AUTH_TOKEN=<YOUR_JWT_TOKEN>",
        "ghcr.io/ibm/mcp-context-forge:latest",
        "python3",
        "-m",
        "mcpgateway.wrapper"
      ]
    }
  }
}
```

### With MCP CLI

```bash
# Install MCP CLI
pip install mcp

# Configure MCP CLI
export MCPGATEWAY_BEARER_TOKEN="your-jwt-token"

# Test connection
mcp-cli ping --server mcpgateway-wrapper
```

## Production Deployment

For production use, consider:

1. **Security**:

   - Change all default passwords
   - Use strong JWT secrets
   - Enable HTTPS
   - Restrict network access

2. **Monitoring**:

   - Set up log aggregation
   - Monitor resource usage
   - Set up alerts

3. **Backup**:

   - Regular database backups
   - Configuration backups
   - Disaster recovery plan

4. **Scaling**:

   - Use PostgreSQL for better performance
   - Consider Redis for caching
   - Load balancing for high availability

## Environment File Structure

The `env.example` file contains all available configuration options organized into sections:

- **Basic Configuration**: Host, port, and core settings
- **Authentication**: JWT and basic auth settings
- **Features**: UI and API enablement
- **Database Configuration**: Connection strings and pool settings
- **Redis Configuration**: Optional Redis settings
- **Logging**: Log level configuration
- **Security**: CORS, rate limiting, SSL settings
- **Advanced Configuration**: Performance and tuning options
- **Monitoring**: Metrics and health check settings
- **Development Settings**: Debug and development options

## Resources

- [MCP Context Forge Documentation](https://github.com/IBM/mcp-context-forge)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [GitHub Container Registry](https://ghcr.io/ibm/mcp-context-forge)
