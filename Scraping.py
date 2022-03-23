import time
import requests
from bs4 import BeautifulSoup


client = requests.Session()
headers = { # U need Burp Suite for this
}

for i in range(1, 20):
    keywords = ["nitro"]
    for keyword in keywords:
        r = client.get(f'https://disboard.org/servers/tag/{keyword}/{i}?sort=-member_count', headers=headers).text
        servers = BeautifulSoup(r, 'html.parser').findAll('div', class_="column is-one-third-desktop is-half-tablet")
        for server in servers:
            dataid = server.find('a', class_="button button-join is-discord").get('data-id')
            x = client.post(f"https://disboard.org/site/get-invite/{dataid}", headers=headers)
            
            # Setting disini supaya cloudflare ga detect ddos (Too Many Request)
            time.sleep(2)
            invite = x.text.replace('"', '')
            origin = requests.get(invite).url
            with open("servers.txt", "a+") as f:
                f.write(f"{origin}\n")
