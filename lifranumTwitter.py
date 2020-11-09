from collections import Counter
import twitter
import json
from datetime import datetime

# TODO : Mettre des variables d'env
# TODO : Virer les # en double
# TODO : Récupérer les auteurs qui twittent avec les # récupérés

api = twitter.Api(consumer_key='H0Fh0LpfVI9pGH1LGb91Hv56R',
                  consumer_secret='osXrTW7IWM9ObxCxt1S6Ncae37SmSzvMKNO1QgzeVawxIp4Oqi',
                  access_token_key='3225285533-HbE2ptwZrjubzgohmBsSirl62ZeyiD38iZ7i3fE',
                  access_token_secret='iGvuTp7aNpfSjKzWm9z55G5BLFnKIa5jW4LDPyDy2fWx6')



def get_authors_using(hashtags):
    # https://twitter.com/search?q=(%23twitterature%20OR%20%23micropoesie)%20lang%3Afr&src=recent_search_click
    hashtags_query = "q=("
    for h in list(hashtags):
        hashtags_query += f"%23{h} OR "
    hashtags_query += ") lang%3Afr&count=100"
    hashtags_query = hashtags_query.replace(" OR )", ")")
    results = api.GetSearch(raw_query=hashtags_query)
    print(results)
    for r in results:
        print(r.user.screen_name)


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


def add_branch(children, child_json, coord_base, level, parent_id):
    list_children = []
    for i, child in enumerate(children):
        child_branch = json.loads(child_json)
        child_branch["id"] = str(parent_id) + str(i)
        child_branch["parentId"] = parent_id
        child_branch["text"]["caption"] = child
        child_branch["offset"]["x"] = 200 * level
        child_branch["offset"]["y"] = coord_base
        coord_base = coord_base - 30
        list_children.append(child_branch)
    return (list_children, coord_base)


def create_mindmap(tree, root, count):
    # TODO : changer la date
    with open("root.json", "r", encoding="utf-8") as json_file:
        root_json = json_file.read()

        # Create root
        mindmap = json.loads(root_json)
        mindmap["title"] = "Mindmap" + str(root)
        mindmap["mindmap"]["root"]["text"]["caption"] = root
        mindmap["mindmap"]["root"]["id"] = "1"

        # Create children 1
        with open("child.json", "r", encoding="utf-8") as json_file:
            child_json = json_file.read()
        level1 = tree[root]
        coord_base = (len(level1) // 2) * 30
        # print("coord base base", coord_base)
        parent_id = mindmap["mindmap"]["root"]["id"]
        mindmap["mindmap"]["root"]["children"], coord_base = add_branch(level1, child_json, coord_base, 1,
                                                                        str(parent_id))

        # create children 2
        coord_base2 = (count[0] // 2) * 30
        for i, l1 in enumerate(level1):
            level2 = tree[root][l1]
            parent_id2 = str(1) + str(i)
            mindmap["mindmap"]["root"]["children"][i]["children"], coord_base2 = add_branch(level2, child_json,
                                                                                         coord_base2, 2, parent_id2)
            # print(count)
            coord_base3 = (count[1] // 2) * 30
            # print(coord_base3)
            for j, l2 in enumerate(level2):
                grandgrandchild = tree[root][l1][l2]
                parent_id3 = str(2) + str(j)
                mindmap["mindmap"]["root"]["children"][i]["children"][j]["children"], coord_base3 = add_branch(grandgrandchild, child_json,
                                                                                                coord_base3, 3, parent_id3)

    return mindmap


if __name__ == '__main__':
    names = ["ensemble", "formel", "conjoncturel", "textuel"]
    all_hashtags = list()

    for name in names:
        with open(f"{name}.md", "r", encoding="utf-8") as doc :
            level1 = doc.readlines()
        hashtags_tree = dict()
        hashtags_tree[name] = dict()
        count_l2 = 0
        count_l3 = 0
        # Sert à ne pas remettre un # qu'on a déjà trouvé auparavant avec un autre
        for l1 in level1:
            l1 = l1.replace("\n", "")
            hashtags_tree[name][l1] = dict()
            level2 = set(get_hashtags_used_with(l1, list(all_hashtags)))

            for l2 in level2:
                if input(f"Tapez 1 si vous trouvez ce mot clé pertinent : {l2}   ") == str(1):
                    choice_l2 = []

                    hashtags_tree[name][l1].update({l2 :  get_hashtags_used_with(l2, list(all_hashtags))})
                    for h in hashtags_tree[name][l1][l2] :
                        all_hashtags.append(h.lower())
                    count_l3 += 1
                count_l2 += 1

        print(hashtags_tree)
        mindmap = create_mindmap(hashtags_tree, name, [count_l2, count_l3])
        with open(f"{name}.json", "w", encoding="utf-8") as json_output:
            json.dump(mindmap, json_output)
    all_hashtags = set(all_hashtags)
    with open("all_hashtags.md", "w", encoding="utf-8") as doc:
        for hash in list(all_hashtags):
            print(hash)
            doc.writelines(hash + "\n")

    # get_authors_using(list(all_hashtags)[:1])

# TODO : - Faire un fichier par catégorie
# - Récup le titre comme root (à la main au début)
# - Récup la liste pr faire les recherches
# - Faire les recherhces sur 2 niveaux
# - Créer la mindmap