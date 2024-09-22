import asyncio
import fal_client
import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv
import tempfile
from mistralai import Mistral
from playwright.sync_api import sync_playwright, Playwright
import requests

load_dotenv()

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"
client = Mistral(api_key=api_key)

# Flux generate outfits 
async def get_outfit(prompt: str):
    handler = fal_client.submit(
        "fal-ai/flux-lora",
        arguments={
            "prompt": prompt
        },
    )

    result = handler.get()
    return result

async def get_outfit_with_lora(prompt: str, lora: str):
    handler = fal_client.submit(
        "fal-ai/flux-lora",
        arguments={
            "prompt": prompt,
            "loras": [
                {
                "path": lora
                }
            ],
            "image_size": "landscape_4_3",
            "num_inference_steps": 28,
            "guidance_scale": 3.5,
            "num_images": 1,
            "enable_safety_checker": True,
            "output_format": "jpeg"
        }
    )
    result = handler.get()
    return result['images'][0]

# FAL Try-on API: https://fal.ai/models/fal-ai/cat-vton/api?platform=python
async def try_on(human_image: Image, outfit_image: Image):
    handler = fal_client.submit(
        "fal-ai/cat-vton",
        arguments={
            "human_image_url": human_image,
            "garment_image_url": outfit_image,
            "cloth_type": "overall"
        },
    )

    result = handler.get()
    print("RESULT",result)
    return result['image']

def get_outfit_descriptions(count: int, human_image_url: str):
    handler = fal_client.submit(
        "fal-ai/florence-2-large/caption",
        arguments={
            "image_url": human_image_url
        },
    )
    result = handler.get()
    human_description = result["results"]

    # Generate outfit descriptions using the OpenAI chat completion endpoint
    outfit_descriptions = []
    for i in range(count):
        response = client.chat.complete(
            model = model,
            messages = [
                {
                    "role": "user",
                    "content": "Give me description of a high fashion outfit that the following person would wear in a fashion show: " + human_description,
                },
            ]
        )
        outfit_description = response.choices[0].message.content
        print("outfit description",i)
        outfit_descriptions.append(outfit_description)
    return outfit_descriptions

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.markdown("<h1 style='text-align: center;'>Fashion Try-on App</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Upload an image of yourself to generate fashionable outfits and create a virtual fashion show!</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        human_image = st.file_uploader("Upload Image of Person #1", type=["jpg", "jpeg", "png"])
        human_image_2 = st.file_uploader("Upload Image of Person #2", type=["jpg", "jpeg", "png"])

        if human_image and human_image_2:
            st.success("Images uploaded successfully!")

            # Open the images
            person_img_1 = Image.open(human_image)
            person_img_2 = Image.open(human_image_2)

            # Create two columns for side-by-side display
            inner_col1, inner_col2 = st.columns(2)

            with inner_col1:
                st.image(person_img_1, caption="Human Image #1")

            with inner_col2:
                st.image(person_img_2, caption="Human Image #2")

             # Save the uploaded image to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                temp_file.write(human_image.getbuffer())  # Use getbuffer() to get the bytes
                temp_file_path = temp_file.name  # Get the path of the temporary file
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file_2:
                temp_file_2.write(human_image_2.getbuffer())  # Use getbuffer() to get the bytes
                temp_file_path_2 = temp_file_2.name  # Get the path of the temporary file

            # Now you can use the saved image path
            human_image_url = temp_file_path
            new_human_url = fal_client.upload_file(human_image_url)
            human_image_url_2 = temp_file_path_2
            new_human_url_2 = fal_client.upload_file(human_image_url_2)
            
        lora = st.text_input("Input Lora #1:", placeholder="fal-flux-lora")
        lora2 = st.text_input("Input Lora #2:", placeholder="fal-flux-lora")

        # which outfit to use in fashion show
        if st.button("Get Outfits"):
            #get all outfit descriptions
            all_outfits = get_outfit_descriptions(1, new_human_url)
            all_outfits_2 = get_outfit_descriptions(1, new_human_url_2)

            # Use async functions to get and try outfits
            # empty string = no lora
            async def generate_outfits(human_url: str, outfits: list, lora: str):
                outfit_images = []
                for i in range(len(outfits)):
                    # Get outfit image using Flux
                    if len(lora) > 0:
                        outfit = await get_outfit_with_lora(outfits[i], lora)
                    else:
                        outfit_image_url = await get_outfit(outfits[i])
                        print("OUTFIT IMAGE URL", human_url, outfit_image_url['images'][0]['url'])
                        # Call the try-on function with the uploaded images
                        outfit = await try_on(human_url, outfit_image_url['images'][0]['url'])

                    # add outfit
                    outfit_images.append(outfit['url'])
                    print("tried on successfully")
                
                # Display the generated outfit images in a grid
                cols = st.columns(len(outfit_images))  
                for i, img_url in enumerate(outfit_images):
                    with cols[i]:  # Use the corresponding column for each image
                        st.image(img_url, caption=f"Outfit #{i + 1}")
                        print("Showing outfits here")
                return outfit_images, outfit_images[0]
                
            
            if lora and lora2:
                outfit, selected_image = asyncio.run(generate_outfits(new_human_url, all_outfits, lora))
                outfit_2, selected_image_2 = asyncio.run(generate_outfits(new_human_url_2, all_outfits_2, lora2))
            else:
                outfit, selected_image = asyncio.run(generate_outfits(new_human_url, all_outfits, False))
                outfit_2, selected_image_2 = asyncio.run(generate_outfits(new_human_url_2, all_outfits_2, False))

            st.success("Try-on process completed. Check the console for the result.")

        
            with col2:
                print(selected_image)
                if st.button("Generate Fashion Show"):
                    # New image/text to video API from Luma
                    async def generate_show(image_url: str):
                        handler = fal_client.submit(
                            "fal-ai/luma-dream-machine",
                            arguments={
                                "prompt": "Full body shot of the person in the photo walking the runway surrounded by a captivated audience",
                                "image_url": image_url,
                                "aspect_ratio": "16:9"
                            },
                        )

                        result = handler.get()
                        print(result)
                        return result["video"]["url"]
                    # use new Luma AI API to generate fashion show given image that is clicked on
                    try:
                        video_url = asyncio.run(generate_show(selected_image))
                        st.write(f"Video URL: {video_url}")

                        response = requests.get(video_url)
                        if response.status_code == 200:
                            video_bytes = response.content
                            st.video(video_bytes)
                        else:
                            st.error("Failed to retrieve video.")
                    except Exception as e:
                        st.error(f"Error generating video: {e}")
                    # video_url_2 = asyncio.run(generate_show(selected_image_2))
                    # response_2 = requests.get(video_url_2)
                    # if response_2.status_code == 200:
                    #     video_bytes = response.content
                    #     st.video(video_bytes)
                    # else:
                    #     st.error("Failed to retrieve video.")
                    st.text("Finished show")