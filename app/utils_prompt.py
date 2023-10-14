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
A utility module for performing prompt engineering with the Vertex PaLM API.
"""


import asyncio
import functools
import streamlit as st
import vertexai

from google.cloud import translate_v2 as translate
from vertexai.preview.language_models import TextGenerationModel

from utils_config import TRANSLATE_CFG


translate_client = translate.Client() 

def render_marketing_prompt_design(
        project_id: str,
        location: str,
        state_key: str,
        show_temperature: bool=True,
        temperature: float=0.2,
        show_max_output_tokens: bool=True,
        max_output_tokens: int=1024,
        show_top_k: bool=True,
        top_k: int=40,
        show_top_p: bool=True,
        top_p: float=0.8,
        show_response: bool=True,
        prompt_title: str="Text Generation",
        prompt_label: str="Create and submit your prompt.",
        prompt_example: str="", 
        model_name: str='text-bison',
        translate: bool=False,
        text_area_height: int = 400
):
    """
    Renders a design for:
        - Prompt engineering for marketing text generation
        - Translation

    Args:
        project_id: 
            The ID of the project to use. (str)
        location: 
            The location of the project. (str)
        state_key: 
            The key of the state to use. (str)
        show_temperature: 
            Whether to show the temperature slider. (bool, default=True)
        temperature: 
            The default temperature. (float, default=0.2)
        show_max_output_tokens: 
            Whether to show the max output tokens slider. (bool, default=True)
        max_output_tokens: 
            The default max output tokens. (int, default=1024)
        show_top_k: 
            Whether to show the top k slider. (bool, default=True)
        top_k: 
            The default top k. (int, default=40)
        show_top_p: 
            Whether to show the top p slider. (bool, default=True)
        top_p: 
            The default top p. (float, default=0.8)
        show_response: 
            Whether to show the response area. (bool, default=True)
        prompt_title: 
            The title of the prompt. (str, default="Text Generation")
        prompt_label: 
            The label of the prompt input field. 
            (str, default="Create and submit your prompt.")
        prompt_example: 
            An example prompt. (str, default="")
        model_name: 
            The name of the model to use. (str, default='text-bison@001')
        translate: 
            Whether to show the translate widget for the user. 
            (bool, default=False)
        text_area_height: 
            The height of the text area. (int, default=400)

    Returns:
        None.
    """
    with st.form(key='{state_key}_form'):
        st.write(f"**{prompt_title}**")

        if (show_temperature or show_max_output_tokens or
            show_top_k or show_top_p):
            col1, col2 = st.columns([70,30])

            with col1:
                custom_prompt = st.text_area(
                    f"{prompt_label}",f"{prompt_example}", text_area_height)
            
            with col2:
                st.write('**Model parameters**')
                if show_temperature:
                    temperature = st.slider('Temperature', 0.0, 1.0, 
                                            temperature)
                if show_max_output_tokens:
                    max_output_tokens = st.slider('Max output tokens', 1, 1024,
                                                  max_output_tokens)
                if show_top_k:
                    top_k = st.slider('TopK', 1, 40, top_k)
                if show_top_p:
                    top_p = st.slider('TopP', 0.0, 1.0, top_p)

        else:
            custom_prompt = st.text_area(
                f"{prompt_label}",f"{prompt_example}", text_area_height)

        submit_button = st.form_submit_button(label='Generate')

    if submit_button:
        if not custom_prompt:
            st.info('Provide a valid prompt.')
        else:
            try:
                # Initialize variables
                with st.spinner('Generating response ...'):
                    vertexai.init(project=project_id, location=location)
                    llm = TextGenerationModel.from_pretrained(model_name)
                    response = llm.predict(
                            prompt=custom_prompt,
                            temperature=temperature,
                            max_output_tokens=max_output_tokens,
                            top_k = top_k,
                            top_p = top_p
                        ).text
                
                st.session_state[state_key] = response
            except:
                st.info('An exception occured. '
                        'Review and provide a valid prompt.')
    
    if show_response and state_key in st.session_state:
        st.write('**Response**')
        for i in st.session_state[state_key].split('\n'):
            st.write(i.replace('Headline', '**Headline**'))

        if translate:
            with st.form(key='{state_key}_translate_form'):
                st.write(f"**Translate generated text**")

                target_language_name = st.selectbox(
                    "Languages", options=TRANSLATE_CFG.keys())

                translate_submit_button = st.form_submit_button(
                    label='Translate')

            if translate_submit_button:
                with st.spinner("Translating..."):
                    st.session_state[
                        f'{state_key}_translated_headline'
                    ] = translate_client.translate(
                            'Headline',
                            source_language="en",
                            target_language=TRANSLATE_CFG[
                                target_language_name],
                        ).get("translatedText","")

                    st.session_state[f"{state_key}_translated"] = []
                    for headline in st.session_state[state_key].split('\n'):
                        st.session_state[
                            f"{state_key}_translated"].append(
                                translate_client.translate(
                                    headline,
                                    source_language="en",
                                    target_language=TRANSLATE_CFG[
                                        target_language_name]
                                ).get("translatedText","")
                            )
            if f"{state_key}_translated" in st.session_state:
                st.write('**Translation**')
                for t in st.session_state[f"{state_key}_translated"]:
                    translated_headline = st.session_state[
                        f'{state_key}_translated_headline']
                    st.write(t.replace(translated_headline,
                                       f'**{translated_headline}**'))

async def async_predict_text_llm(
        prompt: str,
        name: str,
        pretrained_model: str,
        max_output_tokens: int=1024,
        temperature: float=0.2,
        top_k: int=40,
        top_p: float=0.8
    )-> str:
    loop = asyncio.get_running_loop()
    llm = TextGenerationModel.from_pretrained(pretrained_model)
    generated_response = None
    with st.spinner(f"Generating {name}"):
        try:
            generated_response = await loop.run_in_executor(
                None,
                functools.partial(
                    llm.predict,
                        prompt=prompt, 
                        temperature=temperature, 
                        max_output_tokens=max_output_tokens, 
                        top_k=top_k, top_p=top_p))
        except Exception as e:
            print(e)

    if generated_response and generated_response.text:
        return generated_response.text
    return ""

