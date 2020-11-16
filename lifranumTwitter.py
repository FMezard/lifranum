from collections import Counter
import twitter
import json
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt
import csv


# TODO : Mettre des variables d'env
# TODO : Virer les # en double
# TODO : Récupérer les auteurs qui twittent avec les # récupérés
# TODO : POur les auteurices : avoir à chaque fois un tuple pour savoir cb de fois ielles apparaissent ?
api = twitter.Api(consumer_key='H0Fh0LpfVI9pGH1LGb91Hv56R',
                  consumer_secret='osXrTW7IWM9ObxCxt1S6Ncae37SmSzvMKNO1QgzeVawxIp4Oqi',
                  access_token_key='3225285533-HbE2ptwZrjubzgohmBsSirl62ZeyiD38iZ7i3fE',
                  access_token_secret='iGvuTp7aNpfSjKzWm9z55G5BLFnKIa5jW4LDPyDy2fWx6',
                  sleep_on_rate_limit=True
                  )


def get_authors_using(hashtag, mots_cles=None):
    # on veut pouvoir faire ou un simple # ou des listes complexes avec # et mots-clés de Christian
    # https://twitter.com/search?q=(%23twitterature%20OR%20%23micropoesie)%20lang%3Afr&src=recent_search_click
    if type(hashtag) == str:
        results = api.GetSearch(term=f"#{hashtag}", lang="fr", count="100")
    else :
        # ?q=Poème (%23twitterature OR %23poesie)
        hashtag = ["%23" + h  for h in hashtag]
        hashtag = (" OR").join(hashtag)
        results = api.GetSearch(term=f"{mots_cles} ({hashtag})", lang="fr", count="100")


    authors = []
    for r in results:
        authors.append(r.user.screen_name)
        print(r.id)
    return set(authors)

def get_author_retweeters(author):
    # TODO : prendre en considération compte pour le graphe
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


def create_csv_authors():
    with open('authors_hashtags.json', 'r', encoding='utf-8') as jsonfile:
        authors_dict = json.load(jsonfile)
    with open('persons_hashtags.csv', 'w', encoding="utf-8") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for hashtag, authors in authors_dict.items():
            print(hashtag)
            for a in authors:
                results = api.GetSearch(raw_query=f"q=from%3A{a}&result_type=recent&since=2014-07-19&count=1")
                if results:
                    filewriter.writerow([hashtag, a, f'"{results[0].user.description}"'])
                else :
                    filewriter.writerow([hashtag, a, "Description non trouvée"])





def get_hashtags_used_with(hashtag_base, all):
    # raw_query=f"q=%23{hashtag} lang%3Afr&count=100"
    results = api.GetSearch(term=f"#{hashtag_base}", lang="fr", count="100")
    hashtags_next_search = []
    base_list = []
    for r in results:
        for hashtag in r.hashtags:
            base_list.append(hashtag.text)
    counter = Counter(base_list)
    for hashtag in counter:
        if counter[hashtag] > 2 and hashtag not in all and hashtag is not hashtag_base:
            hashtags_next_search.append(hashtag.lower())
    return hashtags_next_search



if __name__ == '__main__':
    counter = 0
    with open("all_hashtags.md", "r", encoding="utf-8") as doc_hashtags:
        hashtags = doc_hashtags.readlines()
        authors = dict()
    for hashtag in hashtags:
        hashtag = hashtag.replace("\n", "")
        authors[hashtag] = list(get_authors_using(hashtag))
        counter += len(authors[hashtag])

    # requests = [(["Poésie"], "Tanka"),
    #              (["1mot1haiku"], "haiku"),
    #              (["Poésie"], "haiku"),
    #              (["twitterature", "poesie", "poem"], "Tanka")]
    # authors = dict()
    # for i, request in enumerate(requests):
    #     authors[str(i)] = list(get_authors_using(request[0], requests[1]))
    # print(authors)
    #
    # print(authors)
    with open("authors_hashtags.json", "w", encoding="utf-8") as authors_json:
        json.dump(authors, authors_json, indent=True)

    create_csv_authors()

    # retweeters = []
    # sampoesie =  [
    #
    #   "Faustruy",
    #   "SandraDulier",
    #   "DinaBail",
    #   "didou_52",
    #   "jeannick_odier",
    #   "TweetDePoemes",
    #   "lepolymorphe",
    #   "RidyardColin"]
    # for author in sampoesie:
    #     retweeters.extend(get_author_retweeters(author))
    # create_graph_retweeters(retweeters)


# TODO : Récupérer les tweets de qqun
# TODO : Pr chaque tweet regarder qui le retweet
# TODO : stocker la liste des retweeters avec des tuples nom / nb de fois
