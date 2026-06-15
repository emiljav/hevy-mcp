# hevy-mcp

A read-only MCP server that exposes your [Hevy](https://hevy.com) workout data to Claude Desktop.

## Prerequisites

- Python 3.10+
- A Hevy account with an API key (Settings → Developer in the Hevy app)

## Setup

### 1. Install dependencies

```bash
cd hevy-mcp
pip install -r requirements.txt
```

### 2. Configure your API key

```bash
cp .env.example .env
```

Edit `.env` and replace `your_api_key_here` with your Hevy API key.

### 3. Configure Claude Desktop

Add the following to your `claude_desktop_config.json`:

**Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "hevy": {
      "command": "python",
      "args": ["C:/Users/ejave/hevy-mcp/main.py"],
      "env": {
        "HEVY_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

> **Note:** You can either set `HEVY_API_KEY` in the `env` block above **or** rely on the `.env` file — both work. The `env` block takes precedence.

Restart Claude Desktop after saving the config.

## Available tools

| Tool | Description |
|---|---|
| `get_workouts` | Paginated list of workouts (`page`, `pageSize`) |
| `get_workout` | Single workout by `workout_id` |
| `get_workout_count` | Total number of workouts logged |
| `get_exercise_history` | History for a given `exercise_template_id` (`page`, `pageSize`) |
| `get_routines` | All saved routines (`page`, `pageSize`) |
| `get_exercise_templates` | Exercise library / templates (`page`, `pageSize`) |

## Example prompts

- "How many workouts have I logged in total?"
- "Show me my last 5 workouts."
- "What was my bench press progression over the last 10 sessions?"
- "List all my saved routines."

## Development

Run the server directly to test with the MCP inspector:

```bash
mcp dev main.py
```
