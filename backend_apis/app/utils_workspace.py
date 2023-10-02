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

"""Module to manage Workspace integration"""

import io
import uuid

from datetime import date
from googleapiclient.http import HttpError, MediaIoBaseUpload
from googleapiclient.http import MediaIoBaseDownload


def create_folder_in_folder(
        drive_service,
        folder_name: str, 
        parent_folder_id: str
    ):
    file_metadata = {
        'name' : folder_name,
        'parents' : [parent_folder_id],
        'mimeType' : 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                    fields='id').execute()
    
    return file.get('id')


def download_file(drive_service, file_id: str) -> bytes | None:
    try:
        request = drive_service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(F'Download {int(status.progress() * 100)}.')
    except HttpError as error:
        print(f'An error occured: {error}')
        return None
    return file.getvalue()


def copy_drive_file(
        drive_service,
        drive_file_id: str,
        parentFolderId: str,
        copy_title: str):
    body = {
        'name': copy_title,
        'parents' : [parentFolderId]
    }
    drive_response = drive_service.files().copy(
        fileId=drive_file_id, body=body).execute()
    presentation_copy_id = drive_response.get('id')

    return presentation_copy_id


def upload_to_folder(
        drive_service,
        f,
        folder_id, 
        upload_name, 
        mime_type):
    """Upload a file to the specified folder and prints file ID, folder ID
    Args: Id of the folder
    Returns: ID of the file uploaded"""
    file_metadata = {
        'name': upload_name,
        'parents': [folder_id]
    }
    
    media = MediaIoBaseUpload(
        f, 
        mimetype=mime_type)

    file = drive_service.files().create(
        body=file_metadata, 
        media_body=media,
        fields='id').execute()

    return file.get('id')


def update_doc(
        docs_service,
        document_id: str,
        campaign_name: str,
        business_name: str, 
        scenario: str,
        brand_statement: str, 
        primary_msg: str, 
        comms_channel: str):
    
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
    docs_service.documents().batchUpdate(
        documentId=document_id, body={'requests': requests}).execute()


def set_permission(
        drive_service,
        file_id: str):
    
    permission = {'type': 'domain',
                'domain': 'google.com', 
                'role': 'writer'}
    return drive_service.permissions().create(fileId=file_id,
                                        sendNotificationEmail=False,
                                        body=permission).execute()


def get_chart_id(
        sheets_service,
        spreadsheet_id):
    spreadsheet_id = spreadsheet_id  
    ranges = [] 
    include_grid_data = False 
    request = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id,
                                            ranges=ranges,
                                            includeGridData=include_grid_data)
    response = request.execute()

    chart_id_list = []
    for chart in response['sheets'][0]['charts']:
        chart_id_list.append(chart['chartId'])

    return chart_id_list


def merge_slides(
        slides_service,
        presentation_id: str, 
        spreadsheet_id: str,
        spreadsheet_template_id: str,
        slide_page_id_list: list):
    emu4m = {
        'magnitude': 4000000,
        'unit': 'EMU'
    }

    sheet_chart_id_list = get_chart_id(
        spreadsheet_template_id)

    today = date.today()
    requests = [
            {
                'replaceAllText': {
                    'containsText': {
                        'text': '{{date}}',
                        'matchCase': True
                    },
                    'replaceText': str(today)
                }
            }
        ]

    for chart_id,page_id in zip(sheet_chart_id_list , slide_page_id_list):
        presentation_chart_id = str(uuid.uuid4())
        requests.append({
        'createSheetsChart': {
            'objectId': presentation_chart_id,
            'spreadsheetId': spreadsheet_id,
            'chartId': chart_id,
            'linkingMode': 'LINKED',
            'elementProperties': {
                'pageObjectId': page_id,
                'size': {
                    'height': emu4m,
                    'width': emu4m
                },
                'transform': {
                    'scaleX': 1,
                    'scaleY': 1,
                    'translateX': 100000,
                    'translateY': 100000,
                    'unit': 'EMU'
                }
            }
        }
        })

    body = {
        'requests': requests
    }
    slides_service.presentations().batchUpdate(
        presentationId=presentation_id, body=body).execute()


def create_sheets_chart(
        slides_service,
        presentation_id: str, 
        page_id: str,
        spreadsheet_id: str, 
        sheet_chart_id: str):
    emu4m = {
        'magnitude': 1000000,
        'unit': 'EMU'
    }

    presentation_chart_id = 'MyEmbeddedChart'
    requests = [
        {
            'createSheetsChart': {
                'objectId': presentation_chart_id,
                'spreadsheetId': spreadsheet_id,
                'chartId': sheet_chart_id,
                'linkingMode': 'LINKED',
                'elementProperties': {
                    'pageObjectId': page_id,
                    'size': {
                        'height': emu4m,
                        'width': emu4m
                    },
                    'transform': {
                        'scaleX': 0.5,
                        'scaleY': 0.5,
                        'translateX': 2,
                        'translateY': 2,
                        'unit': 'EMU'
                    }
                }
            }
        }
    ]

    # Execute the request.
    body = {
        'requests': requests
    }
    response = slides_service.presentations().batchUpdate(
        presentationId=presentation_id, body=body).execute()
    
    return response
