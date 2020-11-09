with open("all_hashtags_15102020.md", "r", encoding="utf-8") as doc:
    hashtags = doc.readlines()
    hashtags = set(hashtags)

with open("all_hashtags_15102020.md", "w", encoding="utf-8") as doc:
    for h in hashtags:
        doc.writelines(h)
