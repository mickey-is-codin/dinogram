import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pymongo
from pymongo import MongoClient

log_file = open("../../logs/refresh.txt", "w+")

def main():

    # Open connection to MongoDB
    client = MongoClient('localhost', 27017)
    dino_base = client.dinogram

    # Build the actual html document that will comprise the email
    email_html = build_html(dino_name, wiki_paragraphs, image_links, dino_base)

    # Send the email
    send_dinogram(email_html, dino_base)

    log_file.close()
    client.close()

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

        smtp_server.sendmail(from_email, member, message.as_string())

    log_file.write('Finished sending mail!\n')
    log_file.flush()
    smtp_server.quit()

def fetch_creds(dino_base):

    senders_coll = dino_base.senders
    email  = senders_coll.find()[1]['Email']
    passwd = senders_coll.find()[1]['Passwd']

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

    body = body + '''
            \t\t\t\t<p>
            \t\t\t\t\t<small><a href="https://dinogram.org/unsub">Unsubscribe from Dinogram</a></small>
            \t\t\t\t</p>'''

    if len(paragraphs) == 0:
        body = body + '''\
            \t\t\t\t<p><font face="courier">
            \t\t\t\t\tNo information found for this dinosaur!
            \t\t\t\t</font></p>\n'''

    html = header + body + footer

    return html

if __name__ == "__main__":
    main()
