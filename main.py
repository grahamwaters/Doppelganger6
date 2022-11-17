# from github import Github

# First create a Github instance:

# # using an access token
# g = Github("access_token")

# # Github Enterprise with custom hostname
# g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token")

# # Then play with your Github objects:
# for repo in g.get_user().get_repos():
#     print(repo.name)



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

def main():
    query = 'data science'
    url = url_builder(query)
    print(url)

if __name__ == '__main__':
    main()