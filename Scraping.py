#!/usr/bin/python3
import time,CSV,requests
from bs4 import BeautifulSoup

print("STARTS")

client = requests.Session()
headers = {
'Sec-Ch-Ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
'Authority': 'disboard.org',
'Cookie': 'PHPSESSID=inr2firhjcpe43ct2p72ipq5s5; _csrf=7a0ea6092fcf626b8fe8cd1ecb91261cdea7f164962c453fcb564a1850fd1fdda%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22bM7vIX53gIZ6417Vju5PwwGvqvFY5gbw%22%3B%7D; cf_chl_2=2e8fb528997e3f8; cf_chl_prog=x14; cf_clearance=O26rtVgRCDFfvn41TmvJ3kRG8rnuSOx.4HXE55NG1Io-1647965692-0-250',
'x-csrf-token': 'ekXjLfY6wocYFPEl0UdWzih5of52L0hTwgPPPOVXlSQYCNRbv2L3tH9dqxPldmGYQgyUrgFYDyWzdYll0DD3Uw==',
'Dnt': '1',
'Sec-Ch-Ua-Mobile': '?0',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
'Accept': '*/*',
'X-Requested-With': 'XMLHttpRequest',
'Sec-Ch-Ua-Platform': "Linux",
'Origin': 'https://disboard.org',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Dest': 'empty',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'en-US,en;q=0.9,id;q=0.8'
}


KEYWORDS = ["nitro"]
PAGES = 20
SLEEP = 3
LINKS = []

with open("servers.txt", "r") as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=',')
    
    for row in csv_reader:
        LINKS.append(row[0])

    #print(LINKS)
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
                    # Setting disini supaya cloudflare ga detect ddos (Too Many Request)
                    time.sleep(SLEEP)
                    invite = x.text.replace('"', '')
                    origin = requests.get(invite).url

                    if origin not in LINKS:
                        csv_file.write(f"{origin}\n")
                        print(f"{origin} added")
                    else:
                        print(f"{origin} already in list, skipping...")
