from openai import OpenAI
from dataclasses import dataclass

from dotenv import load_dotenv
from openai.types.beta import Assistant
from openai.types.responses import WebSearchToolParam

load_dotenv()


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
        "development and other key facts about startups relevant to investors. "
        "Also keep in mind that companies may share similar names."
        "Always try to stick to the first company that you've received resources for. "
        "You are very fair and try to also use the full scale for your ratings.",
        tools=[WebSearchToolParam(type="web_search_preview", search_context_size="high")])

    return res.output_text
