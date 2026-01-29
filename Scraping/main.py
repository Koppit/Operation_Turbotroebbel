from get_studies import get_urls
import DataExtractor
import time

"""
Starter scraping av nettsiden
1. Hent alle linker til studie sider
2. Hent ut all data for hvert studi og lagre dem som json filer
"""

if __name__ == "__main__":
    # hent linker
    urls = get_urls()
    
    # les ut alle data for studier
    for url in urls:
        DataExtractor.extract(url)
        # vent litt mellom hver forespørsel
        time.sleep(1)
    
