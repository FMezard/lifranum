import os
import argparse
import urllib.request
import urllib.parse
# import urllib.error
from bs4 import BeautifulSoup
import socket
# from ebooklib import epub, VERSION
import re
# from string import Template

debug = False

chapterCount = 0
# timeout in seconds
timeout = 10
socket.setdefaulttimeout(timeout)


def get_html(url):
    req = urllib.request.Request(url)
    req.add_header('User-agent', 'Mozilla/5.0 (Linux x86_64)')
    # Add DoNotTrack header, do the right thing even if nobody cares
    req.add_header('DNT', '1')
    try:
        request = urllib.request.urlopen(req)
    except socket.timeout:
        if debug:
            raise

    # html.parser generates problems, I could fix them, but switching to lxml
    # is easier and faster
    soup = BeautifulSoup(request.read(), "lxml")
    with open("html_test.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())
    return soup


def get_cover(cover_url):
    print(cover_url)
    tries = 5
    while tries > 0:
        try:
            req = urllib.request.Request(cover_url)
            req.add_header('User-agent', 'Mozilla/5.0 (Linux x86_64)')
            request = urllib.request.urlopen(req)
            temp = request.read()
            with open('cover.jpg', 'wb') as f:
                f.write(temp)
            tries == 0
            # break
            return 1
        except Exception as error:
            tries -= 1
            print("Can't retrieve the cover")
            print(error)
            return 0


def get_book(initial_url):
    base_url = 'http://www.wattpad.com'
    html = get_html(initial_url)

    # Get basic book information
    # author = html.select('div.info strong')[-1].get_text()
    author = html.select('div.author-info strong a')[0].get_text()
    print(author)
    title = html.select('h1')[0].get_text().strip()
    description = html.select('h2.description')[0].get_text()
    coverurl = html.select('div.cover.cover-lg img')[0]['src']
    labels = ['Wattpad']
    for label in html.select('div.tags a'):
        if '/' in label['href']:
            labels.append(label.get_text())
    if debug:
        print("Author: " + author)
        print("Title: " + title)
        print("Description: " + description)
        print("Cover: " + coverurl)
        print("Labels:" + " ".join(labels))

    print("'{}' by {}".format(title, author).encode("utf-8"))
    # print(next_page_url)

    # Get list of chapters
    chapterlist_url = "{}{}".format(initial_url, "/parts")
    chapterlist = get_html(chapterlist_url).select('ul.table-of-contents a')

    # Remove from the file name those characters that Microsoft does NOT allow.
    # This also affects the FAT filesystem used on most phone/tablet sdcards
    # and other devices used to read epub files.
    # Disallowed characters: \/:*?"<>|^
    filename = title
    for i in ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '^']:
        if i in filename:
            filename = filename.replace(i, '')
    # Apple products disallow files starting with dot
    filename = filename.lstrip('.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download stories from wattpad.com and store them as"
                    " epub.",
        epilog="This script doesn't support updating an existing epub with new"
               " chapters",
        argument_default=argparse.SUPPRESS)

    parser.add_argument('initial_url', metavar='initial_url', type=str,
                        nargs=1, help="Book's URL.")
    parser.add_argument('-d', '--debug', action='store_true', default=True,
                        help='print debug messages to stdout')

    args = parser.parse_args()
    if args.debug:
        debug = True
        print(args)

    get_book(args.initial_url[0])