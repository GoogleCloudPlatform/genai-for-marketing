import argparse
import json
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import os
import random
import string
import time

parser = argparse.ArgumentParser()
parser.add_argument("--folder-name", help="Name of the drive folder", type=str)
parser.add_argument(
    "--service-account-email", help="email of your service account", type=str
)
parser.add_argument(
    "--force",
    help="Force script execution even if output file exists",
    action="store_true",
)

dict_args = parser.parse_args()


folder_name = dict_args.folder_name
service_account_email = dict_args.service_account_email

output_dir = os.path.join(os.path.dirname(__file__), "..", "output_config")
output_file = "gdrive_folder_results.json"
output_path = os.path.join(output_dir, output_file)
templates_path = os.path.join(os.path.dirname(__file__), "..", "..", "templates")
terraform_state_path = os.path.join(
    os.path.dirname(__file__), "..", "terraform.tfstate"
)

if not service_account_email:
    try:
        # Construct the path to terraform.tfstate in the parent directory

        # Check if the file exists
        if not os.path.exists(terraform_state_path):
            raise FileNotFoundError(f"File not found: {terraform_state_path}")

        with open(terraform_state_path, "r") as f:
            tfstate = json.load(f)
            service_account_email = tfstate["outputs"]["genai_marketing_infra"][
                "value"
            ]["cloud_run_backend_sa"]
    except (FileNotFoundError, KeyError) as e:
        print(f"Error: Could not get service account email from terraform state: {e}")
        exit(1)

print(
    f"Using arguments\n folder_name: {folder_name}\n service_account_email: {service_account_email}"
)


def create_folder(folder_name):
    """Create a folder and prints the folder ID
    Returns : Folder Id
    """
    creds, _ = google.auth.default()

    try:
        # create drive api client
        service = build("drive", "v3", credentials=creds)
        file_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
        }

        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, fields="id").execute()
        print(f'Folder ID: "{file.get("id")}".')
        return file.get("id")

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


# Sharing Folder with DOMAIN


def share_file(real_folder_id, real_user):
    creds, _ = google.auth.default()

    try:
        # create drive api client
        service = build("drive", "v3", credentials=creds)
        ids = []
        folder_id = real_folder_id

        def callback(request_id, response, exception):
            if exception:
                # Handle error
                print(exception)
            else:
                print(f"Request_Id: {request_id}")
                print(f'Permission Id: {response.get("id")}')
                ids.append(response.get("id"))

        # pylint: disable=maybe-no-member
        batch = service.new_batch_http_request(callback=callback)
        user_permission = {
            "type": "user",
            "role": "writer",
            "emailAddress": real_user,
        }
        batch.add(
            service.permissions().create(
                fileId=folder_id,
                body=user_permission,
                fields="id",
            )
        )
        batch.execute()

    except HttpError as error:
        print(f"An error occurred: {error}")
        ids = None

    return ids


# ----- Files upload ----


def upload_with_conversion(folder_id, source_file, destination_file, file_type):
    """Upload file with conversion
    Returns: ID of the file uploaded
    """
    creds, _ = google.auth.default()

    try:
        # create drive api client
        service = build("drive", "v3", credentials=creds)
        results = (
            service.files()
            .list(
                q=f"name='{destination_file}'",
                pageSize=10,
                fields="nextPageToken, files(id, name)",
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
            )
            .execute()
        )

        query = "'{}' in parents".format(folder_id)
        children = (
            service.files()
            .list(q=query, fields="nextPageToken, files(id, name)")
            .execute()
        )
        # print(children['files'])
        fileCheck = next(
            (item for item in children["files"] if item["name"] == destination_file),
            None,
        )
        if len(children["files"]) == 0 or fileCheck == None:

            file_metadata = {
                "name": destination_file,
                "mimeType": "application/vnd.google-apps.spreadsheet",
                "parents": [folder_id],
            }
            media = MediaFileUpload(source_file, mimetype=file_type, resumable=True)
            # pylint: disable=maybe-no-member
            file = (
                service.files()
                .create(body=file_metadata, media_body=media, fields="id")
                .execute()
            )
            print(f'File with ID: "{file.get("id")}" has been uploaded.')
            return file.get("id")
        else:
            fileData = next(
                (
                    item
                    for item in children["files"]
                    if item["name"] == destination_file
                ),
                None,
            )
            print("File already Exists:", fileData["id"])
            return fileData["id"]

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None


if __name__ == "__main__":
    start_time = time.time()
    required_keys = [
        "folder_gdrive_id",
        "sheet_gdrive_id",
        "doc_gdrive_id",
        "slide_gdrive_id",
    ]
    if os.path.exists(output_path):
        with open(output_path, "r") as jsonFile:
            data = json.load(jsonFile)
            if all(key in data for key in required_keys) and not dict_args.force:
                print("Script already run. Use --force to override.")
                exit(0)

    creds, _ = google.auth.default()
    service = build("drive", "v3", credentials=creds)
    print(folder_name)
    results = (
        service.files()
        .list(
            q=f"name='{folder_name}'",
            pageSize=10,
            fields="nextPageToken, files(id, name)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        )
        .execute()
    )

    if len(results["files"]) == 0:
        print(" folder not found")
        GDRIVE_FOLDER_ID = create_folder(folder_name)
    else:
        print(" folder Already Exists, so using the same")
        GDRIVE_FOLDER_ID = results["files"][0]["id"]
    share_file(GDRIVE_FOLDER_ID, service_account_email)
    MarketingExcelID = upload_with_conversion(
        GDRIVE_FOLDER_ID,
        f"{templates_path}/[data source] GenAI for Marketing.xlsx",
        "GenAI for Marketing.xlsx",
        "text/xls",
    )
    MarketingDocID = upload_with_conversion(
        GDRIVE_FOLDER_ID,
        f"{templates_path}/[template] Gen AI for Marketing Google Doc Template.docx",
        "Gen AI for Marketing Google Doc Template.docx",
        "text/doc",
    )
    MarketingPptID = upload_with_conversion(
        GDRIVE_FOLDER_ID,
        f"{templates_path}/[template] Marketing Assets.pptx",
        "Marketing Assets.pptx",
        "text/ppt",
    )

    if not os.path.exists(output_path):
        data = {}
    else:
        with open(output_path, "r") as jsonFile:
            data = json.load(jsonFile)

    data["folder_gdrive_id"] = GDRIVE_FOLDER_ID
    data["sheet_gdrive_id"] = MarketingExcelID
    data["doc_gdrive_id"] = MarketingDocID
    data["slide_gdrive_id"] = MarketingPptID
    data["execution_time"] = f"{time.time() - start_time:.2f} seconds"

    with open(output_path, "w") as jsonFile:
        json.dump(data, jsonFile)
