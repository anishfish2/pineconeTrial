import pinecone
import sys
import time
import yaml

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
    
    print('Running init.py')
    
    serverName = sys.argv[1]

    def read_yaml(file_path):
        with open(file_path, "r") as f:
            return yaml.safe_load(f)


    apiInfo = read_yaml("config.yaml")

    environment = apiInfo["API"]["ENVIRONMENT"]
    api_key = apiInfo["API"]["KEY"]


    # Create pinecone index and load
    pinecone.init(api_key=api_key, environment=environment)

    pinecone.create_index(serverName, dimension=8, metric="euclidean")

    print("During init.py:", pinecone.list_indexes())
    wait_on_index(serverName)
    time.sleep(30)