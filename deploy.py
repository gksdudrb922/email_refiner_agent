import dotenv

dotenv.load_dotenv()

import os
import vertexai
import vertexai.agent_engines
from vertexai.preview import reasoning_engines
from travel_advisor_agent.agent import travel_advisor_agent

PROJECT_ID = "smooth-tendril-477418-v1"
LOCATION = "asia-northeast1"
BUCKET = "gs://nuri-awesome-weather-agent"

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
