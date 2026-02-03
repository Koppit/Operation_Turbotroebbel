# Project Dependencies

This document lists all dependencies for the Operation Turbotroebbel project.

## Overview

This project consists of several components:
1. **Web Scraping** - Scrapes study information from Fagskolen Viken website
2. **Database** - MySQL database for storing structured study data
3. **MCP Server** - FastMCP server providing API access to the database
4. **Multi-Agent System** - Google ADK-based agent system for intelligent query handling

## Python Dependencies

All Python dependencies are listed in `requirements.txt` and can be installed using:

```bash
pip install -r requirements.txt
```

### External Packages

| Package | Version | Purpose | Used In |
|---------|---------|---------|---------|
| `beautifulsoup4` | >=4.12.0 | HTML parsing for web scraping | `Scraping/get_studies.py`, `Scraping/DataExtractor.py` |
| `pandas` | >=2.0.0 | Data manipulation and analysis | `Scraping/DataExtractor.py` |
| `mysql-connector-python` | >=8.0.0 | MySQL database connectivity | `Scraping/create_database.py`, `Scraping/Push2SQL.py`, `FastMCP_server/*.py`, `PushToMySQL_old.py` |
| `fastmcp` | >=0.1.0 | MCP server framework | `FastMCP_server/mcp_server.py` |
| `google-adk` | >=0.1.0 | Google Agent Development Kit for multi-agent systems | `fagskolen_agent/agent.py` |

### Standard Library Modules

The following Python standard library modules are used (no installation required):

- `os` - Operating system interface
- `json` - JSON data handling
- `argparse` - Command-line argument parsing
- `glob` - File pattern matching
- `typing` - Type hints support
- `time` - Time-related functions
- `sys` - System-specific parameters
- `asyncio` - Asynchronous I/O
- `configparser` - Configuration file parsing
- `pathlib` - Object-oriented filesystem paths
- `urllib.request` - URL handling
- `enum` - Enumeration support
- `warnings` - Warning control

## Infrastructure Dependencies

### Docker

The project uses Docker for running MySQL database:

| Service | Image | Purpose |
|---------|-------|---------|
| MySQL Database | `mysql:8.0` | Data storage and management |

Configuration file: `MySQL/docker-compose.yaml`

To start the MySQL database:

```bash
cd MySQL
docker-compose up -d
```

### Database

- **MySQL 8.0** - Relational database for storing study programs, courses, and related data
- Database schema: `Scraping/TurbotroebbelSQL.sql`

## Development Dependencies

The project uses the following tools for development:

- **Python 3.x** - Primary programming language
- **Git** - Version control
- **Docker & Docker Compose** - Container orchestration

## Optional Dependencies

### For LiteLLM Support (Ollama)

The agent system can work with Ollama through LiteLLM:

- `LiteLlm` from `google.adk.models.lite_llm`

This is already included in the `google-adk` package but requires a separate Ollama installation if you want to use local LLM models.

## Installation Guide

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start MySQL Database

```bash
cd MySQL
docker-compose up -d
```

### 3. Configure Database Connection

The database connection uses the following default credentials (defined in `MySQL/docker-compose.yaml`):

- **Host:** localhost
- **Port:** 3306
- **User:** admin
- **Password:** admin
- **Root Password:** admin

### 4. Initialize Database

```bash
cd Scraping
python create_database.py
```

### 5. Run Web Scraping

```bash
cd Scraping
python main.py
```

### 6. Start MCP Server

```bash
cd FastMCP_server
python mcp_server.py
```

### 7. Run Agent System

```bash
cd fagskolen_agent
python agent.py
```

## Notes

- All dependencies use minimum version requirements (>=) to ensure compatibility
- The project is designed to work with Python 3.8 or higher
- Database credentials are configured in the Docker Compose file
- Some modules may require additional system libraries (e.g., MySQL client libraries)

## Troubleshooting

### MySQL Connection Issues

If you encounter MySQL connection errors:

1. Ensure Docker is running and the MySQL container is up
2. Check that port 3306 is not being used by another service
3. Verify database credentials match those in `docker-compose.yaml`

### Import Errors

If you get import errors for any package:

1. Ensure you've installed all requirements: `pip install -r requirements.txt`
2. Verify you're using Python 3.8 or higher
3. Check that you're in a virtual environment (recommended)

### Google ADK Installation

The `google-adk` package may require specific installation steps. Refer to the official Google ADK documentation for installation instructions.

## Version History

- **Initial Version** - Created comprehensive dependency documentation for the project
