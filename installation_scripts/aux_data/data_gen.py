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


from google.cloud import bigquery
from aux_data.metadata_aux_data import get_metadata_data
from typing import List, Dict
import numpy as np
from datetime import datetime, timedelta

SEED = 1
rng = np.random.default_rng(SEED)


def create_and_populate_customers(num_customers: int = 50000) -> List[Dict]:
    from aux_data.customers_aux_data import channel, locations
    
    customers_location = rng.choice(locations, size=(num_customers))
    customers_channel = rng.choice(channel, size=(num_customers))
    customers_total_purchases = rng.integers(1, 100, size=(num_customers))
    customers_total_value = rng.integers(10, 1000, size=(num_customers))
    customers_total_emails = rng.integers(1, 100, size=(num_customers))
    customers_loyalty_score = rng.integers(1, 100, size=(num_customers))
    customers_is_media_follower = rng.choice([False, True], size=(num_customers))

    baseline_datetime = datetime(2023, 4, 1)
    customers_last_sign_up_date = rng.integers(500, 1000, size=(num_customers))
    customers_last_purchase_date = rng.integers(20, 100, size=(num_customers))
    customers_last_activity_date = customers_last_purchase_date - rng.integers(10, 20, size=(num_customers))

    customers_cart_total = rng.uniform(0.0, 800.0, size=(num_customers))

    customers_data = []

    for i in range(num_customers):
        customer = {}
        customer['customer_id'] = int(i)
        customer['email'] = f'user{i}@sample_user{i}.sample'
        customer['city'] = customers_location[i]['city']
        customer['state'] = customers_location[i]['state']
        customer['channel'] = customers_channel[i]['channel']
        customer['total_purchases'] = int(customers_total_purchases[i])
        customer['total_value'] = int(customers_total_value[i])
        customer['total_emails'] = int(customers_total_emails[i])
        customer['loyalty_score'] = int(customers_loyalty_score[i])
        customer['is_media_follower'] = bool(customers_is_media_follower[i])

        customer['last_sign_up_date'] = baseline_datetime - timedelta(days=int(customers_last_sign_up_date[i]))
        customer['last_sign_up_date'] = customer['last_sign_up_date'].strftime('%Y-%m-%d')

        customer['last_purchase_date'] = baseline_datetime - timedelta(days=int(customers_last_purchase_date[i]))
        customer['last_purchase_date'] = customer['last_purchase_date'].strftime('%Y-%m-%d')

        customer['last_activity_date'] = baseline_datetime - timedelta(days=int(customers_last_activity_date[i]))
        customer['last_activity_date'] = customer['last_activity_date'].strftime('%Y-%m-%d')

        customer['cart_total'] = round(float(customers_cart_total[i]), 2)

        customers_data.append(customer)

    return customers_data


# Generate and load events table to BQ
def create_and_populate_events(num_customers: int = 50000) -> Dict:
    from aux_data.events_aux_data import event_type

    events_per_customer = list(map(int, np.absolute(np.floor(rng.normal(1, 1, size=(num_customers)) * 100))))
    num_events = sum(events_per_customer)
    
    events_type = rng.choice(event_type, size=(num_events))
    
    baseline_datetime = datetime(2023, 4, 1)
    events_date_delta = rng.integers(20, 200, size=(num_events))
    
    events_data = []
    idx = 0

    for i in range(num_customers):
        for _ in range(events_per_customer[i]):
            event = {}
            event['customer_id'] = i
            event['event_id'] = idx
            event['event_date'] = baseline_datetime - timedelta(days=int(events_date_delta[idx]))
            event['event_date'] = event['event_date'].strftime('%Y-%m-%d')
            event['event_type'] = events_type[idx]['event_type']
            idx += 1
            events_data.append(event)
    return events_data


# Generate and load transactions to BQ
def create_and_populate_transactions(num_customers: int = 50000) -> Dict:
    from aux_data.transactions_aux_data import product_name, transaction_type

    transactions_per_customer = list(map(int, np.absolute(np.floor(rng.normal(1, 1, size=(num_customers)) * 100))))
    num_transactions = sum(transactions_per_customer)

    product_name_choice = rng.choice(product_name, size=(num_transactions))
    transaction_type_choice = rng.choice(transaction_type, size=(num_transactions))

    transaction_qtn = rng.integers(1, 30, size=(num_transactions))
    transaction_value = rng.integers(1, 5000, size=(num_transactions))
    app_purchase_quantity = rng.integers(1, 10, size=(num_transactions))

    transaction_is_online = rng.choice([False, True], size=(num_transactions))

    baseline_datetime = datetime(2023, 4, 1)
    transactions_date_delta = rng.integers(20, 200, size=(num_transactions))
    
    transaction_data = []

    transaction_id = 0
    for i in range(num_customers):
        for _ in range(transactions_per_customer[i]):
            transaction = {}
            transaction['transaction_id'] = transaction_id
            transaction['customer_id'] = i
            transaction['transaction_quantity'] = int(transaction_qtn[transaction_id])
            transaction['transaction_value'] = int(transaction_value[transaction_id])
            transaction['transaction_type'] = transaction_type_choice[transaction_id]['transaction_type']
            transaction['app_purchase_quantity'] = int(app_purchase_quantity[transaction_id])
            transaction['is_online'] = bool(transaction_is_online[transaction_id])

            transaction['transaction_date'] = baseline_datetime - timedelta(days=int(transactions_date_delta[transaction_id]))
            transaction['transaction_date'] = transaction['transaction_date'].strftime('%Y-%m-%d')
            
            transaction['product_name'] = product_name_choice[transaction_id]['product_name']
            transaction['product_id'] = product_name_choice[transaction_id]['product_id']

            transaction_id += 1
            transaction_data.append(transaction)
    
    return transaction_data


def generate_and_populate_dataset(
        PROJECT_ID: str,
        DATASET_ID: str,
        create_tables: bool = True
):
    bq_client = bigquery.Client(project=PROJECT_ID)

    # Define tables schema
    customers_schema = [
        bigquery.SchemaField('customer_id', 'INTEGER', mode='NULLABLE'),
        bigquery.SchemaField('email', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('city', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('state', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('channel', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('total_purchases', 'INTEGER', mode='NULLABLE'),
        bigquery.SchemaField('total_value', 'INTEGER', mode='NULLABLE'),
        bigquery.SchemaField('total_emails', 'INTEGER', mode='NULLABLE'),
        bigquery.SchemaField('loyalty_score', 'INTEGER', mode='NULLABLE'),
        bigquery.SchemaField('is_media_follower', 'BOOLEAN', mode='NULLABLE'),
        bigquery.SchemaField('last_sign_up_date', 'DATE', mode='NULLABLE'),
        bigquery.SchemaField('last_purchase_date', 'DATE', mode='NULLABLE'),
        bigquery.SchemaField('last_activity_date', 'DATE', mode='NULLABLE'),
        bigquery.SchemaField('cart_total', 'FLOAT', mode='NULLABLE')
    ]

    events_schema = [
        bigquery.SchemaField('customer_id', 'INTEGER', mode='NULLABLE'),
        bigquery.SchemaField('event_id', 'INTEGER', mode='NULLABLE'),
        bigquery.SchemaField('event_date', 'DATE', mode='NULLABLE'),
        bigquery.SchemaField('event_type', 'STRING', mode='NULLABLE')
    ]

    transactions_schema = [
        bigquery.SchemaField('transaction_id', 'INTEGER', mode='NULLABLE'),
        bigquery.SchemaField('customer_id', 'INTEGER', mode='NULLABLE'),
        bigquery.SchemaField('transaction_quantity', 'INTEGER', mode='NULLABLE'),
        bigquery.SchemaField('transaction_value', 'INTEGER', mode='NULLABLE'),
        bigquery.SchemaField('transaction_type', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('app_purchase_quantity', 'INTEGER', mode='NULLABLE'),
        bigquery.SchemaField('is_online', 'BOOLEAN', mode='NULLABLE'),
        bigquery.SchemaField('transaction_date', 'DATE', mode='NULLABLE'),
        bigquery.SchemaField('product_name', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('product_id', 'INTEGER', mode='NULLABLE')
    ]

    metadata_schema = [
        bigquery.SchemaField('dataset_id', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('table_id', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('column_id', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('description', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('is_primary_key', 'BOOLEAN', mode='NULLABLE'),
        bigquery.SchemaField('is_foreign_key', 'BOOLEAN', mode='NULLABLE')
    ]

    if(create_tables):
        print('Creating tables ...')
        for table_id, table_schema in zip(['customers', 'events', 'transactions', 'metadata'], 
                            [customers_schema, events_schema, transactions_schema, metadata_schema]):
            table_id = f'{PROJECT_ID}.{DATASET_ID}.{table_id}'
            table = bigquery.Table(table_id, schema=table_schema)
            table = bq_client.create_table(table)


    print('Generating and populating METADATA table ...')    
    table_id = f"{PROJECT_ID}.{DATASET_ID}.metadata"
    bq_client.load_table_from_json(
        get_metadata_data(DATASET_ID=DATASET_ID), 
        destination=bigquery.Table(table_ref=table_id, schema=metadata_schema)
    )

    print('Generating and populating CUSTOMERS table ...')
    customers_data = create_and_populate_customers()
    table_id = f"{PROJECT_ID}.{DATASET_ID}.customers"
    bq_client.load_table_from_json(
        customers_data, 
        destination=bigquery.Table(table_ref=table_id, schema=customers_schema))
    
    print('Generating and populating EVENTS table ...')
    events_data = create_and_populate_events()
    table_id = f"{PROJECT_ID}.{DATASET_ID}.events"
    bq_client.load_table_from_json(
        events_data, 
        destination=bigquery.Table(table_ref=table_id, schema=events_schema))
    
    print('Generating and populating TRANSACTIONS table ...')
    transactions_data = create_and_populate_transactions()
    table_id = f"{PROJECT_ID}.{DATASET_ID}.transactions"
    bq_client.load_table_from_json(
        transactions_data, 
        destination=bigquery.Table(table_ref=table_id, schema=transactions_schema))