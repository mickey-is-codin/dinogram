import os
import sys
import time
import json
import requests
import random
import datetime

import smtplib

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pymongo
from pymongo import MongoClient

log_file = open('/home/ubuntu/dino_log.txt', 'w+')

def main():

    log_file.write('\nBeginning program execution for {}...\n'.format(datetime.datetime.now()))
    log_file.flush()

    options = Options()
    options.headless = True

    # Instantiate web driver...very forcefully
    log_file.write('Attempting to establish webdriver...\n')
    log_file.flush()
    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(180)

    # Get list of wikipedia articles
    log_file.write('Accessing wikipedia list...\n')
    log_file.flush()
    wiki_names = scrape_names(driver, site='wiki')

    # Get list of dinosaurpictures.org articles
    log_file.write('Accessing picture site list...\n')
    log_file.flush()
    pics_names = scrape_names(driver, site='pics')

    # Make a list of the dinosaurs that belong to both
    valid_names = list(set(wiki_names) & set(pics_names))
    num_shared = len(valid_names)
    log_file.write('Found {} dinosaurs shared between both sites...\n'.format(num_shared))
    log_file.flush()

    # Pick a name out of a hat
    random_ix = random.randint(0,num_shared)
    dino_name = valid_names[random_ix]
    log_file.write('Random dinosaur: {}\n\n'.format(dino_name))
    log_file.flush()

    # Get a random wikipedia article and its text
    wiki_paragraphs = scrape_random_article(driver, dino_name)

    # Get links to images of the old guy
    image_links = scrape_image_links(driver, dino_name)

    # Open connection to MongoDB
    client = MongoClient('localhost', 27017)
    dino_base = client.dinogram

    # Build the actual html document that will comprise the email
    email_html = build_html(dino_name, wiki_paragraphs, image_links, dino_base)

    # Send the email
    send_dinogram(email_html, dino_base)

    log_file.close()
    client.close()
    driver.quit()

def send_dinogram(email_html, dino_base):

    log_file.write('Sending dinogram to mailing list\n')
    log_file.flush()

    gmail_address, gmail_passwd = fetch_creds(dino_base)

    mailing_list = fetch_mailing_list(dino_base)

    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(gmail_address, gmail_passwd)

    from_email = gmail_address

    for member in mailing_list:
        log_file.write('Mailing to {}\n'.format(member))
        message = MIMEMultipart('alternative')
        message['Subject'] = 'Dinogram'
        message['From']    = from_email
        message['To']      = member

        message_text = MIMEText(email_html, 'html')
        message.attach(message_text)

        #smtp_server.sendmail(from_email, member, message.as_string())

    log_file.write('Finished sending mail!\n')
    log_file.flush()
    smtp_server.quit()

def fetch_creds(dino_base):

    senders_coll = dino_base.senders
    email  = senders_coll.find()[0]['Email']
    passwd = senders_coll.find()[0]['Passwd']
    print(email, passwd)

    return email, passwd

def fetch_mailing_list(dino_base):

    users_coll = dino_base.users
    mailing_list = [user['Email'] for user in users_coll.find()]

    return mailing_list

def build_html(dino_name, paragraphs, image_links, dino_base):

    header = '''\
        <html>
        \t<head>\
        </head>
        \t\t<body>
        \t\t\t<div style="background-color:lightblue">
        \t\t\t\t<h1 \
            style="text-align:center;font-family: 'Mountains of Christmas';">\
            Dino of the Day: '''+dino_name+'''!</h1>'''

    footer = '''\
        \t\t\t</div>
        \t\t</body>
        </html>'''

    body = ''

    body = body + '''\
            \t\t\t\t<h2 style="text-align:center">Images of '''+dino_name+'''</h2>'''

    for link_ix, link in enumerate(image_links):

        if (link_ix % 2 == 0):
            body = body + '''\
	        \t\t\t\t<br>
	        \t\t\t\t\t<img \
		    style="display:block;margin-left:auto;margin-right:auto;height:400px;width:600px" \
		    src='''+link+'''>
	        \t\t\t\t<br>\n'''

    body = body + '''\
            \t\t\t\t<p> Images taken shamelessly from <a href="https://dinosaurpictures.org">dinosaurpictures.org.</a> </p>'''

    body = body + '''\
            \t\t\t\t<h2 style="text-align:center">Info on '''+dino_name+'''</h2>'''

    for paragraph in paragraphs:
        body = body + '''\
            \t\t\t\t<p><font face="courier">
            \t\t\t\t\t'''+paragraph+'''
            \t\t\t\t</font></p>\n'''

    if len(paragraphs) == 0:
        body = body + '''\
            \t\t\t\t<p><font face="courier">
            \t\t\t\t\tNo information found for this dinosaur!
            \t\t\t\t</font></p>\n'''

    html = header + body + footer

    return html

def scrape_image_links(driver, random_dino_string):

    base_url = 'https://dinosaurpictures.org/'
    full_url = base_url + random_dino_string + '-pictures'
    log_file.write('Pictures site url: {}\n\n'.format(full_url))
    log_file.flush()

    driver.get(full_url)

    images_div = driver.find_element_by_xpath('/html/body/div[1]/div[4]')

    image_elements = images_div.find_elements_by_xpath('.//a')
    image_link_list = [image.get_attribute('href') for image in image_elements]
    image_link_list = [link for link in image_link_list if link[-4:] == '.jpg']

    return image_link_list

def scrape_random_article(driver, random_dino_string):

    base_url = 'https://en.wikipedia.org/wiki/'
    article_url = base_url + random_dino_string
    log_file.write('Wikipedia article url: {}\n'.format(article_url))
    log_file.flush()

    article_result = requests.get(article_url)
    article_content = article_result.content
    article_soup = BeautifulSoup(article_content, 'html.parser')

    article_paragraphs = [p_elem.get_text() for p_elem in article_soup.find_all('p')]
    article_paragraphs = [para for para in article_paragraphs if len(para) > 15]

    #for para_ix in range(len(article_paragraphs)):
    #    log_file.write(article_paragraphs[para_ix])

    return article_paragraphs

def scrape_names(driver, site):

    wiki_list_url = 'https://en.wikipedia.org/wiki/List_of_dinosaur_genera'
    pics_home_url = 'https://dinosaurpictures.org'

    if site == 'wiki':
        # Navigate to wiki list homepage
        request_result = requests.get(wiki_list_url)
        request_content = request_result.content
        soup = BeautifulSoup(request_content, 'html.parser')

        # Find all list elements in the page and take out the proper ones
        all_li = soup.find_all('li')
        all_list_links = [element.find('a') for element in all_li]
        name_list = [element.string for element in all_list_links[6:-107]]
        log_file.write('Found {} dinosaurs on wikipedia page\n\n'.format(len(name_list)))
        log_file.flush()

        return name_list

    elif site == 'pics':
        # Navigate to picture site homepage
        driver.get(pics_home_url)

        # Click show more link
        view_all_link = driver.find_element_by_link_text('show more...')
        view_all_link.click()

        # Get dino-list div
        list_div_xpath = driver.find_element_by_xpath('/html/body/div[1]/div[3]/ul')

        # Get all links contained within dino-list div
        dino_links_xpath = list_div_xpath.find_elements_by_xpath('.//li')
        log_file.write('Found {} dinosaurs on picture site\n\n'.format(len(dino_links_xpath)))
        log_file.flush()

        # Create list of all names and create link for each
        name_list = [a_elem.text for a_elem in dino_links_xpath]

        return name_list

if __name__ == '__main__':
    main()
