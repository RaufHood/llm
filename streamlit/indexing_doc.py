import requests 
from elasticsearch import Elasticsearch
from tqdm.auto import tqdm

# get documents
docs_url = 'https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/documents.json?raw=1'
docs_response = requests.get(docs_url)
documents_raw = docs_response.json()
documents = []
for course in documents_raw:
    course_name = course['course']

    for doc in course['documents']:
        doc['course'] = course_name
        documents.append(doc)

# index the document
index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "text": {"type": "text"},
            "section": {"type": "text"},
            "question": {"type": "text"},
            "course": {"type": "keyword"}
        }
    }
}
es_client = Elasticsearch('http://localhost:9200')
index_name = "course-questions"
es_client.indices.create(index=index_name, body=index_settings)
for doc in tqdm(documents):
    es_client.index(index=index_name, document =doc)
print("finished indexing")

# define search function
def elastic_search(query):
    search_query = {
        'size': 5,
        'query': {
            'bool': {
                'must': {
                    'multi_match': {
                        'query': query,
                        'fields': ['question^3', 'text', 'section'],
                        'type': 'best_fields'
                    }
                },
                'filter': {
                    'term': {
                        'course': 'data-engineering-zoomcamp'
                    }
                }
            }
        }
    }

    response = es_client.search(index=index_name, body= search_query)
    result_docs = [hit['_source'] for hit in response['hits']['hits']]
    return result_docs
