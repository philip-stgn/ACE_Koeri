import json
from dataclasses import dataclass

from dotenv import load_dotenv
from openai.types.beta import Assistant
from openai.types.responses import WebSearchToolParam

load_dotenv()
from openai import OpenAI

@dataclass
class ResearcherContext:
    client: OpenAI
    assistant: Assistant | None


def research(client: OpenAI, question: str) -> str:
    res = client.responses.create(
        input=question,
        model="gpt-4.1",
        instructions="You are a researcher focused on web research on startup companies. "
                      "Your colleagues will ask you questions and you should professionally "
                      "answer them. Note that your research should focus on market "
                      "development and other key facts about startups relevant to investors. ",
        tools=[WebSearchToolParam(type="web_search_preview", search_context_size="high")])

    return res.output_text

