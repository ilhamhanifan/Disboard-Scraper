from bs4 import BeautifulSoup
from scrapingant_client import ScrapingAntClient
client = ScrapingAntClient(token='XXX')

for i in range(3):
    keywords = ["nitro"]
    for keyword in keywords:
        r = client.get(
            f'https://disboard.org/servers/tag/{keyword}/?sort=-member_count/{i}', ).text
        servers = BeautifulSoup(r, 'html.parser').findAll(
            'div', class_="column is-one-third-desktop is-half-tablet")
        for server in servers:
            dataid = server.find(
                'a', class_="button button-join is-discord").get('data-id')
            # https://disboard.org/site/get-invite/
            url = f"https://disboard.org/server/join/{dataid}"
            x = client.get(url)
            invite = x.text.replace('"', '')
            print(f'{invite}')
            with open("servers.txt", "a+") as f:
                f.write(f"{invite}\n")
