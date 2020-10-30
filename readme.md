# OLX-notifiler

This is a simple webscraping project that scrape OLX.pl for new offers and sends you an email when new offer was added.

## How to use:

First you have to configure you gmail smtp credencials in "gmail-credentials.yml".
You may need to change your gmal security settings to accepts simple logging in.

Then you run script with:

>> python olx-notify.py [olx_url] [session_name] [send_from] [send_to]

where:
- [olx_url] is a url with offers you search for. Jus go to olx.pl search for whatever you want, use filters you want and copy the url from web browser.
- [session_name] is just na name of a session. Is used to name a file that keeps the last scraped offers.
- [send_from] is a email address that you specify in gmail-credentials.yml
- [send_to] is a target email address that you want to be notified.

author: Cezary Pukownik