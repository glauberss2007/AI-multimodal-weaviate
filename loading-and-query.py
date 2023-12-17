import weaviate, os, requests, json, weaviate.classes

#client = weaviate.connect_to_local(
#    headers={
#        "X-OpenAI-Api-Key": os.environ['OPENAI_API_KEY'],
#        "X-Cohere-Api-Key": os.environ['COHERE_API_KEY'],
#    }
#)

client = weaviate.connect_to_embedded(
    headers={
        "X-OpenAI-Api-Key": os.environ['OPENAI_API_KEY'],
        "X-Cohere-Api-Key": os.environ['COHERE_API_KEY'],
    }
)

client.is_ready()
print(client)

# Sample data importing
def load_data(path):
    resp = requests.get(path)
    return json.loads(resp.text)

sample_10 = ""
sample_1k = ""

data_10 = load_data(sample_10)
data_1k = load_data(sample_1k)

if client.collections.exists("Questions"):
    client.collections.delete("Questions")

## Create a collection using cohere as a vectorizer
client.collections.create(
    name = "Questions",
    vectorizer_config = weaviate.classes.Configure.Vectorizer.text2vec_cohere(),
    generative_config = weaviate.classes.Configure.Generative.openai(model="gpt-4")
)

# Import data
questions = client.collections.get("Questions")
questions.data.insert_many(data_10)
#questions.data.insert_many(data_1k)

#response = client.collections.get("Questions")
response = questions.query.fetch_objects(limit=5)
print(response.objects[0].properties)

#item = questions.query.fetch_object_by_id(response[0])

#response = questions.aggregate.over_all()
#print(response)

# Quering data



