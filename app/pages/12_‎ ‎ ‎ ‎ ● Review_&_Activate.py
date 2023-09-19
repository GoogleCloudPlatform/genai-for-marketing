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
Content Activation:
"""

import base64
import io
import pandas as pd
import re
import streamlit as st
import streamlit.components.v1 as components
import time
import tomllib
import uuid
import zipfile

from googleapiclient import discovery
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
from io import BytesIO
from utils_campaign import Campaign, generate_names_uuid_dict 


# Load configuration file
with open("./app_config.toml", "rb") as f:
    data = tomllib.load(f)

# Set project parameters 
PROJECT_ID = data["global"]["project_id"]
LOCATION = data["global"]["location"]
TEXT_MODEL_NAME = data["models"]["text"]["text_model_name"]
IMAGE_MODEL_NAME = data["models"]["image"]["image_model_name"]
CAMPAIGNS_KEY = data["pages"]["campaigns"]["campaigns_key"]

# Variables for Workspace integration
SCOPES = data["pages"]["12_review_activate"]["workspace_scopes"]
SLIDES_TEMPLATE_ID = data["pages"]["12_review_activate"]["slides_template_id"]
DOC_TEMPLATE_ID = data["pages"]["12_review_activate"]["doc_template_id"]
DRIVE_FOLDER_ID = data["pages"]["12_review_activate"]["drive_folder_id"]
SHEET_TEMPLATE_ID = data["pages"]["12_review_activate"]["sheet_template_id"]
service_account_json_key = data["global"]["service_account_json_key"]
creds = service_account.Credentials.from_service_account_file(
    filename=service_account_json_key, scopes=SCOPES)
new_folder_id = DRIVE_FOLDER_ID


PAGE_PREFIX_KEY = "Content_Activation"
SELECTED_CAMPAIGN_KEY = f"{PAGE_PREFIX_KEY}_Selected_Campaign"
SLIDE_ID_KEY = f"{PAGE_PREFIX_KEY}_slide_id_key"
DOC_ID_KEY = f"{PAGE_PREFIX_KEY}_doc_id_key"
SHEET_ID_KEY = f"{PAGE_PREFIX_KEY}_sheet_id_key"
NEW_FOLDER_KEY = f"{PAGE_PREFIX_KEY}_new_folder_id_key"


st.set_page_config(
    page_title=data["pages"]["12_review_activate"]["page_title"], 
    page_icon=data["pages"]["12_review_activate"]["page_icon"])

import utils_styles
utils_styles.sidebar_apply_style(
    utils_styles.style_sidebar,
    data["pages"]["12_review_activate"]["sidebar_image_path"]
)

cols = st.columns([15, 85])
with cols[0]:
    st.image(data["pages"]["12_review_activate"]["page_title_icon"])
with cols[1]:
    st.title(data["pages"]["12_review_activate"]["page_title"])


def render_openlink_button(link:str, button_text:str):
    st.markdown(
    f"""
        <a href="{link}" class="rounded-button">{button_text}</a>
    """, 
    unsafe_allow_html=True)

campaign_list = []
if CAMPAIGNS_KEY not in st.session_state:
    st.info("Please create a campaign first")
else:
    campaign_list = generate_names_uuid_dict().keys()

    with st.form(PAGE_PREFIX_KEY+"_Choose_A_Campaign"):
        st.write("**Choose a campaign to preview and edit**")
        selected_campaign = st.selectbox("List of campaigns", campaign_list)
        choose_a_campaign_button = st.form_submit_button()

    if choose_a_campaign_button:
        st.session_state[SELECTED_CAMPAIGN_KEY] = generate_names_uuid_dict()[
            selected_campaign]


def content_activated():
    with st.spinner('Activation in progress...'):
        time.sleep(3)
    st.success('Activation completed')

campaign: Campaign|None = None

if SELECTED_CAMPAIGN_KEY in st.session_state:
    campaign = st.session_state[CAMPAIGNS_KEY][st.session_state[
        SELECTED_CAMPAIGN_KEY]]

    st.subheader('Available assets')

    # Creative brief
    if campaign is not None and isinstance(campaign.brief, dict):
        with st.expander("📋 Campaign Brief", expanded=False):
            st.subheader("📋 Campaign Brief")
            campaign.brief = st.data_editor(campaign.brief)
            
            col1, col2, col3 = st.columns([20, 30, 50])

            with col1:
                is_button_clicked = st.button(":loudspeaker: Send Brief")
            if is_button_clicked:
                with st.spinner('Activation in progress...'):
                    time.sleep(3)
                st.success('Activation completed')
            
            with col2:
                st.download_button(
                    label='⬇️ Download Brief',
                    data=pd.DataFrame().from_dict(
                        campaign.brief, orient='index', columns=['assets']
                    ).to_csv().encode('utf-8'),
                    file_name='creative_brief.csv',
                    mime='text/csv'
                )

    # Asset group
    if (campaign is not None and
        isinstance(campaign.asset_classes_images, pd.DataFrame) and 
        isinstance(campaign.asset_classes_text, pd.DataFrame)):
        with st.expander("📚 Asset Classes", expanded=False):
            col1, col2 = st.columns([9,91])
            with col1:
                st.image(
                    "https://upload.wikimedia.org/wikipedia/commons/c/c7/Google_Ads_logo.svg",
                    width=60)
            with col2:
                st.subheader("Asset Classes")

            campaign.asset_classes_text = st.data_editor(
                campaign.asset_classes_text
            )

            st.dataframe(
                campaign.asset_classes_images,
                column_config={f"image_{i}":st.column_config.ImageColumn()
                    for i in range(len(campaign.asset_classes_images.columns))})
            
            col1, col2, col3 = st.columns([17, 33, 50])
            
            with col1:
                is_button_clicked = st.button(":loudspeaker: Activate")
            if is_button_clicked:
                with st.spinner('Activation in progress...'):
                    time.sleep(3)
                st.success('Activation completed')

            with col2:
                files_bytes_io = []
                for i in campaign.asset_classes_images.iloc[0]:
                    base64_data = re.sub('^data:image/.+;base64,', '', i)
                    byte_data = base64.b64decode(base64_data)
                    files_bytes_io.append(BytesIO(byte_data))

                temp_zip_file = BytesIO()

                with zipfile.ZipFile(temp_zip_file,
                                     'a',
                                     zipfile.ZIP_DEFLATED) as zip_file:
                    for idx, value in enumerate(files_bytes_io):
                        zip_file.writestr(f'image_{idx}.png', value.getvalue())
                    zip_file.writestr(
                        'asset_classes_text.csv',
                        campaign.asset_classes_text.to_csv().encode('utf-8'))

                temp_zip_file.seek(0)

                st.download_button(
                    '⬇️ Download Asset Group',
                    data=temp_zip_file.read(),
                    file_name='assets.zip',
                    mime='application/zip',
                )

    # Emails
    if campaign is not None and (campaign.emails, pd.DataFrame):
        with st.expander("✉️ Email Copy", expanded=False):
            st.subheader("✉️ Email Copy")
            campaign.emails = st.data_editor(
                campaign.emails,
                column_config={"imageb64":st.column_config.ImageColumn()})

            col1, col2, col3 = st.columns([22, 28, 50])
            
            with col1:
                is_button_clicked = st.button(":loudspeaker: Send Emails")
            if is_button_clicked:
                with st.spinner('Activation in progress...'):
                    time.sleep(3)
                st.success('Activation completed')

            with col2:
                st.download_button(
                    label='⬇️ Download Emails',
                    data=campaign.emails.to_csv().encode('utf-8'),
                    file_name='emails_copy.csv',
                    mime='text/csv'
                )
                
    #Threads
    if campaign is not None and isinstance(campaign.ads_threads, dict):
        with st.expander("📱 Threads Ads", expanded=False):
            col1, col2 = st.columns([9,91])
            with col1:
                st.image(
                    "https://upload.wikimedia.org/wikipedia/commons/9/9d/Threads_%28app%29_logo.svg",
                    width=60)
            with col2:
                st.subheader("Threads Ads")
            campaign.ads_threads = st.data_editor(campaign.ads_threads)
            
            if 'image' in campaign.ads_threads:
                st.image(campaign.ads_threads["image"])
            
            col1, col2, col3 = st.columns([30, 40, 30])
            
            with col1:
                is_button_clicked = st.button(":loudspeaker: Activate Threads Ads")
            if is_button_clicked:
                with st.spinner('Activation in progress...'):
                    time.sleep(3)
                st.success('Activation completed')

            with col2:
                temp_zip_file = BytesIO()

                with zipfile.ZipFile(temp_zip_file,
                                     'a',
                                     zipfile.ZIP_DEFLATED) as zip_file:
                    if 'image' in campaign.ads_threads:                
                        base64_data = re.sub('^data:image/.+;base64,',
                                             '',
                                             campaign.ads_threads["image"])
                        byte_data = base64.b64decode(base64_data)
                        files_bytes_io = BytesIO(byte_data)
                        zip_file.writestr('threads_image.png',
                                          files_bytes_io.getvalue())
                    
                    zip_file.writestr(
                        'threads_assets.csv', 
                        pd.DataFrame(
                            campaign.ads_threads,
                            index=[0]).to_csv().encode('utf-8'))

                temp_zip_file.seek(0)

                st.download_button(
                    '⬇️ Download Threads Ad',
                    data=temp_zip_file.read(),
                    file_name='threads_ad.zip',
                    mime='application/zip',
                )

    # Instagram Ads
    if campaign is not None and isinstance(campaign.ads_insta, dict):
        with st.expander("📱 Instagram Ads", expanded=False):
            col1, col2 = st.columns([9,91])
            with col1:
                st.image("https://upload.wikimedia.org/wikipedia/commons/9/95/Instagram_logo_2022.svg")
            with col2:
                st.subheader("Instagram Ads")
            campaign.ads_insta = st.data_editor(campaign.ads_insta)

            if 'image' in campaign.ads_insta:
                st.image(campaign.ads_insta["image"])

            col1, col2, col3 = st.columns([32, 34, 34])
            
            with col1:
                is_button_clicked = st.button(
                    ":loudspeaker: Activate Instagram Ads")
            if is_button_clicked:
                with st.spinner('Activation in progress...'):
                    time.sleep(3)
                st.success('Activation completed')

            with col2:
                temp_zip_file = BytesIO()

                with zipfile.ZipFile(temp_zip_file,
                                     'a',
                                     zipfile.ZIP_DEFLATED) as zip_file:
                    if 'image' in campaign.ads_insta:                
                        base64_data = re.sub('^data:image/.+;base64,',
                                             '',
                                             campaign.ads_insta["image"])
                        byte_data = base64.b64decode(base64_data)
                        files_bytes_io = BytesIO(byte_data)
                        zip_file.writestr('instagram_image.png',
                                          files_bytes_io.getvalue())
                    
                    zip_file.writestr(
                        'instagram_assets.csv', 
                        pd.DataFrame(
                            campaign.ads_insta,
                            index=[0]).to_csv().encode('utf-8'))

                temp_zip_file.seek(0)

                st.download_button(
                    '⬇️ Download Instagram Ad',
                    data=temp_zip_file.read(),
                    file_name='instagram_ad.zip',
                    mime='application/zip',
                )

    # Website
    if campaign is not None and isinstance(campaign.website_post, dict):
        with st.expander("🖥️ Website Post", expanded=False):
            st.subheader("🖥️ Website Post")
            campaign.website_post = st.data_editor(campaign.website_post)
            st.image(campaign.website_post["website_image"])
            
            col1, col2, col3 = st.columns([16, 34, 50])

            with col1:
                is_button_clicked = st.button(":loudspeaker: Publish")
            if is_button_clicked:
                with st.spinner('Activation in progress...'):
                    time.sleep(3)
                st.success('Activation completed')

            with col2:
                temp_zip_file = BytesIO()

                with zipfile.ZipFile(temp_zip_file,
                                     'a',
                                     zipfile.ZIP_DEFLATED) as zip_file:
                    if 'website_image' in campaign.website_post:                
                        base64_data = re.sub(
                            '^data:image/.+;base64,',
                            '',
                            campaign.website_post["website_image"])
                        byte_data = base64.b64decode(base64_data)
                        files_bytes_io = BytesIO(byte_data)
                        zip_file.writestr('instagram_image.png',
                                          files_bytes_io.getvalue())

                    zip_file.writestr(
                        'website_post.csv', 
                        pd.DataFrame(
                            campaign.website_post,
                            index=[0]).to_csv().encode('utf-8'))

                temp_zip_file.seek(0)

                st.download_button(
                    '⬇️ Download Post',
                    data=temp_zip_file.read(),
                    file_name='website_post.zip',
                    mime='application/zip',
                )

    # Celebration
    if (campaign is not None and 
        isinstance(campaign.brief, dict) and 
        isinstance(campaign.asset_classes_images, pd.DataFrame) and 
        isinstance(campaign.asset_classes_text, pd.DataFrame) and
        isinstance(campaign.emails, pd.DataFrame) and 
        isinstance(campaign.ads_threads, dict) and 
        isinstance(campaign.ads_insta, dict) and 
        isinstance(campaign.website_post, dict)):
        
        is_button_clicked = st.button("🎈 Let's Celebrate!!!")
        if is_button_clicked:
            st.balloons()

# ----------------------Workspace code----------------------
# ----------------------Workspace code----------------------

if SELECTED_CAMPAIGN_KEY in st.session_state:
    def merge_slide(presentation_id: str, spreadsheet_id:str):

        emu4m = {
            'magnitude': 4000000,
            'unit': 'EMU'
        }
        
        sheet_chart_id_list = get_chart_id(SHEET_TEMPLATE_ID)
        page_list = data["pages"]["12_review_activate"]["slide_page_id_list"]

        service = build('slides', 'v1', credentials=creds)
        from datetime import date

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

        for chart_id,page_id in zip(sheet_chart_id_list,page_list):
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
        service.presentations().batchUpdate(
            presentationId=presentation_id, body=body).execute()
            


    def copy_drive_file(drive_file_id: str,
                        parentFolderId: str,
                        copy_title: str):
       
        drive_service = build('drive', 'v3', credentials=creds)
        body = {
            'name': copy_title,
                'parents' : [ parentFolderId  ]
        }
        drive_response = drive_service.files().copy(
            fileId=drive_file_id, body=body).execute()
        presentation_copy_id = drive_response.get('id')

        return presentation_copy_id

    def upload_to_folder(f,folder_id, upload_name, mime_type):
        """Upload a file to the specified folder and prints file ID, folder ID
        Args: Id of the folder
        Returns: ID of the file uploaded"""

       
    
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'name': upload_name,
            'parents': [folder_id]
        }
        
        media = MediaIoBaseUpload(f, mimetype=mime_type)
    
        file = service.files().create(body=file_metadata, media_body=media,
                                    fields='id').execute()
    
        return file.get('id')

    def update_doc(document_id: str, business_name: str, Scenario: str,
                   brand_statement: str, primary_msg: str, comms_channel: str):
        
        requests = [
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
                        'text': '{{Scenario}}',
                        'matchCase':  'true'
                    },
                    'replaceText': Scenario,
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
        service = build('docs', 'v1', credentials=creds)
        service.documents().batchUpdate(
            documentId=document_id, body={'requests': requests}).execute()


    def get_chart_id(spreadsheet_id):
        service = discovery.build('sheets', 'v4', credentials=creds)
        spreadsheet_id = spreadsheet_id  
        ranges = [] 
        include_grid_data = False 

    
        request = service.spreadsheets().get(spreadsheetId=spreadsheet_id,
                                             ranges=ranges,
                                             includeGridData=include_grid_data)
        response = request.execute()

        chart_id_list = []
        for chart in response['sheets'][0]['charts']:
            chart_id_list.append(chart['chartId'])
        return chart_id_list
        

    def create_sheets_chart(presentation_id: str, page_id: str,
                            spreadsheet_id: str, sheet_chart_id: str):
     
        slides_service = build('slides', 'v1', credentials=creds)
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
      
    
    def create_folder_in_folder(folder_name: str, parent_folder_id: str):
        
        file_metadata = {
        'name' : folder_name,
        'parents' : [parent_folder_id],
        'mimeType' : 'application/vnd.google-apps.folder'
        }
        service = build('drive', 'v3', credentials=creds)
        file = service.files().create(body=file_metadata,
                                        fields='id').execute()
        
        return file.get('id')
        

    def set_permission(file_id: str):
        
        permission = {'type': 'domain',
                    'domain': 'google.com', 
                    'role': 'writer'}
        service = build('drive', 'v3', credentials=creds)
        return service.permissions().create(fileId=file_id,
                                            sendNotificationEmail=False,
                                            body=permission).execute()
    
    if NEW_FOLDER_KEY in st.session_state and st.session_state[NEW_FOLDER_KEY]:
        new_folder_id = st.session_state[NEW_FOLDER_KEY]
    else:
        ts = int(time.time())
        new_folder_id = create_folder_in_folder(f"Marketing_Assets_{ts}",
                                                new_folder_id)
        st.session_state[NEW_FOLDER_KEY] = new_folder_id
        set_permission(new_folder_id)
    st.divider()
    link = f'http://drive.google.com/corp/drive/folders/{new_folder_id}'
    st.write("**Google Workspace Integration** | "
            f"[Explore the assets folder in Google Drive 🡭]({link})")
    upload_to_drive_button = st.button("Upload available assets to Google Drive")

    if upload_to_drive_button:
        # Asset group
        if (campaign is not None and 
            isinstance(campaign.asset_classes_images, pd.DataFrame) and 
            isinstance(campaign.asset_classes_text, pd.DataFrame)):    
            with st.spinner('Uploading assets to Google Drive...'):
                csv_bytes = io.BytesIO(str.encode(
                    campaign.asset_classes_text.to_csv()))
                try:
                    upload_to_folder(csv_bytes, new_folder_id,
                                     'assets.csv','text/csv')

                    files_bytes_io = []
                    c=0
                    for i in campaign.asset_classes_images.iloc[0]:
                        base64_data = re.sub('^data:image/.+;base64,', '', i)
                        byte_data = base64.b64decode(base64_data)
                        files_bytes_io.append(BytesIO(byte_data))
                        f = io.BytesIO(byte_data)
                        upload_to_folder(f, new_folder_id,
                                         f'image_{c}.png', 'image/png')
                        c+=1            
                    st.info("Upload is done. "
                            "Click on 'Explore the assets "
                            "folder in Google Drive' link "
                            "to see the files.")
                except:
                    st.error("Network Issue.")
        else:
            st.info("Please link an asset group to the campaign "
                    "at the 'Asset Group for PMax' page")
        
    add_slide_button = st.button("Generate Workspace assets")

    if add_slide_button:
        with st.spinner('Generating slides and docs...'):
            try:
                slide_id = copy_drive_file(SLIDES_TEMPLATE_ID,
                                           new_folder_id,
                                           " Marketing Assets")        
                st.session_state[SLIDE_ID_KEY] = slide_id
                sheet_id = copy_drive_file(SHEET_TEMPLATE_ID,
                                           new_folder_id,
                                           "GenAI Marketing Data Source")            
                st.session_state[SHEET_ID_KEY] = sheet_id
                merge_slide(slide_id,sheet_id)
                doc_id = copy_drive_file(DOC_TEMPLATE_ID,
                                         new_folder_id,
                                         "GenAI Marketing Demo Summary")
                st.session_state[DOC_ID_KEY] = doc_id
                
                brief_dict = {}
                if campaign is not None and campaign.brief is not None:
                    brief_dict = campaign.brief
                
                business_name = brief_dict.get('business_name', 'Cymbal') 
                Scenario = brief_dict.get(
                    'brief_scenario',
                    'Targeting gender: Women, Age group: 20-30, '
                    'Campaign objective: Drive Awareness, '
                    'Competitor: Fashion Forward')
                brand_statement = brief_dict.get(
                    'brand_statement',
                    'Mission: To create stylish, affordable jewelry '
                    'that women love to wear. '
                    'Goals: To drive awareness of Cymbal brand '
                    'and products among women ages 20-30.').replace('*','')
                primary_msg = brief_dict.get(
                    'primary_message',
                    'Cymbal is a fashion brand for women aged 20-30. '
                    'We are a modern, stylish brand '
                    'that offers high-quality clothing and accessories '
                    'at affordable prices. '
                    'We are committed to providing our customers with the '
                    'best possible shopping experience.').replace('*','')
                comms_channel = brief_dict.get(
                    'comm_channels',
                    'Social media is a great way to reach a large audience '
                    'of potential customers. '
                    'You can create engaging content that will capture '
                    'their attention and make them want '
                    'to learn more about your brand. '
                    'Make sure to use high-quality images and videos, '
                    'and use clear and concise language.').replace('*','')
                
                update_doc(doc_id, business_name, Scenario, brand_statement,
                           primary_msg, comms_channel)
            except Exception as e:
                print(e)
                st.error("Network Issue.")
            else:
                if (SLIDE_ID_KEY in st.session_state and 
                    st.session_state[SLIDE_ID_KEY]):
                    slide_id = st.session_state[SLIDE_ID_KEY]
                    components.iframe(
                        f'https://docs.google.com/file/d/{slide_id}/preview',
                        height=430)
                if (DOC_ID_KEY in st.session_state and 
                    st.session_state[DOC_ID_KEY]):
                    doc_id = st.session_state[DOC_ID_KEY]
                    components.iframe(
                        f'https://docs.google.com/file/d/{doc_id}/preview',
                        height=600)
                if (SHEET_ID_KEY in st.session_state and 
                    st.session_state[SHEET_ID_KEY]):   
                    sheet_id = st.session_state[SHEET_ID_KEY]
                    with st.expander("Check Google Sheet Data Source",
                                     expanded=False):
                        components.iframe(
                            f'https://docs.google.com/file/d/{sheet_id}/preview',
                            height=600)
