#!/usr/bin/python3
import time,CSV,requests
from bs4 import BeautifulSoup

print("STARTS")

client = requests.Session()
headers = { # U need Burp Suite for this
}

KEYWORDS = ["nitro"]
PAGES = 20
SLEEP = 3
LINKS = []

with open("servers.txt", "r") as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=',')
    
    for row in csv_reader:
        LINKS.append(row[0])


    with open("servers.txt", "w") as csv_file:
        for keyword in KEYWORDS:
            for page in range(PAGES):
                print(f"sending request for {keyword} at page {page} ")
                r = client.get(f'https://disboard.org/servers/tag/{keyword}/{page}?sort=-member_count', headers=headers).text
                print(f"request received")
                servers = BeautifulSoup(r, 'html.parser').findAll('div', class_="column is-one-third-desktop is-half-tablet")
                for server in servers:
                    print("Fetching Invite Link")
                    dataid = server.find('a', class_="button button-join is-discord").get('data-id')
                    x = client.post(f"https://disboard.org/site/get-invite/{dataid}", headers=headers)                    
                    invite = x.text.replace('"', '')
                    origin = requests.get(invite).url

                    if origin not in LINKS:
                        csv_file.write(f"{origin}\n")
                        print(f"{origin} added")
                    else:
                        print(f"{origin} already in list, skipping...")
                    
                    # Slow the Request down to prevent Cloudflare detection (Too Many Request)
                    time.sleep(SLEEP)
                        
