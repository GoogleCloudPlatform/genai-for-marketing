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
import utils_workspace
import zipfile

from io import BytesIO
from utils_campaign import generate_names_uuid_dict 
from utils_config import GLOBAL_CFG, MODEL_CFG, PAGES_CFG

page_cfg = PAGES_CFG["12_review_activate"]

# Set project parameters 
PROJECT_ID = GLOBAL_CFG["project_id"]
LOCATION = GLOBAL_CFG["location"]
TEXT_MODEL_NAME = MODEL_CFG["text"]["text_model_name"]
IMAGE_MODEL_NAME = MODEL_CFG["image"]["image_model_name"]
CAMPAIGNS_KEY = PAGES_CFG["campaigns"]["campaigns_key"]

# Variables for Workspace integration
SLIDES_TEMPLATE_ID = page_cfg["slides_template_id"]
SLIDES_PAGE_ID_LIST = page_cfg["slide_page_id_list"]
DOC_TEMPLATE_ID = page_cfg["doc_template_id"]
DRIVE_FOLDER_ID = page_cfg["drive_folder_id"]
SHEET_TEMPLATE_ID = page_cfg["sheet_template_id"]

PAGE_PREFIX_KEY = "Content_Activation"
SELECTED_CAMPAIGN_KEY = f"{PAGE_PREFIX_KEY}_Selected_Campaign"
SLIDE_ID_KEY = f"{PAGE_PREFIX_KEY}_slide_id_key"
DOC_ID_KEY = f"{PAGE_PREFIX_KEY}_doc_id_key"
SHEET_ID_KEY = f"{PAGE_PREFIX_KEY}_sheet_id_key"
NEW_FOLDER_KEY = f"{PAGE_PREFIX_KEY}_new_folder_id_key"


st.set_page_config(
    page_title=page_cfg["page_title"], 
    page_icon=page_cfg["page_icon"])

import utils_styles
utils_styles.sidebar_apply_style(
    utils_styles.style_sidebar,
    page_cfg["sidebar_image_path"]
)

cols = st.columns([15, 85])
with cols[0]:
    st.image(page_cfg["page_title_icon"])
with cols[1]:
    st.title(page_cfg["page_title"])


if CAMPAIGNS_KEY not in st.session_state:
    st.info("Please create a campaign first")
else:
    with st.form(PAGE_PREFIX_KEY+"_Choose_A_Campaign"):
        st.write("**Choose a campaign to preview and edit**")
        selected_campaign = st.selectbox(
            "List of campaigns", 
            generate_names_uuid_dict().keys())
        choose_a_campaign_button = st.form_submit_button()

    if choose_a_campaign_button:
        st.session_state[SELECTED_CAMPAIGN_KEY] = generate_names_uuid_dict()[
            selected_campaign]


def content_activated():
    with st.spinner('Activation in progress...'):
        time.sleep(3)
    st.success('Activation completed')

# campaign = None
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

    # Audiences
    if campaign is not None and isinstance(campaign.audiences, pd.DataFrame):
        with st.expander("📚 Audiences", expanded=False):
            st.subheader("📚 Audiences")
            st.dataframe(campaign.audiences)
            st.download_button(
                label='⬇️ Download Audience',
                data=campaign.audiences.to_csv().encode('utf-8'),
                file_name='audiences.csv',
                mime='text/csv'
            )

    # Trendspotting news articles
    if campaign is not None and isinstance(
        campaign.trendspotting_summaries, pd.DataFrame):
        with st.expander("📚 Trendspotting News Summaries", expanded=False):
            st.subheader("📚 Trendspotting News Summaries")
            st.dataframe(campaign.trendspotting_summaries)
            st.download_button(
                label='⬇️ Download News Summaries',
                data=campaign.trendspotting_summaries.to_csv().encode('utf-8'),
                file_name='trendspotting_summaries.csv',
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
    if campaign is not None and isinstance(campaign.emails, pd.DataFrame):
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
            
            col1, col2, col3 = st.columns([20, 37, 43])

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


# ----------------------Workspace code----------------------

    link = ('http://drive.google.com/corp/drive/folders/'
            f'{campaign.workspace_assets["folder_id"]}')
    st.write("**Google Workspace Integration** | "
            f"[Explore the assets folder in Google Drive ↗]({link})")
    upload_to_drive_button = st.button(
        "Upload available assets to Google Drive")

    if upload_to_drive_button:
        # Asset group
        if (campaign is not None and 
            isinstance(campaign.asset_classes_images, pd.DataFrame) and 
            isinstance(campaign.asset_classes_text, pd.DataFrame)):    
            with st.spinner('Uploading assets to Google Drive...'):
                csv_bytes = io.BytesIO(str.encode(
                    campaign.asset_classes_text.to_csv()))
                try:
                    utils_workspace.upload_to_folder(
                        f=csv_bytes, 
                        folder_id=campaign.workspace_assets["folder_id"],
                        upload_name='assets_group_pmax.csv',
                        mime_type='text/csv')

                    files_bytes_io = []
                    for i, image_bytes in enumerate(
                        campaign.asset_classes_images.iloc[0]):
                        base64_data = re.sub(
                            '^data:image/.+;base64,', '', image_bytes)
                        byte_data = base64.b64decode(base64_data)
                        files_bytes_io.append(BytesIO(byte_data))
                        f = io.BytesIO(byte_data)
                        utils_workspace.upload_to_folder(
                            f=f, 
                            folder_id=campaign.workspace_assets["folder_id"],
                            upload_name=f'image_{i}.png', 
                            mime_type='image/png')
                    st.info("Upload to Drive completed.")
                except:
                    st.error("Network Issue.")
        else:
            st.info("Please link an asset group to the campaign "
                    "at the 'Asset Group for PMax' page")
        
    add_slide_button = st.button("Generate Workspace assets")

    if add_slide_button:
        with st.spinner('Generating Google Slides ...'):
            try:
                slide_id = utils_workspace.copy_drive_file(
                    drive_file_id=SLIDES_TEMPLATE_ID,
                    parentFolderId=campaign.workspace_assets["folder_id"],
                    copy_title="Marketing Assets")
                st.session_state[CAMPAIGNS_KEY][
                    st.session_state[SELECTED_CAMPAIGN_KEY]].workspace_assets[
                        "slide_id"] = slide_id
                
                sheet_id = utils_workspace.copy_drive_file(
                    drive_file_id=SHEET_TEMPLATE_ID,
                    parentFolderId=campaign.workspace_assets["folder_id"],
                    copy_title="GenAI Marketing Data Source")            
                st.session_state[CAMPAIGNS_KEY][
                    st.session_state[SELECTED_CAMPAIGN_KEY]].workspace_assets[
                        "sheet_id"] = sheet_id

                utils_workspace.merge_slides(
                    presentation_id=slide_id,
                    spreadsheet_id=sheet_id,
                    spreadsheet_template_id=SHEET_TEMPLATE_ID,
                    slide_page_id_list=SLIDES_PAGE_ID_LIST)

            except Exception as e:
                print(e)
                st.error("Something went wrong. Please try again.")
            else:
                components.iframe(
                    f'https://docs.google.com/file/d/{slide_id}/preview',
                    height=430)
                doc_id = st.session_state[CAMPAIGNS_KEY][
                    st.session_state[SELECTED_CAMPAIGN_KEY]].workspace_assets[
                        "brief_docs_id"]
                components.iframe(
                    f'https://docs.google.com/file/d/{doc_id}/preview',
                    height=600)
                with st.expander("Check Google Sheet Data Source",
                                    expanded=False):
                    components.iframe(
                        f'https://docs.google.com/file/d/{sheet_id}/preview',
                        height=600)
