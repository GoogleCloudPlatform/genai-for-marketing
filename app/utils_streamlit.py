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
Utility module to reset the state of a page or the application.
"""


import streamlit as st


def reset_page_state(prefix: str):
    """Reset the state of a specific streamlit page

    Args:
        prefix (str): Identifier of the page
    """
    for key in st.session_state:
        if key.startswith(prefix) or key.startswith(f"FormSubmitter:{prefix}"):
            del st.session_state[key]


def reset_st_state():
    '''Reset the state of all streamlit pages'''
    for key in st.session_state:
        del st.session_state[key]

