import pinecone
import sys
import time
import yaml



if __name__ == '__main__':
    
    serverName = sys.argv[1]

    print('Creating index', serverName)

    def read_yaml(file_path):
        with open(file_path, "r") as f:
            return yaml.safe_load(f)


    apiInfo = read_yaml("config.yaml")

    environment = apiInfo["API"]["ENVIRONMENT"]
    api_key = apiInfo["API"]["KEY"]


    # Create pinecone index and load
    pinecone.init(api_key=api_key, environment=environment)

    print('Before creation:', pinecone.list_indexes())

    pinecone.create_index(serverName, dimension=8, metric="euclidean")

    time.sleep(60)

    print('After creation:', pinecone.list_indexes())
