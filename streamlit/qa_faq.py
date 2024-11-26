# setup:
# 1. streamlit for front end
# 2. ollama as LLM
# 3. Langchain embeddings
# 4. ElasticSearch for RAG search

import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from tqdm.auto import tqdm
import requests

# Load env var
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# define client connection
client = OpenAI(api_key=openai_api_key)

# define es client
es_client = Elasticsearch('http://localhost:9200')
print(es_client.info())

# define elast search
def elastic_search(query, index_name = "course-questions"):
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

# create a prompt from template
def build_prompt(query, search_results):
    prompt_template = """
You're a course teaching assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT: 
{context}
""".strip()

    context = ""
    
    for doc in search_results:
        context = context + f"section: {doc['section']}\nquestion: {doc['question']}\nanswer: {doc['text']}\n\n"
    
    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt

# define llm call
def llm(prompt):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

# one functon call for rag
def rag(query):
    search_results = elastic_search(query)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt)
    return answer

def main():
    st.title("RAG Function Invocation")

    # input box
    user_input = st.text_input("Enter your input:")

    # button to invoke RAG function
    if st.button("Ask"):
        with st.spinner('Processing..'):
            output = rag(user_input)
            st.success("Completed!")
            st.write(output)

#query = 'The course has already started, can I still join it?'

if __name__ == "__main__":
    main()
