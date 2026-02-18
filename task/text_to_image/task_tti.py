import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('DIAL_API_KEY')


from task._models.custom_content import Attachment
from task._utils.constants import API_KEY, DIAL_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role

class Size:
    """
    The size of the generated image.
    """
    square: str = '1024x1024'
    height_rectangle: str = '1024x1792'
    width_rectangle: str = '1792x1024'


class Style:
    """
    The style of the generated image. Must be one of vivid or natural.
     - Vivid causes the model to lean towards generating hyper-real and dramatic images.
     - Natural causes the model to produce more natural, less hyper-real looking images.
    """
    natural: str = "natural"
    vivid: str = "vivid"


class Quality:
    """
    The quality of the image that will be generated.
     - ‘hd’ creates images with finer details and greater consistency across the image.
    """
    standard: str = "standard"
    hd: str = "hd"

async def _save_images(attachments: list[Attachment]):
    async with DialBucketClient(api_key=API_KEY, base_url=DIAL_URL) as bucket_client:
        for attachment in attachments:
            if attachment.type and attachment.type == 'image/png':
                image_content = await bucket_client.get_file(attachment.url)
                filename = f"{datetime.now().strftime("%Y%m%d_%H%M%S")}.png"

                with open(filename, 'wb') as image_file:
                    image_file.write(image_content)
                
                print(f"Image saved as {filename}")


def start() -> None:
    dalle_client = DialModelClient(
        api_key=API_KEY,
        endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT,
        deployment_name='dall-e-3',
    )

    user_input = "Generate an image of a futuristic city skyline at sunset in a vivid style and hd quality."

    ai_message = dalle_client.get_completion(
        messages=[
            Message(
                role=Role.USER,
                content=user_input)],
        custom_fields={
            "size": Size.square,
            "style": Style.vivid,
            "quality": Quality.hd
        }
    )

    if custom_content := ai_message.custom_content:
        if attachments := custom_content.attachments:    
            asyncio.run(_save_images(attachments))

start()
