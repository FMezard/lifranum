from bs4 import BeautifulSoup
import csv
from os import listdir

files = listdir("urls")
types_urls = {}
new_csv_lines = []

for file in files:
    with open("urls/"+ file, "r", encoding="utf-8") as xml :
        content = xml.read()
    soup = BeautifulSoup(content, "xml")
    categorie = soup.schema["xmlns:tns"]

    if categorie == "http://www.example.org/LIFRANUMidentification":
        categorie = "individuel"
        url = soup.find("element", {"name": "webunit"})["type"]
        if url == "string":
            url_before = soup.find("element", {"name": "webunit"})
            url = url_before.next_sibling.next_sibling["value"]

    elif categorie == "http://www.example.org/community":
        categorie = "communautaire"
        url = soup.find("element", {"name": "webunit"})["type"]
    elif categorie == "http://www.example.org/collectiveauthor":
        categorie = "auteur_collectif"
        url = soup.find("element", {"name": "siteblog"})["type"]
    elif categorie == "http://www.example.org/support":
        categorie = "revue_en_ligne"
        url = soup.find_all("complexType")[1]["name"]
        if url == "edition":
            url = soup.find("element", {"name" : "publicationtype"})["type"]
    else :
        print(f"type non répertorié dans le fichier {file} : {categorie}")
    if "http" not in url :
        print(url, "problème sur ce fichier", file)
    types_urls[url] = categorie

with open("Corrige_URLs_Lifranum_2021_01_19.csv", "r", encoding="utf-8") as csv_file:
    spamreader = csv.reader(csv_file, delimiter=';', quotechar='|')
    for line in spamreader:
        new_line = list(line)
        if line[2] == "methodologie":
            if line[0] in types_urls:
                new_line.append(types_urls[line[0]])
                print(new_line)
        new_csv_lines.append(new_line)

with open("2021_02_09_urls_lifranum.csv", "w", newline='', encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file, delimiter=';', quotechar='|')
    for line in new_csv_lines:
        writer.writerow(line)



