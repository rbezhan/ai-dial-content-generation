import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('DIAL_API_KEY')

from io import BytesIO
from pathlib import Path

from task._models.custom_content import Attachment, CustomContent
from task._utils.constants import API_KEY, DIAL_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role


async def _put_image() -> Attachment:
    file_name = 'dialx-banner.png'
    image_path = Path(__file__).parent.parent.parent / file_name
    mime_type_png = 'image/png'
    
    async with DialBucketClient(api_key=API_KEY, base_url=DIAL_URL) as bucket_client:
        with open(image_path, 'rb') as image_file:
            image_bytes = image_file.read()
        
        image_content = BytesIO(image_bytes)

        attachment = await bucket_client.put_file(content=image_content, name=file_name, type=mime_type_png)

        return Attachment(
            title=file_name,
            url=attachment.get("url"),
            type=mime_type_png
        )


def start() -> None:
    model_client = DialModelClient(
        api_key=API_KEY,
        endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT,
        deployment_name="anthropic.claude-v3-haiku"
    )

    attachment = asyncio.run(_put_image())
    print(attachment)

    model_client.get_completion(
        [
            Message(
                role=Role.USER,
                content="What is on this image?",
                custom_content=CustomContent(
                    attachment=[attachment]     
                )
            )
        ]
    )

start()
