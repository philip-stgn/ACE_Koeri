from dotenv import load_dotenv
load_dotenv()
import json
import os
from dataclasses import asdict
import streamlit as st
import time

from openai import OpenAI

from analyst_context import AnalystContext
from analyze_pitch_pdf import create_assistant, create_thread, load_pdf_into_model, delete_assistant, analyst_user_ask_question, \
analyst_user_message
from news_api import search_by_company_name
from researcher import research
from startup_evaluation import StartupQuestion, StartupEvaluation


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

    questions = analyst_user_ask_question(cx, "Another colleague offered to help you by doing some web research. What are your five most important research questions regarding this startup? Note that your colleague doesn't know which startup you're analyzing. So ask as precise as possible. It is very important that you answer in the JSON Format using a List like this: [\"Research Topic 1\", \"Research Topic 2\",\"Research Topic 3\", ,\"Research Topic 4\", ,\"Research Topic 5\"]")

    print("Generate Questions")

    questions = json.loads(questions)
    question_results: [StartupQuestion] = []

    for question in questions:
        assert question is not None

        research_result = research(cx.client, question)

        question_results.append(StartupQuestion(question=question, answer=research_result))

        print("Asked one question")

        analyst_user_message(cx, f"Regarding your research question: \"{question}\" My colleague found following results: {research_result}")

    print("Asked all questions")

    detailed_result = analyst_user_ask_question(cx, "With all this information, what is you detailed final rating for future investments in this company? Give a score out of 10 on each chosen category and show your reasoning. Please also try to support you reasoning by hard facts and numbers with sources.")

    print("Generated detailed report")

    category_scores_json = analyst_user_ask_question(cx, "Can you please extract all category scores into a json list with the following format: [{\"category\":\"categoryName\", \"score\": float}] . Please only output the JSON object itself!")

    print("Extracted category scores")

    total_score = analyst_user_ask_question(cx, "Ok, now please output the final score without any additional details as a singular float number between 0 and 10")

    evaluation = StartupEvaluation(
        company_name=company_name,
        company_summary=analyst_user_ask_question(cx, "Please give me a short one sentence description on the company"),
        category_scores=json.loads(category_scores_json),
        questions=question_results,
        evaluation_text=detailed_result,
        final_score=float(total_score),
    )

    os.makedirs("results", exist_ok=True)
    with open(f"results/{company_name}.json", "w") as outfile:
        outfile.write(json.dumps(asdict(evaluation), indent=4))

    delete_assistant(cx)


if __name__ == '__main__':
    #evaluate_startup("examples/airbnb.pdf", "AirBnB")


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

