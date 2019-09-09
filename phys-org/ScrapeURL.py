import requests
from bs4 import BeautifulSoup
from time import sleep
from typing import List

url = "https://m.phys.org"

def is_valid_link(link):
    """A valid link has /news/YYYY/ in the URL. Until they change their back end"""
    index = link.find('/news/')
    if (index < 0):
        return False
    # Check if NEXT 4 characters are a year
    try:
        next_four = link[index + 6:index + 6 + 4]
        yr = int(next_four)
        if ((yr < 2022) and (yr > 1970)):
            return True
    except:
        return False
    return False

def get_article_urls(url):
    """Grab all 'valid' links from input URL."""
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
    }

    r = requests.get(url, headers=header)

    if (r.status_code != 200):
        raise ConnectionRefusedError('Connection to website not successful.')

    soup = BeautifulSoup(r.content, 'html5lib')
    all_anchors = soup.find_all('a', href=True)
    all_anchors = list(set(all_anchors)) # remove duplicates
    valid_anchors = [l['href'] for l in all_anchors if (is_valid_link(l['href']))]
    
    return valid_anchors


def get_many_urls(base_url: str, num_pages = 10, delay = 0.1) -> List[str]:
    """Make num_pages requests and grab the valid URLs.
    
    Parameters
    ------
    base_url : string
        The url on which we build the paginated URL
    num_pages : int
        Number of pages we want to crawl through (must be greater than 1)
    delay : float
        Length of time between requests (in seconds). Set so we do not overload their servers.
    
    Example
    ------
    We want to get all article links in the first 10 pages of the mobile site.
        >>> base_url = 'https://m.phys.org'
        >>> urls = get_many_urls(base_url)
    """
    n_requests = num_pages
    if (num_pages < 1):
        n_requests = 1
    
    all_urls = set()
    for n in range(num_pages):
        go_to_url = base_url + '/page{}.html?spotlight=false'.format(n + 1)
        all_urls = all_urls.union(set(get_article_urls(go_to_url)))
        sleep(delay) # sleep for 0.1 seconds -- make up to 10 requests per second
        
    return list(all_urls)
