# Alternative README — Fagskolen Data & MCP

> Concise guide built from the code in `Scraping`, `FastMCP_server`, and `fagskolen_agent` (in that order). ✅

---

## 1) Scraping (data extraction pipeline) 🔧

Purpose
- Crawl Fagskolen Viken public site and extract study program and course information into structured JSON files for later ingestion to MySQL.

Key scripts
- `main.py` — Orchestrates the pipeline: create database, collect study URLs, extract data for each study, then push JSONs to the database.
- `get_studies.py` — `get_urls()` / `scrape_urls()` to collect study page links (supports buffered output to `studies_urls.json`).
- `DataExtractor.py` — `StudyDataExtractor` class that parses study HTML, extracts study metadata and course details, and can write JSON files into `json_for_processing/`.
- `create_database.py` — Runs the provided SQL script (`TurbotroebbelSQL.sql`) to initialise database schema.
- `Push2SQL.py` — Loads JSON files from `json_for_processing/` and upserts the data into tables: `courses`, `study_place`, `study_programs`, and `lookuptalbe_study_course`.

Typical usage
```bash
# 1) Create DB schema
python Scraping/create_database.py

# 2) Fetch/refresh URLs (writes to studies_urls.json)
python Scraping/get_studies.py

# 3) Run the full pipeline (create DB, scrape all pages, export JSON, push to DB)
python Scraping/main.py

# 4) Or push JSONs manually (dry-run to parse without writing)
python Scraping/Push2SQL.py --dry-run
```

Notes
- The extractor uses `BeautifulSoup`, `pandas`, and `urllib` to parse pages and follow course links to collect learning outcomes and metadata.
- `DataExtractor` writes JSON into `json_for_processing/` (one file per study), which `Push2SQL.py` consumes.
- `Push2SQL.py` expects a MySQL connection (can use `--config path/to/config.cnf`), otherwise it will try localhost defaults.

---

## 2) FastMCP_server (MCP server exposing DB tools) ⚙️

Purpose
- Provide an MCP service exposing small DB access tools (study programs and courses) that agents can call via HTTP.

Key files
- `mcp_server.py` — Registers tools on a FastMCP instance and starts the server (default HTTP port: 8001). Tools include functions from `TableStudyPrograms` and `TableCourses`.
- `database_connection.py` — `DBConnection` class that wraps a MySQL connection and provides `query()` and `check_connection()` helpers.
- `study_program_tools.py` — `TableStudyPrograms` class with methods like `get_number_of_study_programs()`, `get_study_programs_names()`, `get_datafields()`, and `get_datafields_values(program, fields)`.
- `courses_tools.py` — `TableCourses` class with `get_number_of_courses()`, `get_course_names()`, `get_course_info(title)`.

Typical usage
```bash
# Ensure your MySQL is running and schema is present (see Scraping/create_database.py)
# Run the MCP server (starts and listens on port 8001):
python FastMCP_server/mcp_server.py
```

What the tools allow
- Listing categories, programs and course names
- Querying specific fields for a study program
- Returning full course info by course title

Security & config
- Database connection parameters are in `database_connection.DBConnection` defaults: host `127.0.0.1`, user `root`, password `admin`. Override these as needed or adapt the code to read config files.

---

## 3) fagskolen_agent (agent configuration & orchestration) 🤖

Purpose
- Defines an agent stack that uses the MCP tools to answer questions about study programs and courses at Fagskolen i Viken.

Key elements
- `agent.py` sets up agent/tool wiring using Google ADK classes (`Agent`, `SequentialAgent`, `AgentTool`, and `McpToolset`).
- `MCP_SERVER` is configured to `http://127.0.0.1:8001/mcp` — the MCP server started by `FastMCP_server`.
- Pipeline agents:
  - `input_agent` — structures user input
  - `retriver_agent` — retrieves data via the MCP tools (must use the toolset only)
  - `Verify_agent` — verifies the retrieved information
  - `Presenting_agent` — formats the final output for the end user
  - `root_agent` and `sequential_agent` orchestrate flow; `question_tool` is exposed to `root_agent`.

Setup notes
- A Google API key value is referenced via `.env` (configure your key securely). Do not commit secrets.
- The agent configuration expects the MCP server to be reachable at the configured `MCP_SERVER` URL.

---

## Dependencies & install suggestions 💡
- Python 3.9+ recommended
- Core Python packages used by the codebase:
  - pandas, beautifulsoup4, lxml, mysql-connector-python
  - fastmcp (server), google-adk (agent SDK)
- Example install command (adjust packages as needed):
```bash
pip install pandas beautifulsoup4 lxml mysql-connector-python
# Also install packages required for your agent / MCP stack
pip install fastmcp google-adk
```

---

## Quick start checklist ✅
1. Configure MySQL and create the DB schema: `python Scraping/create_database.py`
2. (Optional) Refresh study links: `python Scraping/get_studies.py`
3. Run full scraping pipeline: `python Scraping/main.py`
4. Start MCP server: `python FastMCP_server/mcp_server.py`
5. Configure `fagskolen_agent/.env` (add your GOOGLE_API_KEY securely) and run your agent as required.

---

## Notes & safety ⚠️
- This README is a technical, alternate summary derived from the code in `Scraping`, `FastMCP_server`, and `fagskolen_agent` only.
- **Do not store API keys/secrets in source control**. The repo contains a `.env` sample; replace with your secret values locally.

---

If you want, I can also add a small `requirements.txt` and a minimal startup script for a one-line demonstration (scrape → push → start MCP). 🔧
