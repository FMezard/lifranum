from collections import Counter
import twitter
import json
import csv
import os

# TODO : Mettre des variables d'env
# TODO : Virer les # en double
# TODO : Récupérer les auteurs qui twittent avec les # récupérés
# TODO : POur les auteurices : avoir à chaque fois un tuple pour savoir cb de fois ielles apparaissent ?
api = twitter.Api(consumer_key=os.getenv('CONSUMER_KEY'),
                  consumer_secret=os.getenv('CONSUMER_SECRET'),
                  access_token_key=os.getenv('ACCESS_TOKEN_KEY'),
                  access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'),
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



def create_csv_authors(json, csv):
    """
    Create a csv file (that can be easily read with excel) with a list of authors + hashtag they were discovered with + biography
    :param json: json file
    :param csv: csv file
    :return: None
    """
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
    """
    Get all the hashtags used with a specific one that are not already in a list (avoids repetitions)
    :param hashtag_base: str
    :param all: list
    :return: list
    """
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
    with open("all_hashtags_triee.md", "r", encoding="utf-8") as doc_hashtags:
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
    # print(authors)https://manif.app/?lat=45.19242647710092&long=5.725722312927246&zoom=16&lang=fr
    #
    # print(authors)
    # with open("authors_hashtags.json", "w", encoding="utf-8") as authors_json:
    #     json.dump(authors, authors_json, indent=True)
    #
    # create_csv_authors()

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


