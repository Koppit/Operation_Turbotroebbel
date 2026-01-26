from get_studies import get_urls

"""
This is main
"""

import DataExtractor



url = "https://fagskolen-viken.no/studier/ledelse/administrativ-koordinator"
url = "https://fagskolen-viken.no/studier/ledelse/praktisk-lederutdanning"
DataExtractor.extract(url)
