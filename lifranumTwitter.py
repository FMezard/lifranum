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


from hashtags import HashtagsVocabularyGraph

# TODO : Mettre des variables d'env
# TODO : Virer les # en double
# TODO : Récupérer les auteurs qui twittent avec les # récupérés
# TODO : POur les auteurices : avoir à chaque fois un tuple pour savoir cb de fois ielles apparaissent ?
api = twitter.Api(consumer_key=os.getenv('CONSUMER_KEY'),
                  consumer_secret=os.getenv('CONSUMER_SECRET'),
                  access_token_key=os.getenv('ACCESS_TOKEN_KEY'),
                  access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'),
                  tweet_mode='extended',
                  sleep_on_rate_limit=True
                  )


def get_authors_using(hashtag, research_words=None):
    """
    TODO : keeping the number of times an author appears in a research
    Returns a set of authors twitter's id using specific hashtag(s) (and potentially other words)
    :param hashtag: list or string
    :param research_words: string
    :return: set
    """
    if type(hashtag) == str:
        results = api.GetSearch(term=f"#{hashtag}", lang="fr", count="100")
    else :
        hashtag = ["%23" + h  for h in hashtag]
        hashtag = (" OR").join(hashtag)
        results = api.GetSearch(term=f"{research_words} ({hashtag})", lang="fr", count="100")
    authors = []
    for r in results:
        authors.append(r.user.screen_name)

        print(r.id)
    return set(authors)

def get_author_retweeters(author):
    """
    Returns the list of ids of users who retweeted the tweets of a specific author
    :param author: str (username of author)
    :return: list (ids of authors)
    """
    retweeters_final = []
    results = api.GetSearch(raw_query=f"q=from%3A{author}&result_type=recent&since=2014-07-19&count=100")
    for r in results:
        if r.retweeted_status :
            retweeters = api.GetRetweeters(r.retweeted_status.id)
        else :
            retweeters = None
        if retweeters:
            for ret in retweeters :
                retweeters_final.append((author, ret))
    return retweeters_final




def create_csv_authors(authors_dict, csv_name):
    """
    Create a csv file (that can be easily read with excel) with a list of authors + hashtag they were discovered with + biography
    :param authors_dict: dict of authors per hashtags
    :param csv: csv file
    :return: None
    """

    with open(csv_name, 'w', encoding="utf-8") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for hashtag, authors in authors_dict.items():
            print(hashtag)
            for a in authors:
                results = api.GetSearch(raw_query=f"q=from%3A{a}&result_type=recent&since=2014-07-19&count=1")
                if results:
                    filewriter.writerow([hashtag, a, results[0].user.description, results[0].user.url])
                else :
                    filewriter.writerow([hashtag, a, "Description non trouvée"])





def create_hashtags_edges_list(root_list):
    # TODO : ajouter un niveau de recherche de hashtags
    with open(root_list, "r", encoding="utf-8") as text :
        hashtags_base = text.readlines().strip()
    with open("graph_hashtags.csv", "w", newline='\n') as csv_graph :
        thewriter = csv.writer(csv_graph, delimiter='\t',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for h_base in hashtags_base:
            for hashtag in get_hashtags_used_with(h_base, []):
                thewriter.writerow([h_base.strip(), hashtag[0], hashtag[1]])

def create_hashtags_graph_viz(graph):
    hashtags_graph = nx.read_edgelist(graph, delimiter="\t", data=[('Weight', int)])
    print(len(nx.nodes(hashtags_graph)))
    nodes = [u for (u,v) in nx.degree(hashtags_graph, weight="Weight") if v > 2]
    hashtags_graph = nx.subgraph(hashtags_graph, nodes)
    print(len(nx.nodes(hashtags_graph)))
    elarge = [(u, v) for (u, v, d) in hashtags_graph.edges(data=True) if d["Weight"] > 5]
    esmall = [(u, v) for (u, v, d) in hashtags_graph.edges(data=True) if d["Weight"] <= 5]
    pos = nx.kamada_kawai_layout(hashtags_graph)  # positions for all nodes
    # k=0.4,,  weight="Weight"
    # nodes
    nx.draw_networkx_nodes(hashtags_graph, pos, node_size=30)

    # edges
    nx.draw_networkx_edges(hashtags_graph, pos, edgelist=elarge, width=1.5, edge_color="b")
    nx.draw_networkx_edges(
        hashtags_graph, pos, edgelist=esmall, width=0.3, alpha=0.5, edge_color="b"
    )

    nx.draw_networkx_labels(hashtags_graph, pos, font_size=7, font_family="sans-serif")
    plt.show()


    plt.savefig("graph.png")





def get_author_retweeters(author):
    # TODO : prendre en considération compte pour le graphe
    retweeters_final = []
    results = api.GetSearch(term=f"@{author}", lang="fr", count="100")
    for r in results:
        if r.retweeted_status :
            retweeters = api.GetRetweeters(r.retweeted_status.id)
        else :
            retweeters = None
        if retweeters:
            for ret in retweeters :
                retweeters_final.append((author, ret))
    # compte = Counter(retweeters)
    # print(compte)
    return retweeters_final

def create_graph_retweeters(retweeters):
    #author : string
    # retweeters : list
    # Il faudra faire des tuple auteur / retweeter
    # Et une longue liste de tous les noeuds
    options = {
    'node_color': 'green',
    'node_size': 50,
    'width': 1,
    'with_labels' : True
}
    G = nx.Graph()
    # G.add_node(author)
    # G.add_nodes_from(retweeters)
    for a, r in retweeters:
        G.add_edge(a, r)
    print("le graph", G.number_of_edges())
    nx.draw_circular(G, **options)
    plt.savefig("graph.png")


if __name__ == '__main__':
    counter = 0
    # getting all authors using our list of #
    # with open("all_hashtags_triee.txt", "r", encoding="utf-8") as doc_hashtags:
    #     hashtags = doc_hashtags.readlines()
    #     authors = dict()
    # for hashtag in hashtags:
    #     hashtag = hashtag.replace("\n", "")
    #     authors[hashtag] = list(get_authors_using(hashtag))
    #     counter += len(authors[hashtag])
    #
    #
    # with open("authors_hashtags.json", "w", encoding="utf-8") as authors_json:
    #     json.dump(authors, authors_json, indent=True)
    #
    # # Saving the dict of authors per hashtags to a csv file and adding the bio of the author
    # create_csv_authors(authors, "authors_hashtags.csv")
    # authors = dict()
    # authors["wattpad"] = get_authors_using("wattpad")
    # create_csv_authors(authors, '23112020_wattpad_authors.csv')

    # print(create_hashtags_graph_viz("graph_hashtags.csv"

    # Si on veut avoir un nouveau graph en interrogeant twitter à nouveau, mettre graph=None ou ne pas mettre graph
    hashtags = HashtagsVocabularyGraph("20201611_hashtags_l1_corr.txt", api, graph_file="20201611_hashtags_l1_corrgraph.csv")
    print(hashtags.newlist)
    with open("20202611_hashtags_l2.txt", "w", encoding="utf-8") as file:
        for h in hashtags.newlist:
            file.write(h + "\n")
    hashtags.create_hashtags_graph_viz()
    # hashtags.create_hashtags_graph_viz()
# TODO : refaire la liste des # avec du code qui ressemble à qque chose ! et un graphe !
# TODO : écrire du code pour récupérer des auteurs et les stocker dans un très gros CSV
# TODO : Réfléchir à comment repérer qui retweete qui