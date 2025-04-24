from dotenv import load_dotenv
load_dotenv()
import json
import streamlit as st
import time

from openai import OpenAI

from analyst_context import AnalystContext
from analyze_pitch_pdf import create_assistant, create_thread, load_pdf_into_model, delete_assistant, analyst_user_ask_question, \
analyst_user_message
from news_api import search_by_company_name
from researcher import research


def evaluate_startup(pitch_deck_path: str, company_name: str):
    cx = AnalystContext(None, None, client=OpenAI())

    create_assistant(cx)
    create_thread(cx)

    print("Setup done")

    load_pdf_into_model(cx, pitch_deck_path)

    print("Analyzed pitch deck")

    news_summary = search_by_company_name(company_name, cx.client)

    print("Analyzed news")

    analyst_user_message(cx, f"A colleague already did some research on current news and made following summary: {news_summary}")

    questions = analyst_user_ask_question(cx, "Another colleague offered to help you by doing some web research. What are your five most important research questions regarding this startup? Note that your colleague doesn't know which startup you're analyzing. So ask as precise as possible. Please answer in the JSON Format using a List like this: [\"Research Topic 1\", \"Research Topic 2\",\"Research Topic 3\", ,\"Research Topic 4\", ,\"Research Topic 5\"]")

    print("Generate Questions")

    questions = json.loads(questions)

    for question in questions:
        assert question is not None

        research_result = research(cx.client, question)

        print("Asked one question")

        analyst_user_message(cx, f"Regarding your research question: \"{question}\" My colleague found following results: {research_result}")

    print("Asked all questions")

    detailed_result = analyst_user_ask_question(cx, "With all this information, what is you detailed final rating for future investments in this company? Give a score out of 10 on each chosen category and show your reasoning. Please also try to support you reasoning by hard facts and numbers with sources. For the Format try to use markdown and consistent formatting.")

    print("Generated detailed report")

    total_score = analyst_user_ask_question(cx, "Ok, now please output the final score without any additional details as a number between 0 and 10")

    print(detailed_result)
    print(total_score)

    delete_assistant(cx)


if __name__ == '__main__':
    #evaluate_startup("mint.pdf", "Mint")

    #streamlit run main.py
    st.title("Melgmir Unicorn Finder🦄")

    st.header("Upload your pitchdeck ...")
    company_name = st.text_input("Name of Company")
    file = st.file_uploader("Upload a file", type=["txt", "csv", "jpg", "png"])

    if st.button("Analyse pitchdeck ..."):
        with st.spinner("Please wait..."):
            time.sleep(2)  # Simulate loading
            st.success("Finished!")
            time.sleep(1)
            st.switch_page("pages/evaluation_screen.py")

