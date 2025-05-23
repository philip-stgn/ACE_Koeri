import os

from newsapi import NewsApiClient

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

newsapi_client = NewsApiClient(api_key=os.environ["NEWS_API_KEY"])
prompt = "Summarize the key points across all articles in bullet points. Word limit is 400. Focus on recent events, leadership, market performance, partnerships, innovation, and public perception. Identify strengths and weaknesses of the company based on this news coverage. Evaluate the overall tone of the news (positive, neutral, or negative). Give the company a score from 1 to 10 based on: Market potential, Innovation, Risk factors, Public perception. Justify your rating with a short explanation."


def search_by_company_name(company_name: str, client: OpenAI) -> str:
    company_everything = newsapi_client.get_everything(
        q=company_name,
        sources='the-verge, cnn, fortune, the-washington-post, business-insider, le-monde, die-zeit',
        sort_by='relevancy')
    top_articles = company_everything["articles"][:30]

    return client.responses.create(
        model="gpt-4.1",
        instructions="You are a startup-analyst.",
        input=f"We have some articles about the company {company_name}." +
        prompt +
        f"Here are the articles: {top_articles}").output_text
