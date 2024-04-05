# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Utility module to:
- Retrieve top search terms from Google Trends dataset
- Query the GDELT API to retrieve news related to top search terms
- Summarize news articles
"""

import requests
from newspaper import Article
from newspaper import ArticleException

from vertexai.generative_models import GenerativeModel
import vertexai.preview.generative_models as generative_models

gdelt_api_url: str = 'https://api.gdeltproject.org/api/v2/doc/doc'
mode: str = 'ArtList'
format: str = 'json'
n_near_words: int = 20
source_country: str = 'US'
source_lang: str = 'english'
tone = 'tone>10'


def _get_articles_info(
        keywords: list[str], 
        start_date: str, 
        end_date: str,
        max_records: int) -> dict:
    """Get articles that match the given keywords.

    Args:
        keywords: 
            A list of keywords to search for.
        startdate: 
            The start date of the search.
        enddate: 
            The end date of the search.
        max_records:
            Number of articles to be retrieved
    Returns:
        A dictionary with news articles that match the given keywords.
    """
    query = (f'near{n_near_words}:"{" ".join(keywords)}" '
             f'sourcecountry:{source_country} '
             f'sourcelang:{source_lang} '
             f'{tone}')
    params = {'query': query,
              'format': format,
              'mode': mode,
              'maxrecords': str(max_records),
              'startdatetime': start_date,
              'enddatetime': end_date}

    response = requests.get(gdelt_api_url, params=params)
    response.raise_for_status()
    return response.json()


def _parse_article(url: str) -> Article|None:
    """Parses an article from the given URL.

    Args:
        url: 
            The URL of the article to parse.

    Returns:
        The parsed article as a string.
    """
    article = Article(url)

    try:
        article.download()
        article.parse()
    except ArticleException:
        return None
    else:
        return article


def _get_documents(articles: dict) -> list[dict]:
    """Gets a list of documents from a list of articles.

    Args:
        articles: 
            A list of articles.

    Returns:
        A list of documents.
    """
    documents = []
    unique_docs = set()

    for article in articles['articles']:
        parsed_article = _parse_article(article['url'])
        if (parsed_article and parsed_article.text and 
            (article['title'] not in unique_docs)):
            unique_docs.add(article['title'])
            document = {
                'page_content': parsed_article.text,
                'title': article['title'],
                'url': article['url'],
                'domain': article['domain'],
                'date': article['seendate']
            }
            documents.append(document)
    return documents


def get_relevant_documents(
        keywords: list,
        start_date: str,
        end_date: str,
        max_records: int) -> list[dict]:
    """Gets a list of relevant documents from a query.
    Args:
        query: A query.

    Returns:
        A list of relevant documents.
    """
    articles = _get_articles_info(
        keywords, start_date, end_date, max_records)
    documents = _get_documents(articles)

    return documents


def summarize_news_article(
        page_content: dict,
        llm: GenerativeModel):
    """Summarizes a news article.

    Args:
        document: 
            A dictionary containing the following keys:
                `page_content`: The text of the news article.
        llm: A language model that can be used to generate summaries.

    Returns:
        A dictionary containing the following keys:
            `page_content`: The original text of the news article.
            `summary`: A one-sentence summary of the news article.
    """
    prompt_template = (
        "Write a one sentence summary of the news article below:"
        f"input: {page_content}"
        "output:")

    try:
        summary = llm.generate_content(
            contents=prompt_template,
            generation_config={
                "max_output_tokens": 2048,
                "temperature": 0.8,
                "top_p": 0.8,
            },
            safety_settings = {
                generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            },
            stream=False,
        )
    except Exception as e:
        print(e)
        return ""

    if isinstance(summary.text, str):
        return summary.text
    else:
        return ""


def summarize_documents(documents: dict, llm) -> list:
    """Summarizes a list of news articles.

    Args:
        documents: 
            A dictionary containing a list of news articles, 
            each of which is a dictionary containing the following keys:
                `page_content`: The text of the news article.
        llm: A language model that can be used to generate summaries.

    Returns:
        A list of dictionaries, each of which contains the following keys:
            `page_content`: The original text of the news article.
            `summary`: A one-sentence summary of the news article.
    """
    summaries = []

    for document in documents:
        summaries.append(
            summarize_news_article(document, llm)
        )

    return summaries
