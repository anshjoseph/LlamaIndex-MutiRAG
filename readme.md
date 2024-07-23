```json
{
  "provider": "LanceDB",
  "provider_config": {
    "embeding": {
      "provider": "OpenAI",
      "model_name": "text-embedding-3-small"
    },
    "chunk_size": 512,
    "overlapping": 200,
    "worker": 2,
    "similarity_top_k":2,
    "rag": {
      "loc": "dev"
    }
  }
}
```

```json
{
  "provider": "MongoDB",
  "provider_config": {
    "embeding": {
      "provider": "OpenAI",
      "model_name": "text-embedding-3-small"
    },
    "chunk_size": 512,
    "overlapping": 200,
    "worker": 2,
    "similarity_top_k":2,
    "rag": {
      "uri": "mongodb+srv://ansh:ansh1234@cluster0.rijb2zb.mongodb.net/",
      "db": "movies",
      "collection_name": "movies_records"
    }
  }
}
```