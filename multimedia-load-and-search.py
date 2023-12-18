import IPython
import weaviate, weaviate.classes, os, json, base64, requests
from IPython.display import Image, Audio, Video

client = weaviate.connect_to_local()

client.is_ready()

print(client.get_meta())

## chech multi2vec-bind model capabilities

# Create the animals collection
if(client.collections.exists("Animals")):
    client.collections.delete("Animals")

client.collections.create(
    name="Animals",

    vectorizer_config=weaviate.classes.Configure.Vectorizer.multi2vec_bind(
        audio_fields=[weaviate.classes.Multi2VecField(name="audio", type="audio")],
        image_fields=[weaviate.classes.Multi2VecField(name="image", type="image")],
        video_fields=[weaviate.classes.Multi2VecField(name="video", type="video")]
    )
)

def toBase64(path):
    with open(path, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')


# Insert images to weviate

source = os.listdir("./data-samples/image/")
objs = list()

for name in source:
    print(f"Adding {name}")
    path = "./data-samples/image/" + name
    objs.append(
        {
            "name": name,
            "path": path,
            "image": toBase64(path),
            "mediaType": "image"
        }
    )

animals = client.collections.get("Animals")
animals.data.insert_many(objs)

animals.aggregate.over_all()

# Insert audio files
source = os.listdir("./data-samples/audio/")
objs = list()

for name in source:
    print(f"Adding {name}")
    path = "./data-samples/audio/" + name
    objs.append(
        {
            "name": name,
            "path": path,
            "audio": toBase64(path),
            "mediaType": "audio"
        }
    )

animals = client.collections.get("Animals")
animals.data.insert_many(objs)
animals.aggregate.over_all()

# Insert video files into weaviate
source = os.listdir("./data-samples/video/")
objs = list()
animals = client.collections.get("Animals")

for name in source:
    print(f"Adding {name}")
    path = "./data-samples/video/" + name
    animals.data.insert(
        {
            "name": name,
            "path": path,
            "video": toBase64(path),
            "mediaType": "video"
        }
    )

print(animals.aggregate.over_all())

# Check all media files added to it
itr = animals.iterator(
    return_properties=["name"]
)

def json_print(data):
    print(json.dumps(data, indent=2))

def display_media(item):
    path = item["path"]

    if(item["mediaType"] == "image"):
        display(Image(path))

    if (item["mediaType"] == "audio"):
        display(Audio(path))

    if (item["mediaType"] == "video"):
        display(Video(path))

def url_to_base64(url):
    image_response = requests.get(url)
    content = image_response.content
    return base64.b64encode(content).decode('utf-8')

def file_to_base64(path):
    with open(path,'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')


# text to media search
animals = client.collections.get("Animals")

response = animals.query.near_text(
    query="dog with stick",
    return_properties=['name', 'path', 'mediaType'],
    limit=3
)

for obj in response.objects:
    json_print(obj.properties)
    display_media(obj.properties)

# image to media search
Image("./data-samples/test/test-cat.jpg")
response = animals.query.near_image(near_image=toBase64("./test/test-cat.jpg"), return_properties=['name','path','mediaType'], limit=3)

for obj in response.objects:
    json_print(obj.properties)
    display_media(obj.properties)

# Audio sto media search
Audio("./data-samples/test/dog_audio.wav")
response = animals.query.near_audio(near_audio=toBase64("./test/dog_audio.wav"), return_properties=['name','path','mediaType'],limit=3)

for obj in response.objects:
    json_print(obj.properties)
    display_media(obj.properties)

# Video to media search
Video("./data-samples/test/test-meerkat.mp4")
response = animals.query.near_video(near_video=toBase64("./data-samples/test/test-meerkat"),return_properties=['name','path','mediaType'],limit=3)

for obj in response.objects:
    json_print(obj.properties)
    display_media(obj.properties)

# Multimodal RAG
# Retrieve IMage -> Pass to LMM (Large Multi Model) -> Get Text/Image Output

# Retrieve content from theVDB with a query
animals = client.collections.get("Animals")

def retrieve_image(query):
    response = animals.query.near_text(
        query=query,
        filters=wvc.Filter(path="mediaType").equal("image"),
        return_properties=['name','path','mediaType','image'],
        limit = 1,
    )
    result = response.objects[0].properties

    print("Retrieved image object:",json.dumps(result, indent=2))

    return result

# response = retrieve_image("animal on a log")
response = retrieve_image("dog with a sign")

SOURCE_IMAGE = response['image']

Image(response['path'])


# Generate a description of the image
openai.api_key = os.environ['OPENAI_API_KEY']

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
                # "url": f"data:image/jpeg;base64,{response.objects[0].properties['image']}" #base64 encoded image from Weaviate
                "url": f"data:image/jpeg;base64,{image64}" #base64 encoded image from Weaviate
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


GENERATED_DESCRIPTION = generate_description_from_image_gpt4(
    prompt="This is an image of my pet, please give me a cute and vivid description.",
    image64=SOURCE_IMAGE
)

# Use the image description to generate a new image with DALL·E 3
def generate_image_dalee3(prompt):
  openai_client = OpenAI()

  response_oai = openai_client.images.generate(
    model="dall-e-3",
    prompt=str(prompt),
    size="1792x1024",
    quality="standard",
    n=1,
  )

  result = response_oai.data[0].url
  print (f"Generated image url: {result}")

  return result

image_url = generate_image_dalee3(GENERATED_DESCRIPTION)
Image(url=image_url)


# Doing ALL together
# Step 1 - retrieve an image – Weaviate
retrieved_image = retrieve_image("animal on a log")
SOURCE_IMAGE = retrieved_image['image']

# Step 2 - generate a description - GPT4
GENERATED_DESCRIPTION = generate_description_from_image_gpt4(
    prompt="This is an image of my pet, please give me a cute and vivid description.",
    image64=SOURCE_IMAGE
)

# Step 3 - use the description to generate a new image – DALE-E 3
GENERATED_IMAGE_URL = generate_image_dalee3(GENERATED_DESCRIPTION)

Image(url=str(GENERATED_IMAGE_URL))

