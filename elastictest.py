from elasticsearch import Elasticsearch
from datetime import datetime

es = Elasticsearch(
    cloud_id="b56f3bed4bcf4eb996b4804d3c37d045:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJGMzZWU2MmZmZmRmNTRhNzM4YTNlZThkZjM0NzgwNTkzJDFmNzRhNGI1OGE1YTQ2YTFiMWVhYzc0ODU3Mjg0NTUx",
    api_key='WTJ1WjVZVUJEWVljZTNFVGh1amw6OG5oTGQ2UTJRejJiQWFiWlhIOG51dw=='
)


es.index(index="my-index-000001", id=42, document={"any": "data", "timestamp": datetime.now()})

{'_id': '42', '_index': 'my-index-000001', '_type': 'test-type', '_version': 1, 'ok': True}