import base64
import json
import os
import requests
import weaviate
from IPython.core.display_functions import display
from IPython.display import Image, Audio, Video
import openai
from openai import OpenAI

# Weaviate connection and collection creation
def connect_to_weaviate():
    client = weaviate.connect_to_local()
    if client.is_ready():
        print("Weaviate is ready.")
    else:
        print("Failed to connect to Weaviate.")
    print(client.get_meta())
    return client


def create_animals_collection(client):
    if client.collections.exists("Animals"):
        client.collections.delete("Animals")

    client.collections.create(
        name="Animals",
        vectorizer_config=weaviate.classes.Configure.Vectorizer.multi2vec_bind(
            audio_fields=[weaviate.classes.Multi2VecField(name="audio", type="audio")],
            image_fields=[weaviate.classes.Multi2VecField(name="image", type="image")],
            video_fields=[weaviate.classes.Multi2VecField(name="video", type="video")]
        )
    )


# Utility functions
def to_base64(path):
    with open(path, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')


def insert_media_into_collection(client, media_type, directory):
    source = os.listdir(directory)
    objs = []

    for name in source:
        print(f"Adding {name}")
        path = os.path.join(directory, name)
        objs.append({
            "name": name,
            "path": path,
            media_type: to_base64(path),
            "mediaType": media_type
        })

    animals = client.collections.get("Animals")
    animals.data.insert_many(objs)
    animals.aggregate.over_all()


def display_media(item):
    path = item["path"]

    if item["mediaType"] == "image":
        display(Image(path))
    elif item["mediaType"] == "audio":
        display(Audio(path))
    elif item["mediaType"] == "video":
        display(Video(path))


def json_print(data):
    print(json.dumps(data, indent=2))


# Usage of functions
client = connect_to_weaviate()
create_animals_collection(client)

insert_media_into_collection(client, "image", "./data-samples/image/")
insert_media_into_collection(client, "audio", "./data-samples/audio/")
insert_media_into_collection(client, "video", "./data-samples/video/")

# Media search function for different types
def search_media_by_text(client, query, media_type, return_properties=['name', 'path', 'mediaType'], limit=3):
    animals = client.collections.get("Animals")
    response = animals.query.near_text(
        query=query,
        return_properties=return_properties,
        limit=limit
    )

    for obj in response.objects:
        json_print(obj.properties)
        display_media(obj.properties)

def search_media_by_image(client, image_path, return_properties=['name', 'path', 'mediaType'], limit=3):
    animals = client.collections.get("Animals")
    response = animals.query.near_image(
        near_image=to_base64(image_path),
        return_properties=return_properties,
        limit=limit
    )

    for obj in response.objects:
        json_print(obj.properties)
        display_media(obj.properties)

def search_media_by_audio(client, audio_path, return_properties=['name', 'path', 'mediaType'], limit=3):
    animals = client.collections.get("Animals")
    response = animals.query.near_audio(
        near_audio=to_base64(audio_path),
        return_properties=return_properties,
        limit=limit
    )

    for obj in response.objects:
        json_print(obj.properties)
        display_media(obj.properties)

def search_media_by_video(client, video_path, return_properties=['name', 'path', 'mediaType'], limit=3):
    animals = client.collections.get("Animals")
    response = animals.query.near_video(
        near_video=to_base64(video_path),
        return_properties=return_properties,
        limit=limit
    )

    for obj in response.objects:
        json_print(obj.properties)
        display_media(obj.properties)

# Multimodal RAG functions
def retrieve_image_from_query(client, query):
    animals = client.collections.get("Animals")
    response = animals.query.near_text(
        query=query,
        filters=weaviate.Classes.Filter(path="mediaType").equal("image"),
        return_properties=['name', 'path', 'mediaType', 'image'],
        limit=1,
    )
    result = response.objects[0].properties

    print("Retrieved image object:", json.dumps(result, indent=2))

    return result

# GPT-4 interaction
def generate_description_from_image_gpt4(prompt, image64):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response_oai = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    result = response_oai.json()['choices'][0]['message']['content']
    print(f"Generated description: {result}")

    return result

# DALL-E 3 usage
def generate_image_dalle3(prompt):
    openai_client = OpenAI()

    response_oai = openai_client.images.generate(
        model="dall-e-3",
        prompt=str(prompt),
        size="1792x1024",
        quality="standard",
        n=1,
    )

    result = response_oai.data[0].url
    print(f"Generated image url: {result}")

    return result

# Utilizing the functions
# Example usage of media search functions
search_media_by_text(client, "dog with stick", "image")
search_media_by_image(client, "./data-samples/test/test-cat.jpg")
search_media_by_audio(client, "./data-samples/test/dog_audio.wav")
search_media_by_video(client, "./data-samples/test/test-meerkat.mp4")

# Example usage of multimodal RAG and GPT-4 functions
retrieved_image = retrieve_image_from_query(client, "dog with a sign")
SOURCE_IMAGE = retrieved_image['image']

GENERATED_DESCRIPTION = generate_description_from_image_gpt4(
    prompt="This is an image of my pet, please give me a cute and vivid description.",
    image64=SOURCE_IMAGE
)

# Example usage of DALL-E 3 function
image_url = generate_image_dalle3(GENERATED_DESCRIPTION)
Image(url=image_url)
