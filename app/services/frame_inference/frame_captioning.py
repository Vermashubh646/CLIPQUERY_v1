from groq import Groq
import os
# from dotenv import load_dotenv

# load_dotenv('../../../.env')

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def caption_frames(base64_image):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        }
    ],
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    )
    response = chat_completion.choices[0].message.content
    return response