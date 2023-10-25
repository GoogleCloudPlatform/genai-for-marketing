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
import pyrebase
from .body_schema import Campaign, CampaignList
import json
from google.cloud import secretmanager
import tomllib


# Load configuration file
with open("/code/app/config.toml", "rb") as f:
    config = tomllib.load(f)

# Fetch Secret Configuration
secret_client = secretmanager.SecretManagerServiceClient()
secret_name = config['global']['secret_name']
secret_response = secret_client.access_secret_version(name=secret_name)
firebaseConfig = secret_response.payload.data.decode("UTF-8")

firebaseConfig = json.loads(firebaseConfig)

# Application Default credentials are automatically created.
app = firebase_admin.initialize_app()
db = firestore.client()
pb = pyrebase.initialize_app(firebaseConfig)


def to_serializable(val):
    if hasattr(val, '__dict__'):
        return val.__dict__
    return val

def create_user(email,password):
    user = auth.create_user(
        email=email,
        password=password
    )
    return user.uid   

def authenticate(email,password):
    try:
       user = pb.auth().sign_in_with_email_and_password(email, password)
       jwt = user['idToken']
       return {'token': jwt}
    except:
       return 'There was an error logging in'
    
def validate(jwt):
    user = auth.verify_id_token(jwt)
    return user["uid"]

def create_campaign(userid,campaign:Campaign):
    user_ref = db.collection("users").document(userid)
    if user_ref.get().exists:
        print("Found user")
    print(json.dumps(campaign.__dict__,default=to_serializable))
    update_time, campaign_ref = user_ref.collection("campaigns").add(json.loads(json.dumps(campaign.__dict__,default=to_serializable)))

    return update_time,campaign_ref.id


def read_campaign(userid,campaignid):
    campaign_ref = db.collection("users").document(userid).collection("campaigns").document(campaignid)
    return campaign_ref.to_dict()

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
    
def delete_campaign(user_id,campaign_id):
    camp_ref = db.collection("users").document(user_id).collection("campaigns").document(campaign_id)
    if camp_ref.get().exists:
        print("Deleting Campaign")
        camp_ref.delete()
        return f"{campaign_id} Campaign is deleted."
    return f"{campaign_id} Campaign does not exists."
