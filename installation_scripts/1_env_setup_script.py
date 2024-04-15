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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.`
# See the License for the specific language governing permissions and
# limitations under the License.


import os
from google.cloud import bigquery
from google.cloud import datacatalog_v1
from aux_data import data_gen
from aux_data import bq_tag_generation


print(
    """This installation script will:
     - Create a dataset on BigQuery with data about Audiences.
     - Create a TagTemplate with metadata about the dataset.
       
    This process can take up to 3 minutes to finish.""")

# Set environmental variables
PROJECT_ID = os.environ['PROJECT_ID']
LOCATION = os.environ['LOCATION']
DATASET_ID = 'cdp_dataset'

# Tag template definitions
TAG_TEMPLATE_ID = 'llmcdptemplate'
TAG_TEMPLATE_PATH = f"projects/{PROJECT_ID}/locations/{LOCATION}/tagTemplates/{TAG_TEMPLATE_ID}"

# Create clients for BigQuery and DataCatalog
bq_client = bigquery.Client(project=PROJECT_ID)
datacatalog_client = datacatalog_v1.DataCatalogClient()

dataset_id = "{}.{}".format(bq_client.project, DATASET_ID)
dataset = bigquery.Dataset(dataset_id)
dataset.location = "US"

# Create the dataset
try:
    dataset = bq_client.create_dataset(dataset, timeout=30)
    print(f'Dataset {DATASET_ID} create successfully.')
except Exception as e:
    print(e)


data_gen.generate_and_populate_dataset(
    PROJECT_ID=PROJECT_ID,
    DATASET_ID=DATASET_ID
)

bq_tag_generation.create_template_and_tag_bq(
    PROJECT_ID,
    DATASET_ID,
    TAG_TEMPLATE_ID,
    LOCATION
)

print("Dataset and TagTemplate created successfully.")