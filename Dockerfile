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


FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Install python packages
RUN pip install google-cloud-datacatalog
RUN pip install db-dtypes
RUN pip install -U google-cloud-aiplatform 
RUN pip install pandas 
RUN pip install google-api-python-client 
RUN pip install python-dateutil 
RUN pip install newspaper3k 
RUN pip install google-cloud-bigquery
RUN pip install -U streamlit
RUN pip install pillow
RUN pip install streamlit-drawable-canvas==0.9.1
RUN pip install streamlit-image-select==0.6.0
RUN pip install google-cloud-discoveryengine
RUN pip install google-cloud-translate
RUN pip install cloudpickle

# Copy local code to the container image.
WORKDIR /app
COPY ./app ./

# Run the web service on container startup
CMD ["streamlit", "run", "Home.py"]
