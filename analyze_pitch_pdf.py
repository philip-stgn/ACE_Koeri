import base64
from time import sleep

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.beta.threads import TextContentBlockParam, ImageURLContentBlockParam, ImageURLParam, \
    ImageFileContentBlockParam, ImageFileParam
from wand.image import Image

load_dotenv()  # Lade Umgebungsvariablen aus .env-Datei

from analyst_context import AnalystContext

from openai.types.beta import Assistant

import openai

# --- Your PDF file path as a string ---
PDF_PATH = "airbnb.pdf"  # <-- paste your path here

# --- Extract text from the PDF ---
def create_assistant(cx: AnalystContext):
    assert cx.assistant is None
    cx.assistant = cx.client.beta.assistants.create(
        model="gpt-4o",
        instructions="You are an analyst expert with focus on startups. Your task is to consult investors with "
                     "realistic outlooks on future performance of startups.",
    )

def delete_assistant(cx: AnalystContext):
    cx.client.beta.assistants.delete(assistant_id=cx.assistant.id)

def create_thread(cx: AnalystContext):
    assert cx.thread is None
    cx.thread = cx.client.beta.threads.create()

def load_pdf_into_model(cx: AnalystContext, pdf_path: str) -> str:
    content = [TextContentBlockParam(text="I received a slide deck for a new startup."
                "Can you please take a look at it and summarize the most important key points?", type="text")]

    with Image(filename=pdf_path) as pdf:
        for i, page in enumerate(pdf.sequence):
            with Image(page) as page_img:
                # Prevent Content from becoming to long Current limit according to docs is 10
                if len(content) >= 1:
                    cx.client.beta.threads.messages.create(thread_id=cx.thread.id, role="user", content=content)
                    content = []

                img = page_img.make_blob("png")

                # for some reason it only works if we write the file to disk first
                with open("/tmp/output.png", "wb") as f:
                    f.write(img)

                with open("/tmp/output.png", "rb") as f:
                    img_file_openai = cx.client.files.create(file=f, purpose="assistants")

                cx.client.files.wait_for_processing(img_file_openai.id)

                content.append(ImageFileContentBlockParam(type="image_file", image_file=ImageFileParam(file_id=img_file_openai.id)))

                #content.append(
                #   ImageURLContentBlockParam(type="image_url", image_url=ImageURLParam(url= f"data:image/jpeg;base64,{base64.b64encode(img)}")) )

                #cx.client.beta.threads.messages.create(thread_id=cx.thread.id, role="user", content=json.dumps([{"type": "input_image", "image_url": f"data:image/png;base64,{base64.b64encode(img)}"}]))

    cx.client.beta.threads.messages.create(thread_id=cx.thread.id, role="user", content=content)

    run = cx.client.beta.threads.runs.create(thread_id=cx.thread.id, assistant_id=cx.assistant.id)

    while run.status != "completed":
        run = cx.client.beta.threads.runs.retrieve(run_id=run.id, thread_id=cx.thread.id)
        sleep(1)

    assert run.status == "completed"


# --- Run it ---
if __name__ == "__main__":
    context = AnalystContext(None, None, None)
    context.client = OpenAI()
    create_assistant(context)
    create_thread(context)

    load_pdf_into_model(context, PDF_PATH)
    print("\n📄 Summary:\n")
    print(context.client.beta.threads.messages.list(thread_id=context.thread.id, order="desc", limit=1).data[0].content)
    delete_assistant(context)
