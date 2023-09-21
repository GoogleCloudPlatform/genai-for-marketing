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

"""Module to manage Workspace elements"""

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from typing import Any


def create_folder_in_folder(
        folder_name: str, 
        parent_folder_id: str,
        credentials: Any):
    file_metadata = {
    'name' : folder_name,
    'parents' : [parent_folder_id],
    'mimeType' : 'application/vnd.google-apps.folder'
    }
    service = build('drive', 'v3', credentials=credentials)
    file = service.files().create(body=file_metadata,
                                    fields='id').execute()
    
    return file.get('id')


def copy_drive_file(drive_file_id: str,
                    parentFolderId: str,
                    copy_title: str,
                    credentials: Any):
    
    drive_service = build('drive', 'v3', credentials=credentials)
    body = {
        'name': copy_title,
            'parents' : [ parentFolderId  ]
    }
    drive_response = drive_service.files().copy(
        fileId=drive_file_id, body=body).execute()
    presentation_copy_id = drive_response.get('id')

    return presentation_copy_id

def upload_to_folder(
        f,
        folder_id, 
        upload_name, 
        mime_type,
        credentials):
    """Upload a file to the specified folder and prints file ID, folder ID
    Args: Id of the folder
    Returns: ID of the file uploaded"""

    # create drive api client
    service = build('drive', 'v3', credentials=credentials)

    file_metadata = {
        'name': upload_name,
        'parents': [folder_id]
    }
    
    media = MediaIoBaseUpload(f, mimetype=mime_type)

    file = service.files().create(body=file_metadata, media_body=media,
                                fields='id').execute()

    return file.get('id')


def update_doc(
        document_id: str,
        campaign_name: str,
        business_name: str, 
        scenario: str,
        brand_statement: str, 
        primary_msg: str, 
        comms_channel: str,
        credentials: Any):
    
    requests = [
            {
            'replaceAllText': {
                'containsText': {
                    'text': '{{campaign-name}}',
                    'matchCase':  'true'
                },
                'replaceText': campaign_name,
            }},
            {
            'replaceAllText': {
                'containsText': {
                    'text': '{{business-name}}',
                    'matchCase':  'true'
                },
                'replaceText': business_name,
            }}, 
            {
            'replaceAllText': {
                'containsText': {
                    'text': '{{scenario-brief}}',
                    'matchCase':  'true'
                },
                'replaceText': scenario,
            }},
            {
            'replaceAllText': {
                'containsText': {
                    'text': '{{brand-statement}}',
                    'matchCase':  'true'
                },
                'replaceText': brand_statement,
            }},
            {
            'replaceAllText': {
                'containsText': {
                    'text': '{{primary-msg}}',
                    'matchCase':  'true'
                },
                'replaceText': primary_msg,
            }},
            {
            'replaceAllText': {
                'containsText': {
                    'text': '{{comms-channel}}',
                    'matchCase':  'true'
                },
                'replaceText': comms_channel,
            }}
    ]
    service = build('docs', 'v1', credentials=credentials)
    service.documents().batchUpdate(
        documentId=document_id, body={'requests': requests}).execute()


def set_permission(
        file_id: str,
        credentials: Any):
    
    permission = {'type': 'domain',
                'domain': 'google.com', 
                'role': 'writer'}
    service = build('drive', 'v3', credentials=credentials)
    return service.permissions().create(fileId=file_id,
                                        sendNotificationEmail=False,
                                        body=permission).execute()


