import os

from newsapi import NewsApiClient

from dotenv import load_dotenv
load_dotenv()

#Init
newsapi_client = NewsApiClient(api_key=os.environ["NEWS_API_KEY"])

def search_by_company_name(company_name, client):
    company_everything = newsapi_client.get_everything(q=company_name, sort_by='relevancy')
    top_articles = company_everything["articles"][:3]

    result = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a startup-analyst."},
            {"role": "user",
             "content": f"How do you evaluate the company:{company_name} with the following news-articles: \n\n{top_articles}"}
        ]
    )
    return result

