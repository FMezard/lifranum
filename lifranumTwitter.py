from collections import Counter
import twitter
import json
from datetime import datetime

# TODO : Mettre des variables d'env
# TODO : Virer les # en double
# TODO : Récupérer les auteurs qui twittent avec les # récupérés
# TODO : POur les auteurices : avoir à chaque fois un tuple pour savoir cb de fois ielles apparaissent ?
api = twitter.Api(consumer_key='H0Fh0LpfVI9pGH1LGb91Hv56R',
                  consumer_secret='osXrTW7IWM9ObxCxt1S6Ncae37SmSzvMKNO1QgzeVawxIp4Oqi',
                  access_token_key='3225285533-HbE2ptwZrjubzgohmBsSirl62ZeyiD38iZ7i3fE',
                  access_token_secret='iGvuTp7aNpfSjKzWm9z55G5BLFnKIa5jW4LDPyDy2fWx6')


def get_authors_using(hashtag):
    # https://twitter.com/search?q=(%23twitterature%20OR%20%23micropoesie)%20lang%3Afr&src=recent_search_click
    results = api.GetSearch(term=f"#{hashtag}", lang="fr", count="100")
    authors = []
    for r in results:
        authors.append(r.user.screen_name)
    return set(authors)


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

    print(authors)
    with open("authors.json", "w", encoding="utf-8") as authors_json:
        json.dump(authors, authors_json, indent=True)



# TODO : - Faire un fichier par catégorie
# - Récup le titre comme root (à la main au début)
# - Récup la liste pr faire les recherches
# - Faire les recherhces sur 2 niveaux
# - Créer la mindmap
