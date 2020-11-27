from collections import Counter
import twitter
import json
import csv
import os
import unidecode
import pprint
import networkx as nx
import matplotlib.pyplot as plt
import scipy

import authors
from hashtags import HashtagsVocabularyGraph

api = twitter.Api(consumer_key=os.getenv('CONSUMER_KEY'),
                  consumer_secret=os.getenv('CONSUMER_SECRET'),
                  access_token_key=os.getenv('ACCESS_TOKEN_KEY'),
                  access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'),
                  tweet_mode='extended',
                  sleep_on_rate_limit=True
                  )


if __name__ == '__main__':
    baselist = ""
    graph_file = ""
    # Pour refaire une visualisation à partir d'un fichier csv du graphe déjà existant, mettre le chemin dans graph_file.
    hashtags = HashtagsVocabularyGraph(baselist, api, graph_file=graph_file)
    print(hashtags.newlist)
    with open("20202611_hashtags_l2.txt", "w", encoding="utf-8") as file:
        for h in hashtags.newlist:
            file.write(h + "\n")
    hashtags.create_hashtags_graph_viz()
