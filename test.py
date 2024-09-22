import streamlit as st
import asyncio
import fal_client
import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv
import tempfile
import requests
from mistralai import Mistral
from playwright.sync_api import sync_playwright, Playwright

load_dotenv()

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"
client = Mistral(api_key=api_key)

async def generate_show(image_url: str):
    handler = fal_client.submit(
        "fal-ai/luma-dream-machine",
        arguments={
                "prompt": "The person in the photo walking the runway surrounded by a captivated audience",
                "image_url": image_url,
                "aspect_ratio": "16:9"
        },
    )

    result = handler.get()
    print(result)
    return result["video"]["url"]
if __name__ == "__main__":
    if st.button("Generate Fashion Show"):
        print("Show is generating")
        # use new Luma AI API to generate fashion show given image that is clicked on
        # Run asynchronous functions
        # video_url = asyncio.run(generate_show("https://fal.media/files/penguin/f_x4DK_8RZ1jfgLOh8UAs_df0414b0e2b84e00bf3e3ccc409f16bb.jpg"))

        # video_file = open("https://v2.fal.media/files/2f15f955772343c3a7aae525cebb4237_output.mp4", "rb")
        # video_bytes = video_file.read()

        # Display videos
        # st.video(video_bytes)

        response = requests.get("https://v2.fal.media/files/2f15f955772343c3a7aae525cebb4237_output.mp4")
        if response.status_code == 200:
            video_bytes = response.content
            st.video(video_bytes)
        else:
            st.error("Failed to retrieve video.")

        st.text("Finished show")