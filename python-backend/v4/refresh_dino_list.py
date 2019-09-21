import datetime
import argparse

# Web libraries
import json
import requests
from bs4 import BeautifulSoup

log_file = open("../../logs/refresh.txt", "w+")

def main():

    parser = argparse.ArgumentParser(
        description="Create list of dinosaurs found on wikipedia as well as dinosaurpictures.org"
    )
    parser.add_argument(
        "-d", "--dev",
        action="store_true",
        help="Development mode for printing"
    )
    args = parser.parse_args()

    if args.dev:
        print("Dev mode active")
        dev = True
    else:
        dev = False

    log_file.write('\nRefreshing valid dinosaur list on {}...\n'.format(datetime.datetime.now()))
    log_file.flush()

    log_file.write('Accessing wikipedia list...\n')
    log_file.flush()
    wiki_dinos = scrape_wiki(site='wiki', dev=dev)
    log_file.write('Success!\n')
    log_file.flush()

    log_file.write('Checking dinosaurpictures.org for matches...\n')
    log_file.flush()
    valid_dinos = filter_wiki_list(wiki_dinos, dev=dev)
    log_file.write('Success!\n')
    log_file.flush()

    log_file.write('Writing valid dinosaurs list...\n')
    log_file.flush()
    list_size = write_dino_list(valid_dinos, dev=dev)
    log_file.write("Success! Dino list now contains {} dinosaurs\n".format(list_size))
    log_file.flush()

    log_file.close()

def write_dino_list(dino_list, dev=False):

    dino_list_path = "valid_dinos.csv"

    pictures_root = "http://dinosaurpictures.org/api/dinosaur/"

    list_size = 0
    with open(dino_list_path, "w") as list_file:
        header = "dinos, pic_urls, wiki_article\n"
        list_file.write(header)
        for name in dino_list:

            name_string = name+", "
            list_file.write(name_string)

            urls = []
            dino_request = requests.get(pictures_root+name)

            for pics in dino_request.json()["pics"]:
                voting_url = pics["votingUrl"]
                url_string = "{} ".format(voting_url)
                list_file.write(url_string)
            list_file.write(", ")

            article_paragraphs = scrape_article(name)
            article = "...".join(article_paragraphs)
            article = article.replace("\"", "\"\"")
            article = article.replace("\n", "...")
            article = "\"" + article + "\""
            article = article

            list_file.write(article)

            list_file.write("\n")

            list_size += 1

    if dev:
        print("\n{} now contains {} dinosaurs".format(dino_list_path, list_size))

    return list_size

def scrape_article(dino_string):

    base_url = 'https://en.wikipedia.org/wiki/'
    article_url = base_url + dino_string

    article_result = requests.get(article_url)
    article_content = article_result.content
    article_soup = BeautifulSoup(article_content, 'html.parser')

    article_paragraphs = [p_elem.get_text() for p_elem in article_soup.find_all('p')]
    article_paragraphs = [para for para in article_paragraphs if len(para) > 15]

    return article_paragraphs

def filter_wiki_list(wiki_dinos, dev=False):

    valid_dinos = []
    pictures_root = "http://dinosaurpictures.org/api/dinosaur/"

    for wiki_dino in wiki_dinos:
        pictures_request = requests.get(pictures_root+wiki_dino)
        if pictures_request.status_code == 200:
            if dev:
                print("{} found on both sites, adding to list...".format(wiki_dino))
            result = pictures_request.json()
            valid_dino = result["name"]
            valid_dinos.append(valid_dino)

    return valid_dinos

def scrape_wiki(site, dev=False):

    wiki_list_url = 'https://en.wikipedia.org/wiki/List_of_dinosaur_genera'
    pics_home_url = 'https://dinosaurpictures.org'

    # Navigate to wiki list homepage
    request_result = requests.get(wiki_list_url)
    request_content = request_result.content
    soup = BeautifulSoup(request_content, 'html.parser')

    # Find all list elements in the page and take out the proper ones
    all_li = soup.find_all('li')
    all_list_links = [element.find('a') for element in all_li]
    name_list = [element.string for element in all_list_links[6:-107]]

    if dev:
        print("List of dinosaurs found on Wikipedia:")
        for name in name_list:
            print(name)

    return name_list

if __name__ == "__main__":
    main()
