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


from io import BytesIO
import io
import streamlit as st


def get_default_image_bytesio(
        image_path: str,
        selected_image_key: str,
        display_image: bool = False) -> BytesIO:
    with open(image_path, 'rb') as fp:
        image = io.BytesIO(fp.read())
    st.session_state[selected_image_key] = image
    if display_image:
        st.write("**Currently select image:**")
        st.image(image)
