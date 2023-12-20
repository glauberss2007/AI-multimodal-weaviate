# AI-multimodal-weaviate
Multi-Modal Search with Weaviate Vector Databases created during DeepLearningAI workshop.

## Loading data, searching and creating a group of tasks

The provided [code]() interacts with Weaviate, an AI-powered knowledge graph that allows storing and querying data based on semantic relationships. It showcases various functionalities, including connecting to Weaviate, importing data, performing searches, leveraging generative models like GPT-4, and conducting complex queries.

## Understand the multimodal

The other [code]() demonstrates the integration of Weaviate, a semantic search engine, with various multimedia types (images, audio, video) and AI models like OpenAI's GPT-4 and DALL-E 3. The script connects to Weaviate, creates a collection, inserts multimedia data, performs searches, and interacts with GPT-4 for content generation and DALL-E 3 for image generation.

### Model for text encoder

A text encoder model is designed to convert text data into numerical representations, often in the form of vectors. These models typically utilize natural language processing (NLP) techniques and are trained on large datasets to understand linguistic patterns, context, and semantics

- **Weaviate Context:** Weaviate may use models like BERT, GPT, or other transformer-based models for text encoding. This is essential for performing semantic search, classifications, and other NLP tasks within the knowledge graph.
- **Application:** When you insert text data (like articles, questions, etc.), the text encoder converts it into vectors which are then stored in Weaviate's vector space for querying.

### Model for image encoder

An image encoder model transforms visual information from images into a numerical form, usually vectors, that represent various features of the image. These models are often based on deep learning, particularly convolutional neural networks (CNNs), which excel in processing pixel data and recognizing visual patterns. 

- **Weaviate Context:** Weaviate can integrate with models such as ResNet, VGG, or other CNN-based models to encode images. This enables image-based queries and cross-modal interactions (like searching text to retrieve relevant images).
- **Application:** Images are encoded into vectors, allowing for similarity searches, classifications, and linking images with other data types in the graph.

### Model for audio encoder

Audio encoder models convert audio signals into a numerical representation. These models deal with the temporal nature of sound and are often based on neural networks that can handle sequential data.

- **Weaviate Context:** Weaviate might use models like wav2vec or similar for audio encoding. This facilitates tasks like audio search, clustering, and analysis within the vector space.
- **Application:** Audio files are transformed into vectors, making it possible to search, classify, or link audio with other modalities in the knowledge graph.

### Model for video encoder

Video encoders process and convert video data into a numerical format. These models must handle both the spatial information present in individual frames (like an image encoder) and the temporal information across frames.

- **Weaviate Context:** Video encoders could be based on models that process both visual and temporal aspects, like 3D CNNs or transformer-based models designed for video.
- **Application:** Videos are broken down into vector representations, allowing for searching across video content and linking it with other data types in Weaviate.

### Unified vector space

A unified vector space refers to a common multidimensional space where different types of data (text, images, audio, video) are represented in a way that allows them to be compared and analyzed together. In such a space, similar concepts, regardless of their original modality, are positioned closely together. This is crucial for multimodal tasks like cross-modal retrieval (e.g., finding images using text queries) or multimodal machine learning models.

- **Weaviate Context:** Weaviate creates a unified vector space enabling cross-modal queries and interactions. This means you can search across different data types and find relationships or similarities between, for instance, text and images or audio and videos.
- **Application:** In a unified vector space, a query in one modality (like a text description) can retrieve relevant results in another modality (like similar images or videos), facilitating complex, multimodal interactions within the knowledge graph.

## Multimodal RAG

Multimodal RAG (Retrieval Augmented Generative) refers to a framework or approach that combines retrieval-based and generative-based models to handle multimodal data within a unified vector space.

- **Weaviate Context:** In Weaviate, Multimodal RAG integrates retrieval-based models (used for retrieving relevant information) and generative models (capable of creating new content) within the same framework. This integration helps in understanding the relationships and context between different data types stored in the knowledge graph.
- **Application:** Weaviate employs Multimodal RAG to perform tasks like content generation based on retrieved information, answering queries across different modalities, and enhancing the understanding of relationships between diverse data types in the unified vector space.

This approach in Weaviate enables sophisticated multimodal interactions within the vector search engine, allowing for a deeper understanding and utilization of diverse data types and their relationships.

PS: in this repository you can found a docker compose file. You can navigate to this directory and run `docker-compose up -d` to run it and `docker ps` to confirm if is it running (http://localhost:8080).

# References
- https://www.youtube.com/@Deeplearningai
- https://weaviate.io/learn/workshops
- https://weaviate.io/blog/multimodal-rag
 
