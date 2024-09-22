import streamlit as st
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

def generate_show(image_url: str):
    handler = fal_client.submit(
        "fal-ai/luma-dream-machine/image-to-video",
        arguments={
            "prompt": "Full body shot of the person in the photo walking the runway surrounded by a captivated audience",
            "image_url": image_url,
            "aspect_ratio": "16:9"
        },
    )

    result = handler.get()
    print(result)
    return result["video"]["url"]
if __name__ == "__main__":
    if st.button("Generate Fashion Show"):
        # use new Luma AI API to generate fashion show given image that is clicked on
        try:
            video_url = generate_show("https://fal.media/files/panda/WYDZBN_S67yrK0-NmdC02_1d063d608f054279b98234de753b8258.jpg")
            st.write(f"Video URL: {video_url}")

            response = requests.get(video_url)
            if response.status_code == 200:
                video_bytes = response.content
                st.video(video_bytes)
            else:
                st.error("Failed to retrieve video.")
        except Exception as e:
            st.error(f"Error generating video: {e}")