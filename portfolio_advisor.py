from openai.types.beta import Assistant, Thread
from openai import OpenAI
from dataclasses import dataclass
import os
import json
from time import sleep

from dotenv import load_dotenv
from openai.types.beta.threads import TextContentBlockParam, Run

load_dotenv()


@dataclass
class PortfolioContext:
    assistant: Assistant | None
    thread: Thread | None
    client: OpenAI


def create_assistant(cx: PortfolioContext):
    assert cx.assistant is None
    cx.assistant = cx.client.beta.assistants.create(
        model="gpt-4.1",
        instructions="You are a portfolio advisor and your job is it to create portfolios based on results gathered from your colleagues and requirements from the user."
                     "Please also propose weighed allocations an keep the portfolio recommendations at fewer than 5 companies unless explicitly asked otherwise.",
        temperature=0.2,
    )


def delete_assistant(cx: PortfolioContext):
    cx.client.beta.assistants.delete(assistant_id=cx.assistant.id)


def load_results(cx: PortfolioContext, directory: str):
    files = [entry.name for entry in os.scandir(directory) if entry.is_file()]

    cx.thread = cx.client.beta.threads.create()

    for file in files:
        with open(os.path.join(directory, file), "rt") as f:
            old_result = f.read()

            cx.client.beta.threads.messages.create(
                role="user",
                thread_id=cx.thread.id,
                content=[TextContentBlockParam(
                    type="text",
                    text=old_result
                )])


def portfolio_user_ask_question(cx: PortfolioContext, prompt: str) -> str:
    assert cx.thread is not None
    assert cx.assistant is not None

    cx.client.beta.threads.messages.create(
        thread_id=cx.thread.id, role="user", content=prompt)

    run = portfolio_retrieve_answer(cx)

    return cx.client.beta.threads.messages.list(
        thread_id=cx.thread.id,
        run_id=run.id,
        order="desc",
        limit=1).data[0].content[0].text.value


def portfolio_retrieve_answer(cx: PortfolioContext) -> Run:
    run = cx.client.beta.threads.runs.create(
        thread_id=cx.thread.id, assistant_id=cx.assistant.id)

    while run.status != "completed":
        run = cx.client.beta.threads.runs.retrieve(
            run_id=run.id, thread_id=cx.thread.id)
        sleep(1)

    assert run.status == "completed"

    return run


def close_thread(cx: PortfolioContext):
    cx.client.beta.threads.delete(cx.thread.id)

