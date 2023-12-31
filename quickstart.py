import pinecone
import yaml
import os
import sys
import time

# Modified from Pinecone Quickstart -> https://docs.pinecone.io/docs/quickstart
# Load API data from config.yaml

#Function to ensure index has been fully initalized
def wait_on_index(serverName):
  ready = False

  while not ready:
    try:
      desc = pinecone.describe_index(serverName)
      if desc[7]['ready']:
        return True
      
    except pinecone.core.client.exceptions.NotFoundException:
      pass

if __name__ == '__main__':

    serverName = sys.argv[1]

    print(serverName)

    def read_yaml(file_path):
        with open(file_path, "r") as f:
            return yaml.safe_load(f)


    apiInfo = read_yaml("config.yaml")

    environment = apiInfo["API"]["ENVIRONMENT"]
    api_key = apiInfo["API"]["KEY"]


    # Create pinecone index and load
    pinecone.init(api_key=api_key, environment=environment)

    if len(pinecone.list_indexes()) == 0:
        os.system("python init.py " + serverName)

    if serverName not in pinecone.list_indexes():
        for i in pinecone.list_indexes():
            pinecone.delete_index(i)
        os.system("python init.py " + serverName)
    
    index = pinecone.Index(serverName)

    print(pinecone.list_indexes())

    #Without this line, if index did not exist, http error will throw because of incomplete index intitialization
    wait_on_index(serverName)

    print(pinecone.list_indexes())

    #Print stats before upsert
    print(index.describe_index_stats())

    # Insert Dummy data
    index.upsert([
        ("A", [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]),
        ("B", [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]),
        ("C", [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]),
        ("D", [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]),
        ("E", [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
    ])

    #Print stats after upsert
    print(index.describe_index_stats())
    # # Returns:
    # # {'dimension': 8, 'index_fullness': 0.0, 'namespaces': {'': {'vector_count': 5}}}
    # # Query open index for top (3) vectors most similar to example : '[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]'

    print(index.query(
        vector=[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
        top_k=3,
        include_values=True
    ))
    # Returns:
    # {'matches': [{'id': 'C',
    #               'score': 0.0,
    #               'values': [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]},
    #              {'id': 'D',
    #               'score': 0.0799999237,
    #               'values': [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]},
    #              {'id': 'B',
    #               'score': 0.0800000429,
    #               'values': [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]}],
    #  'namespace': ''}

    # Delete index -> Uncomment if you would like index to be deleted
    #pinecone.delete_index(serverName)