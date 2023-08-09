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


import os
import requests

# Model versions
TEXT_MODEL_NAME = 'text-bison'
IMAGE_MODEL_NAME = 'imagegeneration'
CODE_MODEL_NAME = 'code-bison'

# Looker Dashboards
# The link of the looker Dashboard must follow this format:
# https://<LOOKER INSTANCE URL>/embed/dashboards/<DASHBOARD NUMBER>?allow_login_screen=true
DASHBOARDS = {
    # Sample Dashboard link
    # 'Overview': 'https://mydomain.looker.com/embed/dashboards/1111?allow_login_screen=true'
}

# Enterprise Search datastores and location
DATASTORES = {
    # Sample datastore ID
    # 'google-ads-support_1111111111': 'default_config'
    # '<UNCOMMENT AND PASTE THE ID HERE>': 'default_config'
}
SEARCH_LOCATION = 'global'

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

# Location
LOCATION = 'us-central1'

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

# Google Translation API languages
TRANSLATE_LANGUAGES = {
    "Spanish": "es",
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Assamese": "as",
    "Aymara": "ay",
    "Azerbaijani": "az",
    "Bambara": "bm",
    "Basque": "eu",
    "Belarusian": "be",
    "Bengali": "bn",
    "Bhojpuri": "bho",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chinese (Simplified)": "zh",
    "Chinese (Traditional)": "zh-TW",
    "Corsican": "co",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dhivehi": "dv",
    "Dogri": "doi",
    "Dutch": "nl",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Ewe": "ee",
    "Filipino (Tagalog)": "fil",
    "Finnish": "fi",
    "French": "fr",
    "Frisian": "fy",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Guarani": "gn",
    "Gujarati": "gu",
    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hmong": "hmn",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Igbo": "ig",
    "Ilocano": "ilo",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jv",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Khmer": "km",
    "Kinyarwanda": "rw",
    "Konkani": "gom",
    "Korean": "ko",
    "Krio": "kri",
    "Kurdish": "ku",
    "Kurdish (Sorani)": "ckb",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Lingala": "ln",
    "Lithuanian": "lt",
    "Luganda": "lg",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Maithili": "mai",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Meiteilon (Manipuri)": "mni-Mtei",
    "Mizo": "lus",
    "Mongolian": "mn",
    "Myanmar (Burmese)": "my",
    "Nepali": "ne",
    "Norwegian": "no",
    "Nyanja (Chichewa)": "ny",
    "Odia (Oriya)": "or",
    "Oromo": "om",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese (Portugal, Brazil)": "pt",
    "Punjabi": "pa",
    "Quechua": "qu",
    "Romanian": "ro",
    "Russian": "ru",
    "Samoan": "sm",
    "Sanskrit": "sa",
    "Scots Gaelic": "gd",
    "Sepedi": "nso",
    "Serbian": "sr",
    "Sesotho": "st",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhala (Sinhalese)": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tagalog (Filipino)": "tl",
    "Tajik": "tg",
    "Tamil": "ta",
    "Tatar": "tt",
    "Telugu": "te",
    "Thai": "th",
    "Tigrinya": "ti",
    "Tsonga": "ts",
    "Turkish": "tr",
    "Turkmen": "tk",
    "Twi (Akan)": "ak",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uyghur": "ug",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Zulu": "zu"
}


# Get project ID from metadata
def get_env_project_id() -> str:
    """Returns the Project ID from GAE or Cloud Run"""
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    
    if not project_id:
        project_id = requests.get(
            "http://metadata.google.internal/computeMetadata/v1/project/project-id", 
            headers={"Metadata-Flavor":"Google"}
        ).text

    return project_id
