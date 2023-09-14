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
Configuration variables to be used by the streamlit app.
"""

# Infobot version
# Change with the code snippet provided by your Infobot deployment
# The code is similar to the one commented below
INFOBOT = (
#  '''<script src="https://www.gstatic.com/dialogflow-console/fast/messenger-cx/bootstrap.js?v=1"></script>
# <df-messenger
#   df-cx="true"
#   chat-title="Ads Helper Chatbot"
#   agent-id="XXXXXXXXXXXXXXX"
#   language-code="en"
# ></df-messenger>
#     '''
)


# Workspace default variables --------------------

# Provide the path to your JSON credential
# This credential will be used to interact with Workspace
# This is the path inside the docker image, example: /app/credential.json
SERVICE_ACCOUNT_JSON_KEY = '/app/credentials.json'  # Change this path if you copied the file to a different path 

# ID of the templates
DRIVE_FOLDER_ID = '<DRIVE FOLDER ID>' # example: "1MYB0Ybyo9XZERgIcjsdfeqO0SKqhrkvqMx"
SLIDES_TEMPLATE_ID = '<SLIDES TEMPLATE ID>' # example: '16uQlLkCJ9YRiMU_IoONHsl-vY-uKeoasnWTPlbZZ1D4'
DOC_TEMPLATE_ID = '<DOCS TEMPLATE ID>' # example: '1kqvxZLRXIdfM8MVS7css4UoiJ8f0I4dKFj9cP986K4pM'
SHEET_TEMPLATE_ID = '<SHEETS TEMPLATE ID>' # example: '1gIaIWLOeKmnjso7-CAAAcqMlPznpoEXDdEue3DNWr7bw'
SLIDE_PAGE_ID_LIST = ["p3","p4","p5","p6","p7","p8"] # LIST OF PAGES WHERE YOU WANT TO INSERT CHARTS FROM THE SHEETS

# Scope for the Workspace API - don't change
WORKSPACE_SCOPES = [
    'https://www.googleapis.com/auth/presentations',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.resource',
    'https://www.googleapis.com/auth/documents']
