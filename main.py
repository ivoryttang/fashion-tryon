import asyncio
import fal_client

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
    asyncio.run(submit())