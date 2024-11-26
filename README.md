# llm
This repository contains my notes and educational notebooks on LLMs as part of hands on course.  

How to choose which model to use and where to run it:
- access LLMs via API
for fast prototyping chatgpt api call runs, data will be sent to openai, but very short inference time. and no special setup required.
good performance

- Open Source LLMs
    - full control, access via huggingfacehub
    - performance might be bad
    - require a GPU

- Saturcloud, Amazong Sagemeaker, google colab, github codespaces
    - saturncloud.io
    - choose gpu: 74-XLarge - 4 cores - 16Gi RAM - 1 GPU
    - environment -> image -> saturncloud/saturn-python-llm  2023.09.01 
    - extra packages -> pip ->
    ``pip install -U transofrmers accelerate bitsandbytes``
    - add git repo
    - add token from huggingface
    it takes 10 min or so

flan t5