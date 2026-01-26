from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time

"""
les ut alle nettside linkene til studiene ved fagskolen
"""

def get_urls() -> list:

    base_url = "https://fagskolen-viken.no/"

    # studiene er listet over flere sider, så inkrementer sidetall til alt er lest ut
    page = 0
    urls = []
    while True:

        # send
        req = Request(f"{base_url}studier?page={page}", headers={"User-Agent": "Mozilla/5.0"})
        html = urlopen(req).read().decode("utf-8", errors="ignore")
        soup = BeautifulSoup(html, "lxml")

        results = soup.find_all("a", class_="study-guide__link", href=True)

        # gå ut av loop når det ikke er nye resultater
        if not results:
            break

        # legg linker i listen
        for link in results:
            urls.append(base_url + link['href'])

        page += 1

        # vent litt mellom hver forespørsel
        time.sleep(0.5)

    return urls

if __name__ == "__main__": 
    print(get_urls())