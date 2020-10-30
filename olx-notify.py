# %%
import pandas as pd
from utils import send_mail, scrape_olx
import time
import datetime
import sys

olx_url = sys.argv[1]
session_name = sys.argv[2]
send_from = sys.argv[3]
send_to = sys.argv[4]


# read data from db
# if there is no file just pass
try:
    data = pd.read_feather(f'{session_name}.feather')
except:
    pass



#%%
while True:
    now = datetime.datetime.now()
    try:
        # get new data
        print(f'{now}: Scraping OLX')
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
            send_mail(send_from=send_from, 
                send_to=send_to,
                subject='New OLX offer!!',
                body=body)

            # reload db
            new_data.to_feather(f'{session_name}.feather')
            data = pd.read_feather(f'{session_name}.feather')
        else:
            print(f'{now}: No new offers found.')
            pass
    except KeyboardInterrupt:
        print(f'{now}: Interupted')
    
    # sleep for 5 minutes
    time.sleep(5*60) # 5 min sleep