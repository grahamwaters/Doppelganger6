# from github import Github

# First create a Github instance:

# # using an access token
# g = Github("access_token")

# # Github Enterprise with custom hostname
# g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token")

# # Then play with your Github objects:
# for repo in g.get_user().get_repos():
#     print(repo.name)

import requests
from bs4 import BeautifulSoup


def process_query(query):
    return str(query).replace(' ', '+').lower()



def url_builder(query):
    query_line = process_query(query)

    extensions = ['py','ipynb','md'] # replace spaces here with extension%3A
    extensions = ['extension%3A' + ext for ext in extensions]
    extension_line = ''.join(extensions) # join extensions with .join

    locations = ['Austin'] # replace spaces here with location%3A
    locations = ['location%3A' + str(x) for x in locations if x != '']
    locations_line = ''.join(locations) # join locations with .join

    sort_type = 'o=desc&' # sort by most followers
    # page_num = '&p=2' # page number
    page_num = ''
    type_line = '&type=users' # search for users

    url = "https://github.com/search?{}{}q={}+{}+{}{}".format(sort_type,
                                                            page_num,
                                                        query_line,
                                                        extension_line,
                                                        locations_line,
                                                        type_line)
    return url



#* Part 2 - Scrape the Github Search Results Page

# On the Github search results page, we want to scrape the following information for each user:

# all the data is contained in the div with the class "d-flex hx_hit-user px-0 Box-row"
#     - User's Actual Name (if available)
#     - username on GitHub
#     - user url
#     - user image url
#     - user description
#     - user location
#     - user email (if available)

def scrape_github_search_results(url):
    # get the html
    html = requests.get(url).text
    # create a soup object
    soup = BeautifulSoup(html, 'html.parser')
    # find all the divs with the class "d-flex hx_hit-user px-0 Box-row"
    user_divs = soup.find_all('div', {'class': 'd-flex hx_hit-user px-0 Box-row'})
    # create a list to store the data
    users = []
    # loop through each div
    for div in user_divs:
        # create a dictionary to store the data for each user
        user = {}
        # get the user's actual name
        user['name'] = div.find('div', {'class': 'f4 text-normal'}).text.strip()
        # get the username
        user['username'] = div.find('div', {'class': 'f4 text-normal'}).find('a').text.strip()
        # get the user url
        user['url'] = 'https://github.com' + div.find('div', {'class': 'f4 text-normal'}).find('a')['href']
        # get the user image url
        user['image_url'] = div.find('img')['src']
        # get the user description
        user['description'] = div.find('p', {'class': 'f4 text-normal mb-1'}).text.strip()
        # get the user location
        user['location'] = div.find('p', {'class': 'f4 text-normal mb-1'}).find('span', {'class': 'd-inline-block ml-2'}).text.strip()
        # get the user email
        user['email'] = div.find('p', {'class': 'f4 text-normal mb-1'}).find('a').text.strip()
        # append the user dictionary to the users list
        users.append(user)
    return users







def main():
    query = 'data science'
    url = url_builder(query)
    print(url)

if __name__ == '__main__':
    main()