# Process of development for Doppelganger6

The links will look like this: `https://github.com/search?q=IBM+Data+Scientist&type=users`

As we move through the search results this will change to look like this `https://github.com/search?p=3&q=IBM+Data+Scientist&type=Users`

where the 3 is denoting "page 3" of the search results.

This link shows all the "Data Scientist" profiles on GitHub that have "IBM" in their bio. Now we need to extract their profile pages as html documents and then extract the information we need from them. We will use the `requests` library to get the html documents and the `BeautifulSoup` library to extract the information.

```python
import requests
from bs4 import BeautifulSoup
```
The class of the profile link is `mr-1` which we want to extract the link from. We will use the `find_all` method of the `BeautifulSoup` class to get all the links with the class `mr-1`.

```python
def get_profile_links(soup):
    links = soup.find_all('a', class_='mr-1')
    return links
```
