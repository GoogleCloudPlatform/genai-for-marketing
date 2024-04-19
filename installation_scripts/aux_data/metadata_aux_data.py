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


def get_metadata_data(DATASET_ID: str = 'cdp_dataset') -> list:
  return [{
    "dataset_id": DATASET_ID,
    "table_id": "events",
    "column_id": "event_id",
    "description": "A unique identifier for the event.",
    "is_primary_key": "true",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "events",
    "column_id": "event_date",
    "description": "The date of the event.",
    "is_primary_key": "false",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "events",
    "column_id": "event_type",
    "description": "The type of event.",
    "is_primary_key": "false",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "customers",
    "column_id": "customer_id",
    "description": "A unique identifier of the customer.",
    "is_primary_key": "true",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "customers",
    "column_id": "email",
    "description": "The customer's email address.",
    "is_primary_key": "false",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "customers",
    "column_id": "city",
    "description": "The city where the customer lives.",
    "is_primary_key": "false",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "customers",
    "column_id": "state",
    "description": "The state where the customer lives.",
    "is_primary_key": "false",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "customers",
    "column_id": "channel",
    "description": "The channel through which the customer was acquired.",
    "is_primary_key": "false",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "customers",
    "column_id": "total_purchases",
    "description": "The total number of purchases made by the customer.",
    "is_primary_key": "false",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "customers",
    "column_id": "total_value",
    "description": "The total value of all purchases made by the customer.",
    "is_primary_key": "false",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "customers",
    "column_id": "total_emails",
    "description": "The total number of emails opened by the customer.",
    "is_primary_key": "false",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "customers",
    "column_id": "loyalty_score",
    "description": "A score that measures the customer's engagement with the company.",
    "is_primary_key": "false",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "customers",
    "column_id": "is_media_follower",
    "description": "Whether the customer is a social media follower.",
    "is_primary_key": "false",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "customers",
    "column_id": "last_sign_up_date",
    "description": "The date the customer signed up.",
    "is_primary_key": "false",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "customers",
    "column_id": "last_purchase_date",
    "description": "The date the customer made their last purchase.",
    "is_primary_key": "false",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "customers",
    "column_id": "last_activity_date",
    "description": "The date of the customer's last account activity.",
    "is_primary_key": "false",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "customers",
    "column_id": "cart_total",
    "description": "The value of the items in the customer's shopping cart.",
    "is_primary_key": "false",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "transactions",
    "column_id": "transaction_id",
    "description": "A unique identifier for the transaction.",
    "is_primary_key": "true",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "transactions",
    "column_id": "transaction_quantity",
    "description": "The quantity of items purchased in the transaction.",
    "is_primary_key": "false",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "transactions",
    "column_id": "transaction_value",
    "description": "The total value of the transaction.",
    "is_primary_key": "false",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "transactions",
    "column_id": "transaction_type",
    "description": "The type of transaction (e.g., purchase, refund, etc.).",
    "is_primary_key": "false",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "transactions",
    "column_id": "app_purchase_qnt",
    "description": "The value of the in-app purchase.",
    "is_primary_key": "false",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "transactions",
    "column_id": "is_purchase_online",
    "description": "Whether the purchase was made online.",
    "is_primary_key": "false",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "transactions",
    "column_id": "transaction_date",
    "description": "The date the transaction was made.",
    "is_primary_key": "false",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "transactions",
    "column_id": "product_name",
    "description": "The name of the product that was purchased.",
    "is_primary_key": "false",
    "is_foreign_key": "false"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "events",
    "column_id": "customer_id",
    "description": "A unique identifier of the customer.",
    "is_primary_key": "false",
    "is_foreign_key": "true"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "transactions",
    "column_id": "customer_id",
    "description": "A unique identifier of the customer.",
    "is_primary_key": "false",
    "is_foreign_key": "true"
  }, {
    "dataset_id": DATASET_ID,
    "table_id": "transactions",
    "column_id": "product_id",
    "description": "The code of the inventory item that was purchased.",
    "is_primary_key": "false",
    "is_foreign_key": "true"
  }]