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

def write_dino_list(dino_list, dev=False):

    dino_list_path = "valid_dinos.csv"

    list_size = 0
    with open(dino_list_path, "wb") as list_file:
        header = "dinos\n".encode()
        list_file.write(header)
        for name in dino_list:
            line_string = name+"\n"
            line_string = line_string.encode()
            list_file.write(line_string)
            list_size += 1

    if dev:
        print("\n{} now contains {} dinosaurs".format(dino_list_path, list_size))

    return list_size


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
