import asyncio
import fal_client
import streamlit as st
from PIL import Image

# FAL Try-on API: https://fal.ai/models/fal-ai/cat-vton/api?platform=python
async def submit():
    handler = await fal_client.submit_async(
        "fal-ai/cat-vton",
        arguments={
            "human_image_url": "https://me99.in/wp-content/uploads/2023/03/Cotton-Full-Sleeve-Men-Shirt-For-Summer-1.jpg",
            "garment_image_url": "https://assets.myntassets.com/h_720,q_90,w_540/v1/assets/images/28971488/2024/7/12/d6f2ce64-e7a7-4916-886d-9c3de51ad67c1720763522797-Eteenz-Girls-Tops-2961720763522438-1.jpg",
            "cloth_type": "upper"
        },
    )

    log_index = 0
    async for event in handler.iter_events(with_logs=True):
        if isinstance(event, fal_client.InProgress):
            new_logs = event.logs[log_index:]
            for log in new_logs:
                print(log["message"])
            log_index = len(event.logs)

    result = await handler.get()
    print(result)


if __name__ == "__main__":
    # asyncio.run(submit())
    st.set_page_config(layout="wide")
    st.markdown("<h1 style='text-align: center;'>Fashion Try-on App</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Upload an image of yourself to generate fashionable outfits and create a virtual fashion show!</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        human_image = st.file_uploader("Upload Image of Yourself", type=["jpg", "jpeg", "png"])

        if human_image:
            st.success("Images uploaded successfully!")

            # Display the uploaded images
            st.image(Image.open(human_image), caption="Human Image")

        
            if st.button("Get Outfits"):
                # Assuming the images are uploaded and can be accessed directly
                human_image_url = "https://path/to/human/image.jpg"
                garment_image_url = "https://path/to/garment/image.jpg"

                # Call the submit function with the uploaded images
                asyncio.run(submit(human_image_url, garment_image_url))

                st.success("Try-on process completed. Check the console for the result.")

    with col2:
        if st.button("Generate Fashion Show"):
            st.success("Show is generating")