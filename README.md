# Example Agent 🎬

A sample specialized agent implementation demonstrating how to integrate with [oqtopus](https://www.oqtopus.dev) - the AI agent orchestration platform.

## 📋 Overview

This project serves as a **reference implementation** for developers who want to create their own specialized agents that work with the oqtopus orchestrator. The example agent is a Movie Agent that answers movie-related queries using Google Gemini LLM.

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                           oqtopus.dev                                  │
│                    (Central Orchestrator Platform)                     │
└───────────────────────────────┬────────────────────────────────────────┘
                                │
                    JWT-Signed Request (via rotagent)
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────────┐
│                         Example Agent                                  │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  @auth.require_auth  ←  rotagent package verifies JWT signature  │   │
│  │  /agent endpoint                                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  movie_agent_package/                                            │   │
│  │  ├── repository_layer/  → Data access (movies)                   │   │
│  │  └── service_layer/     → LLM integration (Gemini)               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Google Gemini API Key ([Get one here](https://aistudio.google.com/))
- [rotagent](https://pypi.org/project/rotagent/) package

### 1. Clone & Install

```bash
git clone https://gitlab.com/yaruchyk.o/agent-example.git
cd example-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requrements.txt
pip install rotagent
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Data source - specifies which CSV file to load from static folder
FILE_NAME=movies.csv

# Optional: Set to 'development' to disable security checks during testing
APP_ENV=development
```

## 📊 Customizing Agent Data

The agent's knowledge base is powered by CSV files stored in the `static` folder. You can easily customize what data your agent uses:

### 1. Add Your Data

Place your CSV file in the `movie_agent_package/static/` folder:

```
movie_agent_package/
└── static/
    ├── movies.csv      # Default movie database
    ├── rental.csv      # Alternative: rental properties data
    └── your_data.csv   # Your custom data file
```

**CSV Format Requirements:**
- Use semicolon (`;`) as delimiter
- First row should contain headers
- UTF-8 encoding recommended

Example CSV structure:
```csv
Title;Year;Genre;Rating
The Matrix;1999;Sci-Fi;8.7
Inception;2010;Thriller;8.8
```

### 2. Switch Data Sources

Change the `FILE_NAME` environment variable in your `.env` file:

```bash
# Use movie data
FILE_NAME=movies.csv

# Or switch to rental property data
FILE_NAME=rental.csv

# Or use your custom data
FILE_NAME=your_data.csv
```

### 3. Restart the Server

The new data will be loaded and displayed on the home page, and the agent will use this data as context when answering queries.

> 💡 **Tip**: This makes it easy to repurpose this example agent for different domains - just swap the CSV file and update the `FILE_NAME` variable!

### 3. Run the Server

```bash
python app.py
```

The agent will start on `http://127.0.0.1:5001`

## 🔐 Authentication Setup

The agent uses JWT-based authentication powered by the [rotagent](https://pypi.org/project/rotagent/) library.

### For Development/Testing

You can add a custom development key for local testing without registering on oqtopus:

#### Step 1: Generate Development Keys

Create a simple Python script or run in the Python REPL:

```python
from rotagent import DevTools

# This will:
# 1. Create an 'authorized_keys' folder
# 2. Save the public key to 'authorized_keys/dev_postman.pem'
# 3. Print the private key to add to your .env file
DevTools.setup_persistent_keys(
    keys_dir="authorized_keys", 
    issuer_id="dev_postman"
)
```

#### Step 2: Update Your `.env`

Copy the printed `DEV_PRIVATE_KEY=...` line to your `.env` file.

#### Step 3: Generate a Test Token

```python
from rotagent import DevTools

# Generate a Bearer token for testing
token, body = DevTools.generate_bearer_token(query="What are the best action movies?")
```

Use this token in Postman, curl, or any HTTP client:

```bash
curl -X POST http://127.0.0.1:5001/agent \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"query":"What are the best action movies?"}'
```

### For Production (Integration with oqtopus)

1. **Register your agent** at [www.oqtopus.dev](https://www.oqtopus.dev)
2. **Download the `.pem` file** provided after registration
3. **Place the `.pem` file** in your `authorized_keys/` directory

The filename will be `{orchestrator_id}.pem`, matching the issuer ID from oqtopus.

## 📁 Project Structure

```
example_agent/
├── app.py                      # Flask application entry point
├── authorized_keys/            # Store public keys here (.pem files)
│   └── {issuer_id}.pem         # Downloaded from oqtopus or generated locally
├── movie_agent_package/
│   ├── repository_layer/       # Data access layer
│   │   └── get_movies.py       # Loads data from static folder
│   ├── service_layer/
│   │   └── gemini_llm.py       # LLM wrapper for Gemini
│   └── static/                 # 📊 YOUR DATA GOES HERE
│       ├── movies.csv          # Movie database (default)
│       └── rental.csv          # Real estate data (example)
├── templates/
│   └── index.html              # Web UI - displays data from static folder
├── requrements.txt             # Python dependencies
└── .env                        # Environment variables (not committed)
                                # ↳ FILE_NAME=movies.csv (controls which data to use)
```

## 🔌 API Endpoints

### `POST /agent`

Protected endpoint that processes queries from the orchestrator.

**Headers:**
- `Authorization: Bearer <JWT_TOKEN>` (Required)
- `Content-Type: application/json`

**Request Body:**
```json
{
  "query": "What are the best sci-fi movies of 2023?",
  "output_structure": "{\"found_answer\": bool, \"details\": {...}}"  // Optional
}
```

**Response:**
```json
{
  "result": {
    "found_answer": true,
    "details": {
      "title": "Dune: Part Two",
      "year": 2024,
      "genre": "Science Fiction"
    }
  }
}
```

### `GET /`

Simple web UI to view movie data (no authentication required).

## 🛠️ Creating Your Own Agent

1. **Copy this repository** as a template
2. **Replace `movie_agent_package/`** with your domain logic
3. **Update the `/agent` endpoint** to process queries relevant to your domain
4. **Register your agent** at [www.oqtopus.dev](https://www.oqtopus.dev)

The key requirement is implementing a `/agent` POST endpoint protected with `@auth.require_auth` from rotagent.

## 📦 Dependencies

- `flask` - Web framework
- `rotagent` - JWT authentication for agent-orchestrator communication
- `google-genai` - Google Gemini LLM
- `python-dotenv` - Environment variable management

## 🔗 Related Projects

| Project | Description |
|---------|-------------|
| [oqtopus](https://www.oqtopus.dev) | The AI agent orchestration platform |
| [rotagent](https://pypi.org/project/rotagent/) | Authentication library for agents |

## 📝 License

MIT License - See [LICENSE](LICENSE) for details.

---

**Built for [oqtopus.dev](https://www.oqtopus.dev)** - The AI Agent Orchestration Platform
