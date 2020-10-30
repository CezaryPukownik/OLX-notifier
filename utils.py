import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import yaml

import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
#%%

def send_mail(send_from, send_to, subject, body):
    with open('gmail-credentials.yml') as file:
        credentials = yaml.safe_load(file)

    #The mail addresses and password
    sender_pass = credentials[send_from]['pass']

    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = send_from
    message['To'] = send_to
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    session = smtplib.SMTP('smtp.gmail.com', 587) 
    session.starttls() 
    session.login(send_from, sender_pass) 
    text = message.as_string()
    session.sendmail(send_from, send_to, text)
    session.quit()

    now = datetime.datetime.now()
    print(f'{now}: Mail sent to {send_to}.')
    


# get data from OLX
def scrape_olx(olx_url):
    columns = ['Title', 'Price', 'Link', 'Location', '', '', 'Date']
    olx_data = pd.DataFrame(columns=columns)

    # get avaible pages
    page = 1
    url = '{olx_url}&page={page}'
    r = requests.get(url.format(olx_url=olx_url, page=page))
    soup = BeautifulSoup(r.content, 'html.parser')

    # when is only one page, there is no html object that cac select page
    try:
        avaible_pages = [int(page.text.strip()) for page in soup.find(class_="pager rel clr").find_all(class_='item fleft')]
    except:
        avaible_pages = [1]

    for page in avaible_pages:
        r = requests.get(url.format(olx_url=olx_url, page=1))
        soup = BeautifulSoup(r.content, 'html.parser')
        offers = []
        for offer in soup.find_all(class_='offer-wrapper'):
            offer_data = []
            offer_data.append(offer.find(class_='title-cell').find('strong').text)
            offer_data.append(offer.find(class_='price').text.strip())
            offer_data.append(offer.find(class_='title-cell').find('a').get('href'))
            offer_data.extend(offer.find(class_='bottom-cell').text.strip().split('\n'))
            # offer_data.append(page)
            offers.append(offer_data)

        olx_data = pd.concat([olx_data, pd.DataFrame(offers, columns=columns)])
    
    olx_data = olx_data.drop('', axis=1).drop_duplicates()
    return olx_data
# %%
