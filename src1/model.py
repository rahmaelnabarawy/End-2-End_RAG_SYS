import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent/".env"
load_dotenv(env_path)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"
token = os.environ["GITHUB_TOKEN"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

# response = client.complete(
#     messages=[
#         SystemMessage("You are a helpful assistant."),
#         UserMessage("What is the capital of France?"),
#     ],
#     temperature=1.0,
#     top_p=1.0,
#     model=model
# )

# print(response.choices[0].message.content)