from startup_evaluation import StartupQuestion, StartupEvaluation
from researcher import research
from news_api import search_by_company_name
from analyze_pitch_pdf import create_assistant, create_thread, load_pdf_into_model, delete_assistant, analyst_user_ask_question, \
    analyst_user_message
from analyst_context import AnalystContext
from openai import OpenAI
import tempfile
import streamlit as st
from dataclasses import asdict
import os
import json
from dotenv import load_dotenv
load_dotenv()


def evaluate_startup(
        pitch_deck_path: str,
        company_name: str) -> StartupEvaluation:
    cx = AnalystContext(None, None, client=OpenAI())

    create_assistant(cx)
    create_thread(cx)

    print("Setup done")

    load_pdf_into_model(cx, pitch_deck_path)

    print("Analyzed pitch deck")

    news_summary = search_by_company_name(company_name, cx.client)

    print("Analyzed news")

    analyst_user_message(
        cx,
        f"A colleague already did some research on current news and made following summary: {news_summary}")

    questions = analyst_user_ask_question(
        cx,
        "Another colleague offered to help you by doing some web research. What are your five most important research questions regarding this startup? Note that your colleague doesn't know which startup you're analyzing. So ask as precise as possible. It is very important that you answer in the JSON Format using a List like this: [\"Research Topic 1\", \"Research Topic 2\",\"Research Topic 3\", ,\"Research Topic 4\", ,\"Research Topic 5\"]")

    print("Generate Questions")

    questions = json.loads(questions)
    question_results: [StartupQuestion] = []

    for question in questions:
        assert question is not None

        research_result = research(cx.client, question)

        question_results.append(
            StartupQuestion(
                question=question,
                answer=research_result))

        print("Asked one question")

        analyst_user_message(
            cx,
            f"Regarding your research question: \"{question}\" My colleague found following results: {research_result}")

    print("Asked all questions")

    detailed_result = analyst_user_ask_question(
        cx,
        "With all this information, what is you detailed final rating for future investments in this company? Give a score out of 10 on each chosen category and show your reasoning. Please also try to support you reasoning by hard facts and numbers with sources. Please just reply with the summary itself.")

    print("Generated detailed report")

    category_scores_json = analyst_user_ask_question(
        cx,
        "Can you please extract all category scores into a json list with the following format: [{\"category\":\"categoryName\", \"score\": float}] . Please only output the JSON object itself!")

    print("Extracted category scores")

    total_score = analyst_user_ask_question(
        cx,
        "Ok, now please output the final score without any additional details as a singular float number between 0 and 10")

    evaluation = StartupEvaluation(
        company_name=company_name,
        company_summary=analyst_user_ask_question(
            cx,
            "Please give me a short one sentence description on the company"),
        category_scores=json.loads(category_scores_json),
        questions=question_results,
        evaluation_text=detailed_result,
        final_score=float(total_score),
    )

    os.makedirs("results", exist_ok=True)
    with open(f"results/{company_name}.json", "w") as outfile:
        outfile.write(json.dumps(asdict(evaluation), indent=4))

    delete_assistant(cx)

    return evaluation


if __name__ == '__main__':
    last_evaluation: StartupEvaluation = StartupEvaluation(
        "", "", [], [], "", 3.0)
    st.title("Unicorn-Finder🦄")

    st.header("Upload your pitch deck ...")
    company_name = st.text_input("Name of Company")
    file = st.file_uploader(
        "Upload a file",
        accept_multiple_files=False,
        type=["pdf"])

    if st.button("Analyse pitch deck"):
        enter_company: str = "Please enter the company name!"
        if company_name == "":
            st.markdown(
                "<p style='color:red;'>Please enter the company name!</p>",
                unsafe_allow_html=True)
        elif file is None:
            st.markdown(
                "<p style='color:red;'>Please upload a file!</p>",
                unsafe_allow_html=True)
        else:
            with st.spinner("Gathering and analyzing data. Please wait..."):
                tmp = tempfile.NamedTemporaryFile()
                data = file.read()
                tmp.write(data)
                last_evaluation = evaluate_startup(tmp.name, company_name)

                # Large text area
                st.markdown(
                    "<h1 style='text-align: center;'>Final Score</h1>",
                    unsafe_allow_html=True)
                st.markdown(
                    f"""
                    <div style="
                        background-color:#74BBE3;
                        border-radius:20px;
                        padding:20px;
                        height:200px;
                        display:flex;
                        justify-content:center;
                        align-items:center;
                        font-size:60px;
                        text-align:center;
                    ">
                        <span style="font-weight:bold;">{last_evaluation.final_score}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                vert_space = '<div style="padding: 25px 5px;"></div>'
                st.markdown(vert_space, unsafe_allow_html=True)
                st.markdown(vert_space, unsafe_allow_html=True)

                st.markdown(
                    f"""
                        <p>{last_evaluation.evaluation_text}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
