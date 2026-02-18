import base64
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('DIAL_API_KEY')

from task._utils.constants import API_KEY, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.model_client import DialModelClient
from task._models.role import Role
from task.image_to_text.openai.message import ContentedMessage, TxtContent, ImgContent, ImgUrl


def start() -> None:
    project_root = Path(__file__).parent.parent.parent.parent
    image_path = project_root / "dialx-banner.png"

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    dalle_client = DialModelClient(
        api_key=API_KEY,
        endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT,
        deployment_name="gpt-image-1.5-2025-12-16",
    )
    
    dalle_client.get_completion(
        [
            ContentedMessage(
                role=Role.USER,
                content=[
                    TxtContent(text="Describe the image."),
                    ImgContent(
                        image_url=ImgUrl(
                            url=f"data:image/png;base64,{base64_image}"
                        )
                    )
                ]
            )   
        ]
    )


start()