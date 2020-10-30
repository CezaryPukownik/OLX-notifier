# %%
import pandas as pd
from utils import send_mail, scrape_olx
import time
import datetime

# read data from db
data = pd.read_feather('focusrite.feather')

#%%
while True:
    now = datetime.datetime.now()
    try:
        # get new data
        print(f'{now}: Scraping OLX')
        olx_url = 'https://www.olx.pl/oferty/q-focusrite-2i2/?search%5Bfilter_float_price%3Ato%5D=500'
        new_data = scrape_olx(olx_url=olx_url)

        # check for new
        existing_links = set(data['Link'].values)
        new_links = set(data['Link'].values)
        intersection = new_links.intersection(existing_links)
        new_offers = new_data[~new_data['Link'].isin(intersection)]

        if new_offers.shape[0] > 0: # if there is new 
            print(f'{now}: New offer(s) found!')
            # send main
            body = '\n\n'.join([ '\n'.join([row['Title'], row['Price'], row['Link']]) for __, row in new_offers.iterrows() ])
            send_mail(send_from='python.notificaiton@gmail.com', 
                send_to='cezary.pukownik@gmail.com',
                subject='Nowe ogłoszenie OLX!!',
                body=body)

            # reload db
            new_data.to_feather('focusrite.feather')
            data = pd.read_feather('focusrite.feather')
        else:
            print(f'{now}: No new offers found.')
            pass
    except KeyboardInterrupt:
        print(f'{now}: Interupted')
    
    time.sleep(5*60) # 5 min sleep

#%%
# uncoment for reset a db file
# empty = pd.DataFrame(columns=['Title', 'Price', 'Link', 'Location', 'Date'])
# new_offers.to_feather('focusrite.feather')
# empty.to_feather('focusrite.feather')
# %%
