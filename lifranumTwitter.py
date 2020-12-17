# -*- coding: utf-8 -*-

from collections import Counter
import twitter
import json
import csv
import os
from datetime import datetime
import unidecode
import pprint
import networkx as nx
import matplotlib.pyplot as plt
import scipy
import community as community_louvain

import authors
from hashtags import HashtagsVocabularyGraph

api = twitter.Api(consumer_key=os.getenv('CONSUMER_KEY'),
                  consumer_secret=os.getenv('CONSUMER_SECRET'),
                  access_token_key=os.getenv('ACCESS_TOKEN_KEY'),
                  access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'),
                  tweet_mode='extended',
                  sleep_on_rate_limit=True
                  )
today = datetime.now().strftime("%Y%m%d")
if __name__ == '__main__':
    # baselist = ""
    # graph_file = ""
    # # Pour refaire une visualisation à partir d'un fichier csv du graphe déjà existant, mettre le chemin dans graph_file.
    # hashtags = HashtagsVocabularyGraph(baselist, api, graph_file=graph_file)
    # print(hashtags.newlist)
    # with open("20202611_hashtags_l2.txt", "w", encoding="utf-8") as file:
    #     for h in hashtags.newlist:
    #         file.write(h + "\n")
    # hashtags.create_hashtags_graph_viz()

    # Comparer 2 listes pour vérifier si on peut améliorer le repérage des #
    with open("HASHTAGS_RESULTS/20202611_hashtags_l1_corr.txt", "r") as text:
        h1_corr = text.readlines()
    with open("HASHTAGS_RESULTS/20202611_hashtags_l1.txt", "r") as text:
        h1 = text.readlines()
    difference = [hashtag.strip() for hashtag in h1 if hashtag not in h1_corr]
    print(difference)
# TODO : mettra automatiquement des bons noms de fichiers