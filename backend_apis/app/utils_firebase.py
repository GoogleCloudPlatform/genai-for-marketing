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
Utility module for Firestore.
"""

import firebase_admin
from firebase_admin import firestore,credentials, auth
import os
from .body_schema import Campaign, CampaignList
import json
import tomllib
import google.oauth2.id_token
import google.auth.transport.requests

#Auth Request
HTTP_REQUEST = google.auth.transport.requests.Request()

# Load configuration file
with open("/app/config.toml", "rb") as f:
    config = tomllib.load(f)

# Application Default credentials are automatically created.
app = firebase_admin.initialize_app()
db = firestore.client()

def to_serializable(val):
    if hasattr(val, '__dict__'):
        return val.__dict__
    return val

def verify_auth_token(id_token):
    # Verify Firebase auth.
    claims = google.oauth2.id_token.verify_firebase_token(
        id_token, HTTP_REQUEST, audience=os.environ.get("GOOGLE_CLOUD_PROJECT")
    )
    if not claims:
        return "000"
    
    user_id = claims['sub']
    friendly_id = claims.get("name", claims.get("email", "Unknown"))
    print(friendly_id)
    return user_id

def create_campaign(user_id,campaign:Campaign):
    user_ref = db.collection("users").document(user_id)
    if user_ref.get().exists:
        print("Found user")
    print(json.dumps(campaign.__dict__,default=to_serializable))
    update_time, campaign_ref = user_ref.collection("campaigns").add(json.loads(json.dumps(campaign.__dict__,default=to_serializable)))

    return update_time,campaign_ref.id


def read_campaign(user_id,campaign_id):
    campaign_ref = db.collection("users").document(user_id).collection("campaigns").document(campaign_id)
    camp = campaign_ref.get()
    if camp.exists:
        return camp.to_dict()
    else:
        return {}

def list_campaigns(user_id):
    campaign_col = db.collection("users").document(user_id).collection("campaigns").stream()
    list_campaigns = []
    for campaign in campaign_col:
        camp_dict = campaign.to_dict()
        print(camp_dict)
        list_campaigns.append(CampaignList(id=campaign.id,data=Campaign(**camp_dict)))
    return list_campaigns

def update_campaign(user_id,campaign_id,data:Campaign):
    camp_ref = db.collection("users").document(user_id).collection("campaigns").document(campaign_id)
    if camp_ref.get().exists:
        print("Updating Campaign")
        camp_ref.set(json.loads(json.dumps(data.__dict__,default=to_serializable)))
        return f"{campaign_id} Campaign is updated."

def update_status(user_id,campaign_id,key,status):
    camp_ref = db.collection("users").document(user_id).collection("campaigns").document(campaign_id)
    if camp_ref.get().exists:
        if key == "":
            camp_ref.update({"status" : status})
            return f"{campaign_id} Campaign Status Updated."
        print("Updating Status for",key)
        camp_ref.update({key+".status" : status})
        return f"{campaign_id} Campaign {key} is Activated."
    
        
def delete_campaign(user_id,campaign_id):
    camp_ref = db.collection("users").document(user_id).collection("campaigns").document(campaign_id)
    if camp_ref.get().exists:
        print("Deleting Campaign")
        camp_ref.delete()
        return f"{campaign_id} Campaign is deleted."
    return f"{campaign_id} Campaign does not exists."

