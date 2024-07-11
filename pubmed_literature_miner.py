#! usr/bin/env python3
# Author Gaurav 
# Date 2024-6-20

from urllib.request import urlopen
from bs4 import BeautifulSoup
def candidaLiteratureMiner(term = None, fetch_count = None):
    """sumary_line
    a candidaliteratureMiner from pubmed, given the term as candida
    it will connect to the pubmed, prepare the ids that are releavant
    to the candida, and will return the literature for them.
    Keyword arguments:
    argument -- description
    term = "term" that you want to search in pubmed
    Return: return_description
    returns a ncbi pubmed id and the literature for the candida
    """
    
    pubmed_term = term
    count = fetch_count
    pubmed_open = urlopen(f"https://pubmed.ncbi.nlm.nih.gov/?term={pubmed_term}&sort=date&size={count}")
    ids_text = list(map(lambda n: n.strip().split(),\
                        (map(str,BeautifulSoup(pubmed_open, "html.parser").\
                             find_all("div", class_="share")))))
    ids = [i.split("/")[-2] for i in list(filter(lambda n: \
                         "ncbi" in n,[j for i in ids_text for j in \
                                             i if "permalink" in j]))]
    format_id_links = []
    for i in range(len(ids)):
        format_id_links.append(f"https://pubmed.ncbi.nlm.nih.gov/{ids[i]}/")
    ncbi_derive_information = {}
    for i in range(len(format_id_links)):
        ncbi_derive_information[ids[i]] = ''.join([i.get_text().strip() \
                for i in BeautifulSoup(urlopen(format_id_links[i]), \
                        "html.parser").find_all("div", class_ = "abstract-content selected")])
    return [(k,v) for k,v in ncbi_derive_information.items() if k or v != ""]
