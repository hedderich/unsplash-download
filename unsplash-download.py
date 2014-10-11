#!/usr/bin/env python

import urllib.request
import re
import os

try:
    from bs4 import BeautifulSoup, SoupStrainer
except ImportError as e:
    print("Could not import beatifulsoup4. Make sure it is installed.")
    if DEBUG:
        print(e, file=sys.stderr)

DEBUG         = False
download_path = 'downloads'
base_url      = 'https://unsplash.com'
page          = 1
link_search   = re.compile("/photos/[a-zA-Z0-9]+/download")

if not os.path.exists(download_path):
    os.makedirs(download_path)

while True:
    url = base_url + "/?page=" + str(page)
    print("Parsing page %s" % url)
    try:
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "lxml")
        for tag in soup.find_all(href=link_search):
            image_id     = str(tag['href']).split('/')[2]
            download_url = base_url + str(tag['href'])
            
            if os.path.exists("%s/%s.jpeg" % (download_path, image_id)):
                print("Not downloading duplicate %s" % download_url)
                continue

            print("Downloading %s" % download_url)
            urllib.request.urlretrieve(
                base_url + str(tag["href"]),
                "%s/%s.jpeg" % (download_path, image_id)
            )
            
    except HTMLParser.HTMLParseError as e:
        print('Error parsing the HTML', file=sys.stderr)
        if DEBUG:
            print(e, file=sys.stderr)
    except Exception as e:
        print("An unknown error occured", file=sys.stderr)
        if DEBUG:
            print(e, file=sys.stderr)
    finally:
        page = page + 1