#!/usr/bin/env python3

import os
import json
import argparse
from google.cloud import discoveryengine_v1alpha

#
# Usage:
# python genai_marketing_search_app_creation.py --project="my-project-id" --app-name=my_app --company-name=my_company --uris="cloud.goole.com/*"
#

parser = argparse.ArgumentParser()
parser.add_argument("--project", help="Id of project to use", type=str)
parser.add_argument("--location", help="Location to deploy",
                    type=str, default="global")
parser.add_argument("--app-name", help="Application name", type=str)
parser.add_argument("--company-name", help="Name of your company", type=str)
parser.add_argument(
    "--uris", help="Datastore uris to index comma separated", type=str)

dict_args = parser.parse_args()

print(f"Using arguments: {dict_args}")

project_id = dict_args.project
default_location = dict_args.location
app_name = dict_args.app_name
company_name = dict_args.company_name
uris = dict_args.uris



def create_search_app():

    # Creating datastore client
    datastore_client = discoveryengine_v1alpha.DataStoreServiceClient()

    # Initialize datastore request argument(s) for Search
    parent_collection = f"projects/{project_id}/locations/{default_location}/collections/default_collection"
    datastore_name = f"{app_name}_datastore"
    datastore_id = f"{datastore_name}"

    # check if datastore exists
    try:
        datastore = datastore_client.get_data_store(request=discoveryengine_v1alpha.GetDataStoreRequest(
            name=f"{parent_collection}/dataStores/{datastore_id}",
        ))
        print(f"Datastore already exist: {datastore}")
    except:
        # Create datastore
        datastore = discoveryengine_v1alpha.DataStore(
            display_name=datastore_name,
            industry_vertical="GENERIC",
            solution_types=["SOLUTION_TYPE_SEARCH"],
            content_config="PUBLIC_WEBSITE",
        )

        datastore_request = discoveryengine_v1alpha.CreateDataStoreRequest(
            parent=parent_collection,
            data_store=datastore,
            data_store_id=datastore_id
        )
        print(f"Creating datastore: {datastore_request}")

        datastore_client.create_data_store(request=datastore_request)
        
        create_target_site(project_id, default_location, datastore_id, uris)

    # Creating search engine client
    engine_client = discoveryengine_v1alpha.EngineServiceClient()
    # Initialize search engine request arguments
    search_engine_name = f"{app_name}_search_engine"
    engine_id = f"{search_engine_name}"

    # check if search engine exists
    try:
        engine = engine_client.get_engine(request=discoveryengine_v1alpha.GetEngineRequest(
            name=f"{parent_collection}/engines/{engine_id}"
        ))
        print(f"Engine already exist: {engine}")
    except:
        # Engine config and LLM features
        engine_config = discoveryengine_v1alpha.types.Engine.SearchEngineConfig(
            search_tier="SEARCH_TIER_ENTERPRISE",
            search_add_ons=["SEARCH_ADD_ON_LLM"]
        )
        # Engine
        engine = discoveryengine_v1alpha.Engine(
            search_engine_config=engine_config,
            display_name=search_engine_name,
            solution_type="SOLUTION_TYPE_SEARCH",
            data_store_ids=[datastore_id],
            common_config={'company_name': company_name}
        )
        engine_request = discoveryengine_v1alpha.CreateEngineRequest(
            parent=parent_collection,
            engine=engine,
            engine_id=engine_id
        )
        print(f"Creating engine: {engine_request}")
        engine_client.create_engine(request=engine_request)

    # os.putenv("SEARCH_DATASTORE",f"{parent_collection}/dataStores/{datastore_id}")
    # os.putenv("SEARCH_DATASTORE_ID", datastore_id)
    # os.putenv("SEARCH_ENGINE",f"{parent_collection}/engines/{engine_id}")

    with open("marketingEnvValue.json", "r") as jsonFile:
        data = json.load(jsonFile)
        data["SEARCH_DATASTORE_ID"] = datastore_id
    with open("marketingEnvValue.json", "w") as jsonFile:
        json.dump(data, jsonFile)
    
    print(f"""Search engine app results:
          Datastore: {parent_collection}/dataStores/{datastore_id}
          App: {parent_collection}/engines/{engine_id}
          """)

def create_target_site(project_id, default_location, datastore_id, uris):
    parent_collection = f"projects/{project_id}/locations/{default_location}/collections/default_collection"
    site_search_engine_service_client = discoveryengine_v1alpha.SiteSearchEngineServiceClient()
    uris=uris.split(",")
    for uri in uris:
        target_site = discoveryengine_v1alpha.TargetSite()
        target_site.provided_uri_pattern = uri
        print(f"Creating Target site: {target_site}")
        try:
            site_search_engine_service_client.create_target_site(request=discoveryengine_v1alpha.CreateTargetSiteRequest(
                parent=f"{parent_collection}/dataStores/{datastore_id}/siteSearchEngine",
                target_site=target_site,
            ))
        except:
            print(f"Target site already exist: {uri}")


if __name__ == "__main__":
    create_search_app()