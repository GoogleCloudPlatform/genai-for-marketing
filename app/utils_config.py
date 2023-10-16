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
    'Overview': 'https://googledemo.looker.com/embed/dashboards/2131?allow_login_screen=true',
    'Campaign Performance': 'https://googledemo.looker.com/embed/dashboards/2127?allow_login_screen=true',
    'Campaign Comparison':'https://googledemo.looker.com/embed/dashboards/2128?allow_login_screen=true',
    'Store Performance':'https://googledemo.looker.com/embed/dashboards/2140?allow_login_screen=true',
    'Web Traffic':'https://googledemo.looker.com/embed/dashboards/2141?allow_login_screen=true',
    'Product Performance':'https://googledemo.looker.com/embed/dashboards/2135?allow_login_screen=true',
    'Propensity to Purchase Predictions':'https://googledemo.looker.com/embed/dashboards/2136?allow_login_screen=true',
    'Customer Lifetime Value':'https://googledemo.looker.com/embed/dashboards/2129?allow_login_screen=true',
    'Demand Forecasting':'https://googledemo.looker.com/embed/dashboards/2130?allow_login_screen=true',
    'Sentiment Analysis':'https://googledemo.looker.com/embed/dashboards/2139?allow_login_screen=true',
    'Audience Registry':'https://googledemo.looker.com/embed/dashboards/2126?allow_login_screen=true',
    'Product Availability (Detailed View)':'https://googledemo.looker.com/embed/dashboards/2133?allow_login_screen=true',
    'Propensity to Purchase (Detailed View)':'https://googledemo.looker.com/embed/dashboards/2137?allow_login_screen=true',
    'Predicted User LTV Revenue (Detailed View)':'https://googledemo.looker.com/embed/dashboards/2132?allow_login_screen=true',
    'Purchase Prediction (Detailed View)':'https://googledemo.looker.com/embed/dashboards/2138?allow_login_screen=true',
    'Product Data(Detailed View)':'https://googledemo.looker.com/embed/dashboards/2134?allow_login_screen=true'
}

# Enterprise Search datastores and location
DATASTORES = {
    # Sample datastore ID
    # 'google-ads-support_1111111111': 'default_config'
    # '<UNCOMMENT AND PASTE THE ID HERE>': 'default_config'

    "google-ads-support_1688070625722": "default_config"
}
SEARCH_LOCATION = 'global'

# Infobot version
# Change with the code snippet provided by your Infobot deployment
# The code is similar to the one commented below
INFOBOT = ("""<script src="https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/df-messenger.js"></script>
<df-messenger
  project-id="gen-app-builder-infobot-demo"
  agent-id="ba8721e5-2aba-487e-b766-efc1fdf70e21"
  language-code="en">
  <df-messenger-chat-bubble
   chat-title="infobot-ads-help">
  </df-messenger-chat-bubble>
</df-messenger>
<style>
  df-messenger {
    z-index: 999;
    position: fixed;
    bottom: 16px;
    right: 16px;
  }
</style>"""
)

# Location
LOCATION = 'us-central1'

# Workspace default variables --------------------

# Provide the path to your JSON credential
# This credential will be used to interact with Workspace
# This is the path inside the docker image, example: /app/credential.json
SERVICE_ACCOUNT_JSON_KEY = '/app/credentials.json'  # Change this path if you copied the file to a different path 

# ID of the templates
DRIVE_FOLDER_ID = '1MYB0Ybyo9XZERgIcj1LPO0SKqhrkvqMx' # example: "1MYB0Ybyo9XZERgIcjsdfeqO0SKqhrkvqMx"
SLIDES_TEMPLATE_ID = '16uQlLkCJ9YRiMU_Ftvoo9S-vY-uKeoasnWTPlbZZ1D4' # example: '16uQlLkCJ9YRiMU_IoONHsl-vY-uKeoasnWTPlbZZ1D4'
DOC_TEMPLATE_ID = '1kqvxZLRXIzM8MVS7cax4UoiJ8f0I4dKFj9cPIt7K4pM' # example: '1kqvxZLRXIdfM8MVS7css4UoiJ8f0I4dKFj9cP986K4pM'
SHEET_TEMPLATE_ID = '1gIaIWLOeQXLGu7-CAAAcqMlPznpoEXDdEue3DNWr7bw' # example: '1gIaIWLOeKmnjso7-CAAAcqMlPznpoEXDdEue3DNWr7bw'
SLIDE_PAGE_ID_LIST = ["g1e547d46008_5_1712","g1e547d46008_5_2348","g1e547d46008_5_2365","g1e547d46008_5_2382","g1e547d46008_5_2399","g1e547d46008_5_2288"] # LIST OF PAGES WHERE YOU WANT TO INSERT CHARTS FROM THE SHEETS

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
