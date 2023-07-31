# pineconeTrial
Demo repository for implementation of a Pinecode vector DB


## To Run

- Run 'pip install -r requirements.txt'
- Create a file called config.yaml
  - Inside write:
  - API:
  -   ENVIRONMENT: 'YOUR PINECONE ENVIRONMENT'
  -   KEY: 'YOUR PINECONE API KEY'
  - (Both of these can be found in your pinecone account settings)
- If you would like your index to be deleted after run
  - Uncomment line 96 in quickstart.py
- Run python quickstart.py 'your index name'
