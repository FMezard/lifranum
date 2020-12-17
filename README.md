# lifranum

Récupération de littérature numérique sur twitter


Le dossier HASHTAGS_RESULTS contient 
- `hashtag_baselist.txt` : une liste crée avec Lorraine de hashtags où l'on trouve beaucoup de littérature
- `20202611_hashtags_L1.txt` : liste de tous les # utilisés plus de 2 fois avec un # de la baselist dans un tweet
_ `20202611_hashtags_L1_graph.csv`: graphe avec tous les # utilisés ensemble au moins une fois : une arête = une utilisation dans un même tweet
- `20202611_hashtags_L2.txt` et `20202611_hashtags_L1_graph.csv`: même expérience en prenant l1 comme base


Le dossier HASHTAGS_COMMUNITIES_TEST contient des itérations de recherche de coocurrences de hashtags à partir de la liste initiale de Lorraine et des tests de recherches de communautés. Les résultats n'ont pas encore été analysés. 

Le dossier AUTHORS_RESULTS contient 
- `23112020_wattpad_authors.csv` : résultat d'une recherche des auteurs utilisant le #wattpad 
- `23112020_persons_hasthags.csv` : liste de tous les auteurs utilisant les hashtags sélectionnés (`20202611_hashtags_l1_corr`) avec leur bio.  
- `retweet_graph.ipynb` : jupyter notebook pour faire les graphes de retweets à partir d'une liste d'auteurs

TODO : 
- remettre toutes les dates au bon format
- ajouter dans le code la date automatiquement dans les noms de fichier
