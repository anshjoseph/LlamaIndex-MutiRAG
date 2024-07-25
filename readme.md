# Multi RAG Server

This server is designed to connect to multiple Retrieval-Augmented Generation (RAG) systems using different embedding models for the ingestion pipeline.
Setup and Run

To set up and run the server, follow these steps:

- #### Install the required dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- #### Start the server:
  ```bash
      python main.py
  ```
## Configuring Payloads for Different RAG Systems
You can connect multiple RAG systems and use different embedding models for each. Below are examples of configurations for LanceDB and MongoDB.

#### LanceDB Configuration

```json
{
  "provider": "LanceDB",
  "provider_config": {
    "embedding": {
      "provider": "OpenAI",
      "model_name": "text-embedding-3-small"
    },
    "chunk_size": 512,
    "overlapping": 200,
    "worker": 2,
    "similarity_top_k": 2,
    "rag": {
      "loc": "dev"
    }
  }
}
```
#### MongoDB Configuration
```json

  {
    "provider": "MongoDB",
    "provider_config": {
      "embedding": {
        "provider": "OpenAI",
        "model_name": "text-embedding-3-small"
      },
      "chunk_size": 512,
      "overlapping": 200,
      "worker": 2,
      "similarity_top_k": 2,
      "rag": {
        "uri": "mongodb+srv://username:password@cluster0.mongodb.net/",
        "db": "movies",
        "collection_name": "movies_records"
      }
    }
  }
```
## Working

![](./imgs/flow.jpg)