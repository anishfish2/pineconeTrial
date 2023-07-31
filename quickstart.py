import pinecone
import yaml
import os
import sys
import subprocess

# Modified from Pinecone Quickstart -> https://docs.pinecone.io/docs/quickstart

# Load API data from config.yaml

if __name__ == '__main__':

    serverName = sys.argv[1]

    print('Server name:', serverName)

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


    print('Current indexes:', pinecone.list_indexes())
    
    index = pinecone.Index(serverName)

    print(index.describe_index_stats())

    # Insert Dummy data
    index.upsert([
        ("A", [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]),
        ("B", [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]),
        ("C", [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]),
        ("D", [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]),
        ("E", [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
    ])

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

    # Delete index

        
    print("Before deletion:", pinecone.list_indexes())

    pinecone.delete_index(serverName)

    print("After deletion:", pinecone.list_indexes())
