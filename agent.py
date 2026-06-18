import os
from functools import cached_property

from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.genai import Client


class GlobalGemini(Gemini):
    @cached_property
    def api_client(self) -> Client:
        return Client(
            vertexai=True,
            location=os.environ.get("GOOGLE_CLOUD_LOCATION", "global"),
            project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
            api_key=os.environ.get("GOOGLE_API_KEY"),
        )


root_agent = LlmAgent(
    name="root_agent",
    model=GlobalGemini(model="gemini-2.0-flash"),
    description="This is the root agent for my first agent",
)