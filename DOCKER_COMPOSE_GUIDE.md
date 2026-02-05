# Docker Compose Setup Guide

This document describes how to use Docker Compose to run the Fagskolen Viken project components.

**Note:** This guide uses `docker compose` (Docker Compose V2). If you have an older version, use `docker-compose` (with hyphen) instead.

## Architecture Overview

The project uses a **shared MySQL database** approach:
- A standalone MySQL container runs independently (`MySQL/docker-compose.yaml`)
- The scraping pipeline connects to this external MySQL database
- The MCP server and agent also connect to the same external MySQL database
- All services communicate through a shared Docker network (`fagskolen_network`)

## Available Docker Compose Configurations

### 0. MySQL Database (`MySQL/docker-compose.yaml`)

This is the **required first step**. The MySQL database must be running before starting any other services.

**Service:**
- `db`: MySQL 8.0 database (container name: `fagskolen_mysql`)

**Usage:**
```bash
# Start MySQL database
cd MySQL
docker compose up -d

# Check database status
docker compose ps

# View database logs
docker compose logs -f

# Stop database (data persists in volume)
docker compose down

# Stop and remove database with data
docker compose down -v
```

**Network:**
- Creates `fagskolen_network` that other services will join

### 1. Scraping Pipeline (`docker-compose-scraping.yml`)

This configuration runs the web scraping pipeline that:
- Connects to the external MySQL database
- Runs the scraper to collect study program data from fagskolen-viken.no
- Stores the data in the MySQL database

**Services:**
- `scraper`: Python scraper application

**Prerequisites:**
- MySQL database must be running (see step 0 above)

**Usage:**
```bash
# Start the scraping pipeline
docker compose -f docker-compose-scraping.yml up

# Run in detached mode
docker compose -f docker-compose-scraping.yml up -d

# View logs
docker compose -f docker-compose-scraping.yml logs -f

# Stop and remove containers
docker compose -f docker-compose-scraping.yml down
```

**Output:**
- JSON files are stored in `./Scraping/json_for_processing/`
- Study URLs are saved in `./Scraping/studies_urls.json`
- Data is stored in the external MySQL database

### 2. MCP Server and ADK Agent (`docker-compose-mcp.yml`)

This configuration runs the MCP server and ADK agent that:
- Connects to the external MySQL database
- Runs the MCP server to expose database tools
- Runs the ADK agent for interactive Q&A

**Services:**
- `mcp_server`: FastMCP server on port 8001
- `adk_agent`: Google ADK agent for conversation

**Prerequisites:**
1. MySQL database must be running (see step 0 above)
2. Database should be populated with data (run scraping pipeline first)
3. Copy `.env.example` to `.env` and add your Google API key:
   ```bash
   cp .env.example .env
   # Edit .env and set GOOGLE_API_KEY=your_actual_key
   ```

**Usage:**
```bash
# Start MCP server and agent
docker compose -f docker-compose-mcp.yml up

# Run in detached mode
docker compose -f docker-compose-mcp.yml up -d

# Interact with the agent (requires tty)
docker compose -f docker-compose-mcp.yml run adk_agent

# View logs
docker compose -f docker-compose-mcp.yml logs -f mcp_server
docker compose -f docker-compose-mcp.yml logs -f adk_agent

# Stop and remove containers
docker compose -f docker-compose-mcp.yml down
```

**Accessing services:**
- MCP Server: http://localhost:8001/mcp
- MySQL: localhost:3306

## Complete Workflow

To run the entire system from scratch:

### Step 0: Start MySQL Database

```bash
# Navigate to MySQL directory and start the database
cd MySQL
docker compose up -d

# Verify it's running
docker compose ps

# Return to project root
cd ..
```

### Step 1: Run the Scraping Pipeline

```bash
# Start and run the scraper
docker compose -f docker-compose-scraping.yml up

# Wait for the scraper to complete, then stop
docker compose -f docker-compose-scraping.yml down
```

### Step 2: Start MCP Server and Agent

```bash
# Configure environment variables
cp .env.example .env
# Edit .env and set your GOOGLE_API_KEY

# Start MCP server and agent
docker compose -f docker-compose-mcp.yml up
```

## Database Configuration

All services connect to the same external MySQL database with these credentials:

- **Container Name:** `fagskolen_mysql`
- **Host:** `fagskolen_mysql` (within Docker network) or `localhost` (from host)
- **Port:** 3306
- **Root Password:** admin
- **User:** admin
- **Password:** admin
- **Database:** fagskolen

You can override these by setting environment variables in `.env` or modifying the docker-compose files.

## Volume Persistence

- **Database data:** Stored in named volume `mysql_db_data` in the MySQL container (persists between container restarts)
- **JSON files:** Mapped to `./Scraping/json_for_processing/` on host
- **Study URLs:** Mapped to `./Scraping/studies_urls.json` on host

## Network Configuration

All services share a common Docker network:
- **Network name:** `fagskolen_network`
- The MySQL container creates this network
- The scraping and MCP compose files reference it as an external network
- This allows all services to communicate with each other and the database

## Troubleshooting

### Database Connection Issues

If services cannot connect to the database:

1. Check that the MySQL database is running:
   ```bash
   cd MySQL
   docker compose ps
   ```

2. Check database logs:
   ```bash
   cd MySQL
   docker compose logs db
   ```

3. Verify database is accepting connections:
   ```bash
   docker exec fagskolen_mysql mysqladmin ping -uroot -padmin
   ```

4. Ensure the database is healthy:
   ```bash
   docker inspect fagskolen_mysql --format='{{.State.Health.Status}}'
   ```

5. Verify the network exists:
   ```bash
   docker network ls | grep fagskolen_network
   ```

### MCP Server Connection Issues

If the agent cannot connect to the MCP server:

1. Check MCP server is running:
   ```bash
   docker compose -f docker-compose-mcp.yml ps mcp_server
   ```

2. Check MCP server logs:
   ```bash
   docker compose -f docker-compose-mcp.yml logs mcp_server
   ```

3. Test MCP server endpoint:
   ```bash
   curl http://localhost:8001/mcp
   ```

### Rebuilding Images

If you make changes to code or Dockerfiles:

```bash
# Rebuild images
docker compose -f docker-compose-scraping.yml build
docker compose -f docker-compose-mcp.yml build

# Or rebuild and restart
docker compose -f docker-compose-mcp.yml up --build
```

### Cleaning Up

To completely remove all containers, networks, and volumes:

```bash
# Stop and remove scraping services
docker compose -f docker-compose-scraping.yml down

# Stop and remove MCP server and agent
docker compose -f docker-compose-mcp.yml down

# Stop and remove MySQL database (WARNING: This deletes all data!)
cd MySQL
docker compose down -v
```

## Development Tips

### Running Individual Services

You can run specific services:

```bash
# Only start the database
cd MySQL
docker compose up -d

# Only start MCP server (database must be running)
docker compose -f docker-compose-mcp.yml up mcp_server
```

### Accessing Containers

To get a shell in a running container:

```bash
# Access database
docker exec -it fagskolen_mysql mysql -uroot -padmin fagskolen

# Access MCP server container
docker compose -f docker-compose-mcp.yml exec mcp_server /bin/bash
```

### Viewing Real-time Logs

```bash
# All services
docker compose -f docker-compose-mcp.yml logs -f

# Specific service
docker compose -f docker-compose-mcp.yml logs -f mcp_server
```
