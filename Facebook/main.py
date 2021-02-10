from bs4 import BeautifulSoup

filename = "Haïkudujour.html"
with open(filename, "r", encoding="utf-8") as file:
    filecontent = file.read()
soup = BeautifulSoup(filecontent, features="html.parser")
group_title = soup.h1.text
group_articles = soup.find_all("div", attrs={"class": "ce"})
# print(group_articles)

for article in group_articles:
    author = article.h3.a.text
    texte = article.find_all("p")
    print(author)
    print(texte)

