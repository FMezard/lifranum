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

class HashtagsVocabularyGraph():
    # C'est une classe qui permet de faire des interrogation des # et de faire des graphes
    def __init__(self, baselist, api, graph_file=None):
        self.api = api
        self.graph_file = graph_file

        with open(baselist, "r", encoding="utf-8") as text :
            self.hashtags_roots = [root.strip().lower() for root in text.readlines()]

        if self.graph_file :
            self.filename = self.graph_file
        else:
            self.filename = baselist.replace(".txt", "") + "graph.csv"
            self.create_hashtags_edges_list()

        self.graph = nx.read_edgelist(self.filename, delimiter="\t", data=[('Weight', int)])
        nodes = [u for (u,v) in nx.degree(self.graph, weight="Weight") if v > 5]
        self.sub_graph = nx.subgraph(self.graph, nodes)
        self.newlist = self.sub_graph.nodes()


    def get_hashtags_used_with(self, hashtag_base):
        """
        Get all the hashtags used with a specific one
        :param hashtag_base: str
        :return: list of tuples (hashtag, frequency)
        """
        hashtag_base = unidecode.unidecode(hashtag_base)
        # hashtag_base = hashtag_base.lower().strip()
        results = self.api.GetSearch(term=f"#{hashtag_base}", lang="fr", count="100")
        hashtags_used_with = []
        base_list = []
        for r in results:
            for hashtag in r.hashtags:
                base_list.append(unidecode.unidecode(hashtag.text).lower())
        counter = Counter(base_list)
        for hashtag in counter:
            if hashtag != hashtag_base:
                hashtags_used_with.append((hashtag, counter[hashtag]))
        return hashtags_used_with

    def create_hashtags_edges_list(self):
        # filename = baselist.replace(".txt", "") + "graph.csv"

        with open(self.filename, "w", newline='\n') as csv_graph :
            thewriter = csv.writer(csv_graph, delimiter='\t',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for h_base in self.hashtags_roots:
                for hashtag in self.get_hashtags_used_with(h_base):
                    thewriter.writerow([h_base.strip(), hashtag[0], hashtag[1]])

    def create_hashtags_graph_viz(self):
        # if self.graph_file :
        #     filename = self.graph_file
        # else:
        #     filename = self.create_hashtags_edges_list()
        #
        # hashtags_graph = nx.read_edgelist(filename, delimiter="\t", data=[('Weight', int)])

        elarge = [(u, v) for (u, v, d) in self.graph.edges(data=True) if d["Weight"] > 5]
        esmall = [(u, v) for (u, v, d) in self.graph.edges(data=True) if d["Weight"] <= 5]

        rootnodes = [u for (u, v) in self.graph.nodes(data=True) if u in self.hashtags_roots]
        print(rootnodes)

        pos = nx.kamada_kawai_layout(self.graph)
        nx.draw_networkx_nodes(self.graph, pos, node_size=30)

        # edges
        nx.draw_networkx_edges(self.graph, pos, edgelist=elarge, width=1.5, edge_color="b")
        nx.draw_networkx_edges(
            self.graph, pos, edgelist=esmall, width=0.3, alpha=0.5, edge_color="b"
        )
        nx.draw_networkx_nodes(
            self.graph, pos, nodelist=rootnodes, node_color="r"
        )

        nx.draw_networkx_labels(self.graph, pos, font_size=7, font_family="sans-serif")
        plt.show()
        plt.savefig("graph.png")



