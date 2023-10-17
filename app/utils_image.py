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
Utility module to:
 - Resize image bytes
 - Generate an image with Imagen
 - Edit an image with Imagen
 - Render the image generation and editing UI
"""


import io
import base64
import math

from proto import Message
from utils_config import GLOBAL_CFG, MODEL_CFG
import utils_edit_image

from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
from PIL import Image
import streamlit as st
from streamlit_image_select import image_select
from typing import List

from utils_workspace import download_file


# Confoguration variables for Vertex AI
PROJECT_ID = GLOBAL_CFG["project_id"]
LOCATION = GLOBAL_CFG["location"]
MODEL_NAME = MODEL_CFG["image"]["image_model_name"]
IMAGEN_API_ENDPOINT = f'{LOCATION}-aiplatform.googleapis.com'
IMAGEN_ENDPOINT = f'projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{MODEL_NAME}'
IMAGE_UPLOAD_BYTES_LIMIT = 10 ** 7


def render_image_file(
        image_path: str,
        selected_image_key: str,
        display_image: bool = False):
    with open(image_path, 'rb') as fp:
        image = io.BytesIO(fp.read())
    st.session_state[selected_image_key] = image
    if display_image:
        st.write("**Currently select image:**")
        st.image(image)


def resize_image_bytes(
        bytes_data: bytes, 
        bytes_limit: int=IMAGE_UPLOAD_BYTES_LIMIT) -> bytes:
    """Resizes an image to a specified byte limit.

    Args:
        bytes_data: 
            The image data in bytes. (bytes)
        bytes_limit: 
            The maximum byte size of the resized image. (int)

    Returns:
        The resized image data in bytes.

    Raises:
        Image.ImageTooBigError: If the image is larger than the bytes_limit.
    """
    with io.BytesIO(bytes_data) as buffer_in:
        img_to_resize = Image.open(buffer_in)
        width = img_to_resize.size[0]
        aspect = img_to_resize.size[0] / img_to_resize.size[1]
        bytes_size = len(bytes_data)

        while bytes_size > bytes_limit :    
            resize_factor = bytes_size / (bytes_limit*0.9)
            width = width / math.sqrt(resize_factor)  
            height = width / aspect
            # resize from img_orig to not lose quality
            img = img_to_resize.resize((int(width), int(height)))
            
            with io.BytesIO() as buffer_out:
                img.save(buffer_out, format="PNG")
                bytes_data = buffer_out.getvalue()
                bytes_size = len(bytes_data)
    
    return bytes_data


def predict_large_language_model_sample(
    api_endpoint: str,
    endpoint: str,
    input: dict,
    parameters: dict 
) -> list:
    """Predicts the output of a large language model on a given input.

    Args:
        api_endpoint: 
            The API endpoint of the AI Platform Prediction service. (str)
        endpoint: 
            The name of the endpoint to use for predictions. (str)
        input: 
            The input to the large language model. (str)
        parameters: 
            The parameters for the prediction. (str)

    Returns:
        A list of strings containing the predictions.

    Raises:
        aiplatform.exceptions.NotFoundError: If the endpoint does not exist.
        aiplatform.exceptions.BadRequestError: If the input is invalid.
        aiplatform.exceptions.InternalServerError: If an internal error occurred.
    """

    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    client = aiplatform.gapic.PredictionServiceClient(
        client_options=client_options
    )
    instance = json_format.ParseDict(input, Value())
    instances = [instance]
    parameters_message = json_format.ParseDict(parameters, Value())
    try:
        response = Message.to_dict(client.predict(
            endpoint=endpoint,
            instances=instances,
            parameters=parameters_message
        ))
    
        return response.get("predictions")
    except:
        return []


def image_generation(
        prompt:str,
        sample_count:int,
        sample_image_size: int,
        aspect_ratio: str,
        state_key: str):
    """Generates an image from a prompt.

    Args:
        prompt: 
            The prompt to use to generate the image.
        sample_count: 
            The number of images to generate.
        sample_image_size: 
            The size of the generated images.
        aspect_ratio: 
            The aspect ratio of the generated images.
        state_key: 
            The key to use to store the generated images in the session state.

    Returns:
        None.
    """

    st.session_state[state_key] = predict_large_language_model_sample(
        api_endpoint=IMAGEN_API_ENDPOINT,
        endpoint=IMAGEN_ENDPOINT,
        input={
            "prompt": prompt
        },
        parameters={
            'sampleCount':sample_count,
            'sampleImageSize':sample_image_size,
            'aspectRatio':aspect_ratio
        }
    )


def edit_image_generation(
        prompt:str,
        sample_count:int,
        bytes_data:bytes,
        state_key: str,
        mask_bytes_data: bytes=b""):
    """Generates an edited image from a prompt and a base image.

    Args:
        prompt: 
            A string that describes the desired edit to the image.
        sample_count: 
            The number of edited images to generate.
        bytes_data: 
            The image data in bytes.
        state_key: 
            The key to store the generated images in the session state.
        mask_bytes_data: 
            The mask data in bytes.

    Returns:
        None.
    """
    input_dict = {
        'prompt': prompt,
        'image': {
            'bytesBase64Encoded': base64.b64encode(bytes_data).decode('utf-8')
        }
    }
    
    if mask_bytes_data:
        input_dict["mask"] = {
            "image": {
                "bytesBase64Encoded": base64.b64encode(
            mask_bytes_data).decode('utf-8')
            }
        }
    
    st.session_state[state_key] = predict_large_language_model_sample(
        api_endpoint=IMAGEN_API_ENDPOINT,
        endpoint=IMAGEN_ENDPOINT,
        input=input_dict,
        parameters={
            'sampleCount':sample_count
        }
    )


def render_one_image(
        images_key: str,
        image_position: int,
        select_button: bool=False,
        selected_image_key: str="",
        edit_button: bool=False,
        image_to_edit_key: str="",
        download_button: bool=True):
    """
    Renders one image from a list of images.

    Args:
        images_key: 
            The key in the session state that stores the list of images.
        image_position: 
            The index of the image to render.
        select_button: 
            Whether to show a button that allows the user to select the image.
        selected_image_key: 
            The key in the session state to store the selected image.
        edit_button: 
            Whether to show a button that allows the user to edit the image.
        image_to_edit_key: 
            The key in the session state to store the edited image.
        download_button: 
            Whether to show a button that allows the user to download the image.

    Returns:
        None.
    """
    image = io.BytesIO(
        base64.b64decode(
        st.session_state[images_key][image_position]["bytesBase64Encoded"])
    )
    st.image(image)
    
    if download_button:
        st.download_button(
            label='Download',
            key=f"_btn_download_{images_key}_{image_position}",
            data=image,
            file_name='image.png',
        )
    
    if select_button and selected_image_key:
        if st.button(
            "Select", key=f"_btn_select_{images_key}_{image_position}"):
            st.session_state[selected_image_key] = image

    if edit_button and image_to_edit_key:
        if st.button("Edit", key=f"_btn_edit_{images_key}_{image_position}"):
            st.session_state[image_to_edit_key] = image.getvalue()


def generate_image_columns(
        images_key: str,
        select_button: bool=False,
        selected_image_key: str="",
        edit_button: bool=False,
        image_to_edit_key: str="",
        download_button: bool=True):
    """Generates a grid of image columns.

    Args:
        images_key (str): 
            The key in the session state that stores the images.
        select_button (bool, optional): 
            Whether to show a button to select the image. Defaults to False.
        selected_image_key (str, optional): 
            The key in the session state that stores the selected image. Defaults to an empty string.
        edit_button (bool, optional): 
            Whether to show a button to edit the image. Defaults to False.
        image_to_edit_key (str, optional): 
            The key in the session state that stores the image to edit. Defaults to an empty string.
        download_button (bool, optional): 
            Whether to show a button to download the image. Defaults to True.

    Returns:
        None.
    """
    image_count = len(st.session_state[images_key])
    counter = 0
    while image_count > 0:
        cols = st.columns([25,25,25,25])
        for i, col in enumerate(cols):
            with col:
                try:
                    render_one_image(
                        images_key,
                        i+counter,
                        select_button,
                        selected_image_key,
                        edit_button,
                        image_to_edit_key,
                        download_button)
                except:
                    continue
        counter+=4
        image_count-=4


def render_image_generation_ui(
        image_text_prompt_key: str,
        generated_images_key: str,
        pre_populated_prompts: List[str] = ["an image of a cat"],
        select_button: bool=False,
        selected_image_key: str='',
        edit_button: bool=False,
        image_to_edit_key: str='',
        download_button: bool=True, 
        auto_submit_first_pre_populated: bool=False):
    """Renders a user interface for generating images.

    Args:
        image_text_prompt_key: 
            The key used to store the user's text prompt in the session state.
        generated_images_key: 
            The key used to store the generated images in the session state.
        pre_populated_prompts: 
            A list of pre-populated prompts.
        select_button: 
            Whether to show a button to select a pre-populated prompt.
        selected_image_key: 
            The key used to store the selected image in the session state.
        edit_button: 
            Whether to show a button to edit the selected image.
        title: 
            The title of the user interface.
        image_to_edit_key: 
            The key used to store the image to edit in the session state.
        download_button: 
            Whether to show a button to download the generated images.
        auto_submit_first_pre_populated: 
            Whether to automatically submit the form with the first prompt.

    Returns:
        None.
    """

    SAMPLE_COUNT = [8, 4, 2, 1]
    SAMPLE_IMAGE_SIZE = [256, 64, 512, 1024]
    # ASPECT_RATIO = ['1:1', '5:4', '3:2', '7:4', '4:3', '16:9', '9:16']
    ASPECT_RATIO = ['1:1']

    
    if image_text_prompt_key in st.session_state:
        st.session_state[
            f"{image_text_prompt_key}_text_area"] = st.session_state[
                image_text_prompt_key]
    
    if auto_submit_first_pre_populated:
        if generated_images_key not in st.session_state:
            with st.spinner('Generating images ...'):
                image_generation(
                    pre_populated_prompts[0],
                    SAMPLE_COUNT[0],
                    SAMPLE_IMAGE_SIZE[0],
                    ASPECT_RATIO[0],
                    generated_images_key)

    if generated_images_key in st.session_state:
        generate_image_columns(
            generated_images_key,
            select_button,
            selected_image_key,
            edit_button,
            image_to_edit_key,
            download_button)


def render_image_edit_prompt(
        edit_image_prompt_key: str,
        edited_images_key: str,
        upload_file: bool=True,
        image_to_edit_key: str="",
        mask_image: bool=False,
        mask_image_key: str="",
        select_button: bool=False,
        selected_image_key: str="",
        download_button: bool=True,
        file_uploader_key: str="",
        campaign_image_dict: dict={},
        local_image_list: list=[]):
    """
    Renders a prompt for editing an image.

    Args:
        edit_image_prompt_key: 
            The key to store the edit image prompt in the session state.
        edited_images_key: 
            The key to store the edited images in the session state.
        upload_file: 
            Whether to allow users to upload an image to edit.
        image_to_edit_key: 
            The key to store the image to edit in the session state.
        mask_image: 
            Whether to allow users to mask the image to edit.
        mask_image_key: 
            The key to store the mask image in the session state.
        select_button: 
            Whether to show a button to select an image to edit.
        selected_image_key: 
            The key to store the selected image in the session state.
        download_button: 
            Whether to show a button to download the edited images.
        file_uploader_key: 
            The key to store the file uploader in the session state.
        campaign_image_dict:
            Dict of image metadata dicts from campaign
        local_image_list:
            List of local image paths

    Returns:
        None.
    """

    
    
    if edit_image_prompt_key in st.session_state:
        st.session_state[
            f"{edit_image_prompt_key}_text_area"] = st.session_state[
                edit_image_prompt_key]
    
    if upload_file:
        expander_title = "Upload an image"
        expanded = True
        if image_to_edit_key in st.session_state:
            expander_title = "Change the uploaded image"
            expanded = False
        with st.expander(expander_title, expanded):
            def add_image_to_state(image_to_edit:bytes | None):
                if image_to_edit is not None:
                    if edited_images_key in st.session_state:
                        del st.session_state[edited_images_key]
                    if selected_image_key in st.session_state:
                        del st.session_state[selected_image_key]

                    st.session_state[image_to_edit_key] = image_to_edit
                    if mask_image and mask_image_key in st.session_state:
                        del st.session_state[mask_image_key]
                else:
                    st.error("Network error. Try Again")


            if campaign_image_dict:
                images = campaign_image_dict.values()
                drive_file = image_select(
                    label="Select an image uploaded to the campaign Drive",
                    images=[im["thumbnail"] for im in images],
                    captions = [im["name"] for im in images],
                    key=f"{file_uploader_key}_drive", 
                    return_value="index",
                    use_container_width=False)
                def select_campaign():
                    if drive_file is not None:
                        image_to_edit = download_file(
                            list(campaign_image_dict.keys())[drive_file])
                        add_image_to_state(image_to_edit)
                    else:
                        st.info("Select a Campaign image first")


                st.button("Select image from Campaign",
                          key=f"{file_uploader_key}_drive_button",
                          on_click=select_campaign)


                st.write('========== or ===========')
            else:
                drive_file = None
            if local_image_list:
                local_file = image_select(
                    "Select a local image",
                    local_image_list, 
                    [caption.split("/")[-1] for caption in local_image_list],
                    key=f"{file_uploader_key}_local",
                    use_container_width=False)
                def select_local():
                    if local_file is not None:
                        with open(local_file, "rb") as f:
                            add_image_to_state(f.read())
                    else:
                        st.info("Select a local image first")


                st.button("Select image from Stock",
                          key=f"{file_uploader_key}_local_button",
                          on_click=select_local)
                st.write('========== or ===========')
            else:
                local_file = None

           
            uploaded_file = st.file_uploader(
                'Upload your image here. It MUST be in PNG or JPEG format.',
                type=['png', 'jpg'],
                key=file_uploader_key)
            def upload_button():
                if uploaded_file is not None:
                    add_image_to_state(uploaded_file.getvalue())
                else:
                    st.info("Select an image for the upload")
            st.button('Upload Image',
                      key=f"{file_uploader_key}_upload_button",
                      on_click=upload_button)
    if image_to_edit_key in st.session_state:
        if mask_image:
            with st.expander(
                "[Optional] Paint where to edit in the image",
                expanded=edited_images_key not in st.session_state):
                utils_edit_image.edit_image_canvas(
                        mask_image_key,
                        resize_image_bytes(
                            st.session_state[image_to_edit_key]))
        else:
            st.image(st.session_state[image_to_edit_key])

        with st.form(key=f"{edit_image_prompt_key}_form"):
            edit_image_prompt = st.text_input(
                'Provide a prompt using natural language to edit the image')
            edit_image_button = st.form_submit_button(label='Edit Image')

        if edit_image_button:
                bytes_data = st.session_state[image_to_edit_key]
            
                if bytes_data:
                    if len(bytes_data) > IMAGE_UPLOAD_BYTES_LIMIT:
                        bytes_data = resize_image_bytes(bytes_data)
                    
                    if not edit_image_prompt:
                        st.error("Provide a prompt for editing the image")
                    else:
                        st.session_state[
                            edit_image_prompt_key] = edit_image_prompt
                        with st.spinner('Generating Edited images ...'):
                            edit_image_generation(
                                st.session_state[edit_image_prompt_key],
                                8,
                                bytes_data,
                                edited_images_key,
                                st.session_state.get(
                                    mask_image_key, b""
                                ) if mask_image and mask_image_key else b"")
                else:
                    st.error("No image found to edit")

            
    if edited_images_key in st.session_state:
        with st.expander("Edited Images",
                         expanded=selected_image_key not in st.session_state):
            generate_image_columns(
                edited_images_key,
                select_button,
                selected_image_key,
                download_button=download_button)


def render_image_generation_and_edition_ui(
        image_text_prompt_key: str,
        generated_images_key: str,
        edit_image_prompt_key: str,
        pre_populated_prompts: List[str]=["an image of a cat"],
        select_button: bool=False,
        selected_image_key: str="",
        edit_button: bool=False,
        image_to_edit_key: str="",
        edit_with_mask: bool=False,
        mask_image_key: str="",
        edited_images_key: str="",
        download_button: bool=False,
        auto_submit_first_pre_populated=False):
    
    render_image_generation_ui(
        image_text_prompt_key,
        generated_images_key,
        pre_populated_prompts,
        select_button,
        selected_image_key,
        edit_button,
        image_to_edit_key,
        download_button,
        auto_submit_first_pre_populated)
    
    if image_to_edit_key in st.session_state:
        render_image_edit_prompt(
            edit_image_prompt_key,
            edited_images_key,
            False,
            image_to_edit_key,
            edit_with_mask,
            mask_image_key,
            select_button,
            selected_image_key,
            download_button)
