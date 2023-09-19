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
from datetime import datetime
from typing import Any 
from newspaper import Article
from newspaper import ArticleException


class GoogleTrends:
    """Get Trends from BQ dataset"""

    def __init__(
            self, 
            project_id: str, 
            bq_client: Any):
        self.project_id = project_id
        self.bq_client = bq_client


    def run(self, refresh_date: str):
        """Gets the top search terms on a given date from the BigQuery 
        `google_trends.top_terms` dataset.

        Args:
            refresh_date (str, optional): 
            The date of the search terms to retrieve.

        Returns:
            List[str]: A list of the top search terms on the specified date.
        """
        query = ( 
            "SELECT term, rank "
            "FROM `bigquery-public-data.google_trends.top_terms` "
            f"WHERE refresh_date = '{refresh_date}' "
            "GROUP BY 1,2 "
            "ORDER by rank ASC"
        )
        query_job = self.bq_client.query(
            query,
            location="US",
        )
        df = query_job.to_dataframe()
        
        terms = df.loc[0].values[0]
        terms = terms.split(' ')

        return terms


class GDELTRetriever:
    """Query the GDELT API to retrieve news related to top search terms"""

    def __init__(self, max_records:int = 10, tone: str = 'positive'):
        self.gdelt_api_url: str = 'https://api.gdeltproject.org/api/v2/doc/doc'
        self.mode: str = 'ArtList'
        self.format: str = 'json'
        self.max_records: int = max_records
        self.n_near_words: int = 20
        self.source_country: str = 'US'
        self.source_lang: str = 'english'
        
        if tone == 'positive':
            self.tone = 'tone>10'
        elif tone == 'negative':
            self.tone = 'tone<-5'


    def _get_articles_info(
            self, 
            keywords: list[str], 
            startdate: datetime, 
            enddate: datetime) -> dict:
        """Get articles that match the given keywords.

        Args:
            keywords: 
                A list of keywords to search for.
            startdate: 
                The start date of the search.
            enddate: 
                The end date of the search.

        Returns:
            A dictionary with news articles that match the given keywords.
        """
        query = (f'near{self.n_near_words}:"{" ".join(keywords)}" '
                 f'sourcecountry:{self.source_country} '
                 f'sourcelang:{self.source_lang} '
                 f'{self.tone}')
        params = {'query': query,
                  'format': self.format,
                  'mode': self.mode,
                  'maxrecords': str(self.max_records),
                  'startdatetime': startdate,
                  'enddatetime': enddate}

        response = requests.get(self.gdelt_api_url, params=params)
        response.raise_for_status()
        return response.json()


    def _parse_article(self, url: str) -> Article|None:
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


    def _get_documents(self, articles: dict) -> list[dict]:
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
            parsed_article = self._parse_article(article['url'])
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


    def get_relevant_documents(self, query: dict) -> list[dict]:
        """Gets a list of relevant documents from a query.
        Args:
            query: A query.

        Returns:
            A list of relevant documents.
        """
        keywords = query['keywords']
        startdate = query['startdate']
        enddate = query['enddate']
        articles = self._get_articles_info(keywords, startdate, enddate)
        documents = self._get_documents(articles)

        return documents


def summarize_news_article(document: dict, llm):
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
        f"input: {document['page_content']}"
        "output:")
    document['summary'] = llm.predict(prompt_template).text
    return document


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
