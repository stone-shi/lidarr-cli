# Lidarr CLI

A Python-based Command Line Interface (CLI) for managing your Lidarr server.

## Features
- **Status:** View Lidarr version and OS information.
- **Artists:** List all artists in your library or search for new ones.
- **Albums:** List albums, optionally filtered by artist.
- **Queue:** View the current download queue and progress.
- **History:** View recent activity history.
- **Commands:** Trigger Lidarr commands (e.g., `RefreshArtist`).

## Prerequisites
- Python 3.10+
- Lidarr server URL and API Key

## Configuration
The application uses a `.env` file for configuration:
```env
LIDARR_URL=https://lidarr.local.shifamily.com
LIDARR_API_KEY=edc0f112a92240f99c130bcdc110aee3
```

## Installation
1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   # Option A: Modern way (using pyproject.toml)
   pip install .

   # Option B: Traditional way
   pip install -r requirements.txt
   ```

## Usage
Activate the virtual environment and run `python3 main.py [OPTIONS] COMMAND [ARGS]...`:

### Global Options
- `--json`: Output result in raw JSON format (useful for scripts and `jq`).

### Commands
- `python3 main.py status`: Show Lidarr status.
- `python3 main.py artists`: List all artists (default page 1, limit 20).
- `python3 main.py artists --page 2 --limit 10`: Show page 2 with 10 artists.
- `python3 main.py artists --search "Adele"`: Search for an artist.
- `python3 main.py albums --artist-id 1`: List albums for artist ID 1.
- `python3 main.py albums --page 1 --limit 50`: List first 50 albums in the library.
- `python3 main.py queue`: Show download queue (default page 1, limit 20).
- `python3 main.py queue --page 2 --limit 10`: Show page 2 with 10 items per page.
- `python3 main.py history --limit 5`: Show last 5 history items.
- `python3 main.py command RefreshArtist`: Trigger a command.

### Examples
- **Get JSON output for the queue:**
  ```bash
  python3 main.py --json queue --limit 5
  ```
- **Count items in the queue using jq:**
  ```bash
  python3 main.py --json queue | jq '. | length'
  ```
