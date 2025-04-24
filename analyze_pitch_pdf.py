from analyst_context import AnalystContext
from time import sleep

import os
from dotenv import load_dotenv
from openai.types.beta.threads import TextContentBlockParam, ImageURLContentBlockParam, ImageURLParam, \
    ImageFileContentBlockParam, ImageFileParam, Run
from wand.image import Image

load_dotenv()


# --- Extract text from the PDF ---

def create_assistant(cx: AnalystContext):
    assert cx.assistant is None
    cx.assistant = cx.client.beta.assistants.create(
        model="gpt-4.1",
        instructions="You are an analyst expert with focus on startups. Your task is to consult investors with "
                     "realistic outlooks on future performance of startups. Your final goal will be to rate a startup "
                     "by at least the following categories: Finance, Innovation, Growth potential. Please also take"
                     "notes on additional fitting categories. Also keep in mind that the audience is a competent"
                     "investor who likes to see hard facts and numbers. When using such hard facts and numbers also"
                     "always disclose the source",
        temperature=0.2,
    )


def delete_assistant(cx: AnalystContext):
    cx.client.beta.assistants.delete(assistant_id=cx.assistant.id)


def create_thread(cx: AnalystContext):
    assert cx.thread is None
    cx.thread = cx.client.beta.threads.create()


def load_pdf_into_model(cx: AnalystContext, pdf_path: str):
    content = [
        TextContentBlockParam(
            text="I received a slide deck for a new startup."
            "Can you please take a look at it and create a comprehensive summary?"
            " Pay special attention to hard facts like numbers.",
            type="text")]

    with Image(filename=pdf_path) as pdf:
        for i, page in enumerate(pdf.sequence):
            with Image(page) as page_img:
                # Prevent Content from becoming to long Current limit according
                # to docs is 10
                if len(content) >= 5:
                    cx.client.beta.threads.messages.create(
                        thread_id=cx.thread.id, role="user", content=content)
                    content = []

                print(f"Read page {i}")

                img = page_img.make_blob("png")

                # for some reason it only works if we write the file to disk
                # first
                with open("/tmp/output.png", "wb") as f:
                    f.write(img)

                with open("/tmp/output.png", "rb") as f:
                    img_file_openai = cx.client.files.create(
                        file=f, purpose="assistants")

                cx.client.files.wait_for_processing(img_file_openai.id)

                content.append(
                    ImageFileContentBlockParam(
                        type="image_file",
                        image_file=ImageFileParam(
                            file_id=img_file_openai.id,
                            detail="low")))

    cx.client.beta.threads.messages.create(
        thread_id=cx.thread.id, role="user", content=content)

    retrieve_answer(cx)


def analyst_user_message(cx: AnalystContext, message: str):
    cx.client.beta.threads.messages.create(
        thread_id=cx.thread.id, role="user", content=[
            TextContentBlockParam(
                text=message, type="text")])


def analyst_user_ask_question(cx: AnalystContext, prompt: str) -> str:
    assert cx.thread is not None
    assert cx.assistant is not None

    cx.client.beta.threads.messages.create(
        thread_id=cx.thread.id, role="user", content=prompt)

    run = retrieve_answer(cx)

    return cx.client.beta.threads.messages.list(
        thread_id=cx.thread.id,
        run_id=run.id,
        order="desc",
        limit=1).data[0].content[0].text.value


def retrieve_answer(cx: AnalystContext) -> Run:
    run = cx.client.beta.threads.runs.create(
        thread_id=cx.thread.id, assistant_id=cx.assistant.id)

    while run.status != "completed":
        run = cx.client.beta.threads.runs.retrieve(
            run_id=run.id, thread_id=cx.thread.id)
        sleep(1)

    assert run.status == "completed"

    return run


def company_name(pdf_path):
    return os.path.splitext(os.path.basename(pdf_path))[0]
