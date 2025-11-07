# Email Refiner Agent

A study project exploring AI agent development using Google's Agent Development Kit (ADK). This project demonstrates various concepts including loop agents, evaluation agents, API servers for agents, server-sent events (SSE), agent runners, and deployment to Vertex AI.

## Overview

This project implements a **Travel Advisor Agent** that helps users with location-based questions, providing weather information, currency exchange rates, and local attraction recommendations. The agent serves as a learning platform for understanding:

- **Loop Agents**: Agents that can iterate and refine responses
- **Evaluation Agents**: Testing and validating agent performance
- **API Server**: RESTful API endpoints for agent interactions
- **Server-Sent Events (SSE)**: Real-time streaming responses
- **Agent Runner**: Execution engine for running agents with session management
- **Vertex AI Deployment**: Deploying agents to Google Cloud Platform

## Project Structure

```text
email_refiner_agent/
├── travel_advisor_agent/      # Main agent package
│   ├── __init__.py
│   ├── agent.py               # Agent definition and tools
│   ├── prompt.py              # Agent prompts and instructions
│   └── TravelEval.evalset.json # Evaluation test cases
├── api_mode.ipynb             # API server usage examples
├── code_mode.ipynb            # Direct agent runner examples
├── deploy.py                  # Vertex AI deployment script
├── remote.py                  # Remote agent interaction examples
├── main.py                    # Main entry point
├── prompt.py                  # Root-level prompts
├── pyproject.toml             # Project dependencies
└── session.db                 # SQLite database for session storage
```

## Features

### Travel Advisor Agent

The agent provides three main tools:

1. **get_weather**: Get current weather information for any location
1. **get_exchange_rate**: Convert currencies and get exchange rates
1. **get_local_attractions**: Find popular attractions and points of interest

### Agent Capabilities

- **Session Management**: Persistent conversation sessions using SQLite
- **Streaming Responses**: Real-time streaming via Server-Sent Events
- **Tool Calling**: Dynamic function calling with context awareness
- **State Management**: Maintains conversation state and user context

## Requirements

- Python >= 3.13
- Google Cloud Platform account with Vertex AI enabled
- OpenAI API key (for LiteLLM model access)

## Installation

- Clone the repository:

```bash
git clone <repository-url>
cd email_refiner_agent
```

- Install dependencies using `uv`:

```bash
uv sync
```

- Set up environment variables:

```bash
# Create a .env file with:
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### Code Mode (Direct Agent Runner)

Use the `code_mode.ipynb` notebook to run the agent directly:

```python
from google.adk.runners import Runner
from travel_advisor_agent.agent import travel_advisor_agent
from google.adk.sessions import DatabaseSessionService
from google.adk.artifacts import InMemoryArtifactService

# Initialize services
session_service = DatabaseSessionService(db_url="sqlite:///./session.db")
artifact_service = InMemoryArtifactService()

# Create runner
runner = Runner(
    agent=travel_advisor_agent,
    session_service=session_service,
    app_name="travel_advisor_agent",
    artifact_service=artifact_service,
)

# Run agent with streaming
async for event in runner.run_async(
    user_id="u_123",
    session_id=session.id,
    new_message=message
):
    if event.is_final_response():
        print(event.content.parts[0].text)
```

### API Mode (Server-Sent Events)

Use the `api_mode.ipynb` notebook to interact with the agent via API:

```python
import requests
import sseclient
import json

# Create a session
response = requests.post(
    f"{BASE_URL}/apps/{APP_NAME}/users/{USER_ID}/sessions"
)
session = response.json()

# Stream query with SSE
message = {
    "appName": APP_NAME,
    "userId": USER_ID,
    "sessionId": session["id"],
    "newMessage": {
        "parts": [{"text": "What is the weather in Tokyo?"}],
        "role": "user",
    },
    "streaming": True,
}

response = requests.post(
    f"{BASE_URL}/run_sse",
    json=message,
    stream=True
)

client = sseclient.SSEClient(response)
for event in client.events():
    data = json.loads(event.data)
    # Process streaming events
```

### Remote Deployment (Vertex AI)

Deploy the agent to Vertex AI using `deploy.py`:

```python
import vertexai
from vertexai.preview import reasoning_engines
from travel_advisor_agent.agent import travel_advisor_agent

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=BUCKET,
)

app = reasoning_engines.AdkApp(
    agent=travel_advisor_agent,
    enable_tracing=True,
)

remote_app = vertexai.agent_engines.create(
    display_name="Travel Advisor Agent",
    agent_engine=app,
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines]",
        "litellm",
    ],
    extra_packages=["travel_advisor_agent"],
    env_vars={
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY"),
    },
)
```

### Interacting with Remote Agent

Use `remote.py` to interact with a deployed agent:

```python
from vertexai import agent_engines

remote_app = agent_engines.get(DEPLOYMENT_ID)

for event in remote_app.stream_query(
    user_id="u_123",
    session_id=SESSION_ID,
    message="I'm going to Laos, any tips?",
):
    print(event)
```

## Evaluation

The project includes evaluation test cases in `TravelEval.evalset.json`. These can be used to test agent performance and validate responses.

## Dependencies

- `google-adk[eval]`: Google Agent Development Kit with evaluation tools
- `google-cloud-aiplatform[adk,agent-engines]`: Vertex AI platform integration
- `google-genai`: Google Generative AI SDK
- `litellm`: Unified interface for multiple LLM providers
- `sseclient-py`: Server-Sent Events client
- `cloudpickle`: Serialization for Python objects

## Configuration

### Vertex AI Settings

Update the following in `deploy.py` and `remote.py`:

- `PROJECT_ID`: Your GCP project ID
- `LOCATION`: GCP region (e.g., "asia-northeast1")
- `BUCKET`: GCS bucket for staging

### Agent Model

The agent uses OpenAI's GPT-4o model via LiteLLM. You can change the model in `travel_advisor_agent/agent.py`:

```python
MODEL = LiteLlm(model="openai/gpt-4o")
```

## Development

### Running Tests

Evaluation test cases can be run using the Google ADK evaluation framework:

```bash
# Run evaluations
python -m google.adk.eval <eval_set_file>
```

### Adding New Tools

To add new tools to the agent:

1. Define an async function in `travel_advisor_agent/agent.py`:

```python
async def my_new_tool(tool_context: ToolContext, param: str):
    """Tool description."""
    return {"result": "data"}
```

1. Add it to the agent's tools list:

```python
travel_advisor_agent = Agent(
    ...
    tools=[
        get_weather,
        get_exchange_rate,
        get_local_attractions,
        my_new_tool,  # Add here
    ],
)
```

## License

License information not specified. Please check with the project maintainers for licensing details.

## Contributing

This is a study project. Contributions and suggestions are welcome!

## References

- [Google ADK Documentation](https://cloud.google.com/vertex-ai/docs/adk)
- [Vertex AI Agent Engines](https://cloud.google.com/vertex-ai/docs/agent-engines)
- [LiteLLM Documentation](https://docs.litellm.ai/)
