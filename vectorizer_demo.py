import pinecone
import yaml
import os
import sys
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
import numpy as np
from sent2vec.vectorizer import Vectorizer

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

def vectorize(sentences):
   vectorizer = Vectorizer()
   vectorizer.run(sentences)
   vectors = vectorizer.vectors
   return vectors

if __name__ == '__main__':

    serverName = sys.argv[1]

    def read_yaml(file_path):
        with open(file_path, "r") as f:
            return yaml.safe_load(f)


    apiInfo = read_yaml("config.yaml")

    environment = apiInfo["API"]["ENVIRONMENT"]
    api_key = apiInfo["API"]["KEY"]


    # Create pinecone index and load
    pinecone.init(api_key=api_key, environment=environment)

    if len(pinecone.list_indexes()) == 0:
        os.system("python init.py " + serverName + " 768")

    if serverName not in pinecone.list_indexes():
        for i in pinecone.list_indexes():
            pinecone.delete_index(i)
        os.system("python init.py " + serverName + " 768")
    
    index = pinecone.Index(serverName)

    #Without this line, if index did not exist, http error will throw because of incomplete index intitialization
    wait_on_index(serverName)

    print('How many sentences would you like to enter?')
    numSent = int(input())
    sentences = []
    for i in range(numSent):
       sentences.append(input())
    
    if len(sentences) > 0:
        vectorized_sentences = vectorize(sentences)

        formated_sentences = [(sentences[i], vectorized_sentences[i].tolist()) for i in range(len(vectorized_sentences))]

        index.upsert(formated_sentences)

        for i in vectorized_sentences:
            print(len(i))

    #Print stats after upsert
    print(index.describe_index_stats())

    print('What would you like to ask?')
    question = [input()]

    vectorized_question = vectorize(question)[0].tolist()

    print(index.query(
        vector=vectorized_question,
        top_k=1,
        include_values=True
    ).matches[0].id)

    # # Delete index -> Uncomment if you would like index to be deleted
    # #pinecone.delete_index(serverName)