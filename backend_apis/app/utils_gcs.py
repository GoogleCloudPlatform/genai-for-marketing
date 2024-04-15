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

from google.cloud import storage
import io

def upload_to_gcs(project_id, bucket_name, file, destination_blob_name):
    """Uploads a file to Google Cloud Storage

    Args:
        file_path (str): Path to the local file to upload.
        destination_blob_name (str): Name of the object in the GCS bucket.
    """
    print("Started Uploadig to GCS")
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_file(file)

    print(f"File uploaded to gs://{bucket_name}/{destination_blob_name}")

    return f"{bucket_name}/{destination_blob_name}"


def download_from_gcs(project_id,bucket_name,source_blob_name):
    """Downloads a file from Google Cloud Storage

    Args:
        source_blob_name (str): Name of the object in the GCS bucket.
        destination_file_path (str): Path to save the file locally.
    """

    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    buffer = io.BytesIO()

    blob.download_to_file(buffer)

    print(f"File gs://{bucket_name}/{source_blob_name} downloaded ")
    return buffer