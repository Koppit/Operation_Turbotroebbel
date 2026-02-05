# Docker Compose Setup Guide

This document describes how to use Docker Compose to run the Fagskolen Viken project components.

**Note:** This guide uses `docker compose` (Docker Compose V2). If you have an older version, use `docker-compose` (with hyphen) instead.

## Available Docker Compose Configurations

### 1. Scraping Pipeline (`docker-compose-scraping.yml`)

This configuration runs the web scraping pipeline that:
- Starts a MySQL database
- Runs the scraper to collect study program data from fagskolen-viken.no
- Stores the data in the MySQL database

**Services:**
- `db`: MySQL 8.0 database
- `scraper`: Python scraper application

**Usage:**
```bash
# Start the scraping pipeline
docker-compose -f docker-compose-scraping.yml up

# Run in detached mode
docker-compose -f docker-compose-scraping.yml up -d

# View logs
docker-compose -f docker-compose-scraping.yml logs -f

# Stop and remove containers
docker-compose -f docker-compose-scraping.yml down

# Stop and remove containers with volumes (deletes database)
docker-compose -f docker-compose-scraping.yml down -v
```

**Output:**
- JSON files are stored in `./Scraping/json_for_processing/`
- Study URLs are saved in `./Scraping/studies_urls.json`

### 2. MCP Server and ADK Agent (`docker-compose-mcp.yml`)

This configuration runs the MCP server and ADK agent that:
- Starts a MySQL database (must be populated first by scraping pipeline)
- Runs the MCP server to expose database tools
- Runs the ADK agent for interactive Q&A

**Services:**
- `db`: MySQL 8.0 database
- `mcp_server`: FastMCP server on port 8001
- `adk_agent`: Google ADK agent for conversation

**Prerequisites:**
1. Copy `.env.example` to `.env` and add your Google API key:
   ```bash
   cp .env.example .env
   # Edit .env and set GOOGLE_API_KEY=your_actual_key
   ```

2. Ensure the database is populated with data (run scraping pipeline first)

**Usage:**
```bash
# Start MCP server and agent
docker-compose -f docker-compose-mcp.yml up

# Run in detached mode
docker-compose -f docker-compose-mcp.yml up -d

# Interact with the agent (requires tty)
docker-compose -f docker-compose-mcp.yml run adk_agent

# View logs
docker-compose -f docker-compose-mcp.yml logs -f mcp_server
docker-compose -f docker-compose-mcp.yml logs -f adk_agent

# Stop and remove containers
docker-compose -f docker-compose-mcp.yml down
```

**Accessing services:**
- MCP Server: http://localhost:8001/mcp
- MySQL: localhost:3306

## Complete Workflow

To run the entire system from scratch:

### Step 1: Run the Scraping Pipeline

```bash
# Start and run the scraper
docker-compose -f docker-compose-scraping.yml up

# Wait for the scraper to complete, then stop
docker-compose -f docker-compose-scraping.yml down
```

### Step 2: Start MCP Server and Agent

```bash
# Configure environment variables
cp .env.example .env
# Edit .env and set your GOOGLE_API_KEY

# Start MCP server and agent
docker-compose -f docker-compose-mcp.yml up
```

## Database Configuration

Both configurations use the same MySQL database with these default credentials:

- **Host:** `db` (within Docker network) or `localhost` (from host)
- **Port:** 3306
- **Root Password:** admin
- **User:** admin
- **Password:** admin
- **Database:** fagskolen

You can override these by setting environment variables in `.env` or modifying the docker-compose files.

## Volume Persistence

- **Database data:** Stored in named volume `db_data` (persists between container restarts)
- **JSON files:** Mapped to `./Scraping/json_for_processing/` on host
- **Study URLs:** Mapped to `./Scraping/studies_urls.json` on host

## Network Configuration

Each docker-compose file creates its own network:
- `scraping_network` for the scraping pipeline
- `mcp_network` for the MCP server and agent

## Troubleshooting

### Database Connection Issues

If services cannot connect to the database:

1. Check that the database is healthy:
   ```bash
   docker-compose -f docker-compose-mcp.yml ps
   ```

2. Check database logs:
   ```bash
   docker-compose -f docker-compose-mcp.yml logs db
   ```

3. Verify database is accepting connections:
   ```bash
   docker-compose -f docker-compose-mcp.yml exec db mysqladmin ping -uroot -padmin
   ```

### MCP Server Connection Issues

If the agent cannot connect to the MCP server:

1. Check MCP server is running:
   ```bash
   docker-compose -f docker-compose-mcp.yml ps mcp_server
   ```

2. Check MCP server logs:
   ```bash
   docker-compose -f docker-compose-mcp.yml logs mcp_server
   ```

3. Test MCP server endpoint:
   ```bash
   curl http://localhost:8001/mcp
   ```

### Rebuilding Images

If you make changes to code or Dockerfiles:

```bash
# Rebuild images
docker-compose -f docker-compose-scraping.yml build
docker-compose -f docker-compose-mcp.yml build

# Or rebuild and restart
docker-compose -f docker-compose-mcp.yml up --build
```

### Cleaning Up

To completely remove all containers, networks, and volumes:

```bash
# For scraping pipeline
docker-compose -f docker-compose-scraping.yml down -v

# For MCP server and agent
docker-compose -f docker-compose-mcp.yml down -v
```

## Development Tips

### Running Individual Services

You can run specific services:

```bash
# Only start the database
docker-compose -f docker-compose-mcp.yml up db

# Only start MCP server (database must be running)
docker-compose -f docker-compose-mcp.yml up mcp_server
```

### Accessing Containers

To get a shell in a running container:

```bash
# Access database
docker-compose -f docker-compose-mcp.yml exec db mysql -uroot -padmin fagskolen

# Access MCP server container
docker-compose -f docker-compose-mcp.yml exec mcp_server /bin/bash
```

### Viewing Real-time Logs

```bash
# All services
docker-compose -f docker-compose-mcp.yml logs -f

# Specific service
docker-compose -f docker-compose-mcp.yml logs -f mcp_server
```
