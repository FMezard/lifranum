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