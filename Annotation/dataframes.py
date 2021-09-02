# -*- coding: utf-8 -*-

import pandas as pd
import json
import os
import re

def blogposts_dataframe(blogposts_files, type):
    def json_to_rows(blogposts_files, type):
        for bf in blogposts_files:
            try:
                with open(f"Donnees/{bf}", "r", encoding="utf-8") as file:
                    data = json.load(file)
                if type == "posts":
                    for b in data:
                        content = re.sub(r"border[^ ]* ", "", b["content"])
                        content = re.sub(r"imageanchor[^ ]* ", "", content)
                        yield {"blog_id": b["blog"]["id"],
                               "published": b["published"],
                               "updated": b.get("updated", ""),
                               "url": b["url"],
                               "title": b["title"] if b["title"] else "Sans Titre",
                               "content": content,
                               "labels": " ".join(b.get("labels", "")),
                               "author_id": b["author"].get("id", "Anonyme"),
                               "author_displayName": b["author"]["displayName"]}
                elif type == "blog":
                    yield {"blog_id": data["id"],
                           "description": data["description"],
                           "published": data["published"],
                           "updated": data.get("updated", ""),
                           "url": data["url"],
                           "name": data["name"] if data["name"] else "Sans Titre",
                           "posts_total_items": data["posts"]["totalItems"],
                           "pages_total_items": data["pages"]["totalItems"],
                           "country": data["locale"]["country"],
                           "language": data["locale"]["language"]}
            except FileNotFoundError:
                print(f"Pas de posts pour le blog {bf}")

    rows = list(json_to_rows(blogposts_files, type=type))
    return pd.DataFrame.from_records(rows[:10])




if __name__ == '__main__':
    data = [dirname for dirname in os.listdir("Donnees")]

    # posts = [f"{dirname}/blog_posts_{dirname}.json" for dirname in data]
    infos = [f"{dirname}/blog_info_{dirname}.json" for dirname in data]

    # df_posts = blogposts_dataframe(posts, type="posts")
    df_blogs = blogposts_dataframe(infos, type="blog")
    print(df_blogs.columns)
    # print(df_posts.head())