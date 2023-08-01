# pineconeTrial
Demo repository for implementation of a Pinecode vector DB


## Installation

- Run 'pip install -r requirements.txt'
- Create a file called config.yaml
  - Inside write:
  - API:
  -   ENVIRONMENT: 'YOUR PINECONE ENVIRONMENT'
  -   KEY: 'YOUR PINECONE API KEY'
  - (Both of these can be found in your pinecone account settings)


## Creating an Index
- Run python init.py 'Your Index Name' '# Vector Dimensions"

## Running Pinecone Quickstart
- If you would like your index to be deleted after run
  - Uncomment line 96 in quickstart.py
- Run python quickstart.py 'your index name'

## Running Vectorizer Memory
- If you would like your index to be deleted after run
  - Uncomment line 95 in quickstart.py
- Run python vectorizer_demo.py 'your index name'
- Enter in the sentences to commit to memory when prompted
- Enter in a question when prompted
