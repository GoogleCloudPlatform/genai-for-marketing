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
Utility module to create a campaign and add to campaign state
"""


from dataclasses import dataclass
import streamlit as st 
import uuid
import pandas as pd

from utils_config import PAGES_CFG



CAMPAIGNS_KEY = PAGES_CFG["campaigns"]["campaigns_key"]

@dataclass
class Campaign:
    unique_uuid: uuid.UUID
    name: str
    emails: pd.DataFrame | None = None
    brief: dict | None = None
    website_post: dict | None = None
    ads_threads: dict | None = None
    ads_insta: dict | None = None
    asset_classes_text: pd.DataFrame | None = None
    asset_classes_images: pd.DataFrame | None = None
    workspace_assets: dict | None = None
    trendspotting_summaries: list | None = None
    audiences: pd.DataFrame | None = None
    campaign_uploaded_images: dict | None = None
    theme: str = ""


def add_new_campaign(name: str) -> str:
    new_uuid = uuid.uuid4()
    campaign = Campaign(unique_uuid=new_uuid, name=name)
    if CAMPAIGNS_KEY not in st.session_state:
        st.session_state[CAMPAIGNS_KEY] = {}
    st.session_state[CAMPAIGNS_KEY][str(new_uuid)] = campaign
    return str(new_uuid)


def generate_names_uuid_dict() -> dict:
    if CAMPAIGNS_KEY not in st.session_state:
        return {}
    elif not st.session_state[CAMPAIGNS_KEY]:
        return {}
    else:
        campaigns = st.session_state[CAMPAIGNS_KEY].values()
        return {campaign.name: str(campaign.unique_uuid) for campaign in campaigns} 
