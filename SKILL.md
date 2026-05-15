# Lidarr CLI Skill

A powerful command-line interface for managing a Lidarr server, designed for both human use and AI agent integration.

## Description
This tool allows you to interact with a Lidarr server to monitor system status, search/list artists and albums, view the download queue with detailed error messages, and check activity history. It supports both beautiful terminal tables and raw JSON output for automation.

## Setup
### 1. Prerequisites
- Python 3.10+
- A running Lidarr instance with API access.

### 2. Configuration
Create a `.env` file in the project root:
```env
LIDARR_URL=your_lidarr_url (e.g., https://lidarr.example.com)
LIDARR_API_KEY=your_api_key
```

### 3. Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

## Usage Guidelines for AI Agents

### Command Structure
The CLI follows a standard pattern:
`python3 main.py [GLOBAL_OPTIONS] COMMAND [ARGS]...`

### Global Options
- `--json`: **Crucial for AI agents.** Always use this flag when you need to parse the output. It returns structured JSON that includes detailed metadata, status flags, and error messages.

### Key Commands

| Command | Description | Example |
| :--- | :--- | :--- |
| `status` | Get Lidarr version and OS info. | `python3 main.py --json status` |
| `artists` | List all artists or search for one. | `python3 main.py --json artists --search "Adele"` |
| `albums` | List albums, optionally by artist. | `python3 main.py --json albums --artist-id 1` |
| `queue` | Show download queue + error details. | `python3 main.py --json queue --limit 10` |
| `history` | View recent activity logs. | `python3 main.py --json history --limit 5` |
| `command` | Execute a Lidarr system command. | `python3 main.py command RefreshArtist` |

### Pagination
For `artists`, `albums`, `queue`, and `history`, use:
- `--page`: Page number (default: 1)
- `--limit`: Items per page (default varies by command)

## Interpreting Queue Warnings
When using `--json queue`, pay close attention to:
- `trackedDownloadStatus`: If this is `"warning"`, the item is stuck.
- `trackedDownloadState`: Look for `"importFailed"` or `"importPending"`.
- `statusMessages`: This array contains the exact reason Lidarr is not importing the file (e.g., "Album match is not close enough").

## Best Practices
1. **Always use `--json`**: When processing data, never rely on the table output.
2. **Check for errors**: Wrap calls in try/except or check the exit code.
3. **Pagination**: If you don't find what you're looking for, increment the `--page` number.
4. **Identify Artists**: Use `artists --search` first to get the `id`, then use that `id` with `albums --artist-id`.
