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
Utility module for Vertex AI Search API
"""


from typing import List, Tuple
from google.cloud import discoveryengine


def complete_query(
    search_query: str,
    project_id: str,
    location: str,
    search_engine_id: str,
    complete_client: discoveryengine.CompletionServiceClient
) -> List[str]:
    """Completes a search query with suggestions.

    Args:
        search_query (str): 
            The search query to complete.
        project_id (str): 
            The ID of the project that owns the search engine.
        location (str): 
            The location of the search engine.
        search_engine_id (str): 
            The ID of the search engine.
        complete_client (discoveryengine.CompletionServiceClient): 
            The completion client.

    Returns:
        A list of suggested queries.
    """
    suggestions_list = []
    
    if len(search_query) > 2:
        # The full resource name of the search engine data store
        # e.g. projects/*/locations/global/collections/default_collection/dataStores/default_data_store
        data_store_path = complete_client.data_store_path(
            project=project_id,
            location=location,
            data_store=search_engine_id
        )
        # Initialize request argument(s)
        request = discoveryengine.CompleteQueryRequest(
            data_store=data_store_path,
            query=search_query,
        )

        # Make the request
        response = complete_client.complete_query(request=request)

        for query_suggestion in response.query_suggestions:
            suggestions_list.append(query_suggestion.suggestion)

    # Handle the response
    return suggestions_list


def search(
    search_query: str,
    project_id: str,
    location: str,
    search_engine_id: str,
    serving_config_id: str,
    search_client: discoveryengine.SearchServiceClient
):
    """Searches for documents that match the given query.

    Args:
        search_query: 
            The search query.
        project_id: 
            The ID of the project that owns the search engine.
        location: 
            The location of the search engine.
        search_engine_id: 
            The ID of the search engine.
        serving_config_id: 
            The ID of the serving config.
        search_client: 
            A `discoveryengine.SearchServiceClient` instance.

    Returns:
        A list of `discoveryengine.SearchResponse.SearchResult` objects.
    """
    # The full resource name of the search engine serving config
    # e.g. projects/{project_id}/locations/{location}
    serving_config = search_client.serving_config_path(
        project=project_id,
        location=location,
        data_store=search_engine_id,
        serving_config=serving_config_id,
    )

    snippet_spec = (
        discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
            return_snippet=True
        )
    )
    summary_spec = (
        discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec(
            summary_result_count=3,
            include_citations=True,
        )
    )
    content_spec = discoveryengine.SearchRequest.ContentSearchSpec(
        snippet_spec=snippet_spec, summary_spec=summary_spec
    )    

    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=search_query,
        content_search_spec=content_spec,
        page_size=20,
    )
    response = search_client.search(request)

    return response
