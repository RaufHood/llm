# create streamlit RAG application

- Run elastic search  
``docker run -it --rm --name elasticsearch -m 4GB -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.4.3``

- Run 
``python indexing_doc.py``

- Run app  
``streamlit run streamlit/qa_faq.py``

- curl http://localhost:9200