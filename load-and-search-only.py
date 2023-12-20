import weaviate
import os
import requests
import json
import weaviate.classes

# Connect to a Weaviate instance
# Use 'connect_to_local' for local connections and 'connect_to_embedded' for embedded connections
# Replace with the appropriate function based on your setup
client = weaviate.connect_to_embedded(
    headers={
        "X-OpenAI-Api-Key": os.environ['OPENAI_API_KEY'],
        "X-Cohere-Api-Key": os.environ['COHERE_API_KEY'],
    }
)

# Check if the client is ready
if client.is_ready():
    print("Connected to Weaviate instance:", client)
else:
    print("Failed to connect to Weaviate instance.")
    exit()

# Function to load data from a URL
def load_data(path):
    response = requests.get(path)
    return json.loads(response.text)

# URLs for the sample data
sample_10_url = "http://example.com/sample_10.json"
sample_1k_url = "http://example.com/sample_1k.json"

# Load the sample data
data_10 = load_data(sample_10_url)
data_1k = load_data(sample_1k_url)

# Check if the "Questions" collection exists and delete if it does
if client.collections.exists("Questions"):
    client.collections.delete("Questions")

# Create a "Questions" collection using Cohere as a vectorizer and GPT-4 for generative tasks
client.collections.create(
    name="Questions",
    vectorizer_config=weaviate.classes.Configure.Vectorizer.text2vec_cohere(),
    generative_config=weaviate.classes.Configure.Generative.openai(model="gpt-4")
)

# Import data into the collection
questions_collection = client.collections.get("Questions")
questions_collection.data.insert_many(data_10)
# Uncomment to insert more data
# questions_collection.data.insert_many(data_1k)

# Fetch and print a sample of the imported data
sample_response = questions_collection.query.fetch_objects(limit=5)
print(sample_response.objects[0].properties)

# Perform a vector search
def vector_search(collection, query, limit=5):
    query_response = collection.query.near_text(query=query, limit=limit)
    for item in query_response:
        print(item.properties)

vector_search(questions_collection, "pigments")

# Perform a search with filters
def search_with_filters(collection, query, filter_value, limit=5):
    query_response = collection.query.near_text(
        query=query,
        limit=limit,
        filters=weaviate.classes.Filter("value").greater_than(filter_value)
    )
    for item in query_response:
        print(item.properties)

search_with_filters(questions_collection, "musical instruments", 500)

# Perform a hybrid search
def hybrid_search(collection, query, alpha, limit=5):
    query_response = collection.query.hybrid(query=query, alpha=alpha, limit=limit)
    for item in query_response:
        print(item.properties)

hybrid_search(questions_collection, "musical instruments", 0.7)

# Group task: Vector search and generate content using GPT-4
def group_task_generate_and_tweet(collection, query, limit=4):
    response = collection.generate.near_text(
        query=query,
        limit=limit,
        single_prompt=f"Write a short tweet about: {query}"
    )
    for item in response:
        print(item.properties)
        print(item.generated)

group_task_generate_and_tweet(questions_collection, "musical instruments")
