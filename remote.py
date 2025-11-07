import vertexai
from vertexai import agent_engines

PROJECT_ID = "smooth-tendril-477418-v1"
LOCATION = "asia-northeast1"

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
)

# deployments = agent_engines.list()

# for deployment in deployments:
#     print(deployment)

DEPLOYMENT_ID = "projects/1033622830055/locations/asia-northeast1/reasoningEngines/6508739400526987264"

SESSION_ID = "1595202805658812416"

remote_app = agent_engines.get(DEPLOYMENT_ID)

# remote_app.delete(force=True)


# remote_session = remote_app.create_session(user_id="u_123")

# print(remote_session["id"])

for event in remote_app.stream_query(
    user_id="u_123",
    session_id=SESSION_ID,
    message="I'm going to Laos, any tips?",
):
    print(event, "\n", "=" * 50)
