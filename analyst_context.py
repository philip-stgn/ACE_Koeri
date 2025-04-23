from dataclasses import dataclass

from openai import OpenAI
from openai.types.beta import Assistant, Thread


@dataclass
class AnalystContext:
    assistant: Assistant
    client: OpenAI
    thread: Thread