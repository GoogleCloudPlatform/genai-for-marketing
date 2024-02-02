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