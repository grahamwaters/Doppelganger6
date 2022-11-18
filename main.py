# from github import Github

# installation steps
# pip3 install pipreqs
# python3 -m pipreqs.pipreqs . --force


# First create a Github instance:

# # using an access token
# g = Github("access_token")

# # Github Enterprise with custom hostname
# g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token")

# # Then play with your Github objects:
# for repo in g.get_user().get_repos():
#     print(repo.name)

import re
import os
import pandas as pd
from zipfile import ZipFile
from bs4 import BeautifulSoup
from tqdm import tqdm
# import spacy and load the language library to use for NER
import spacy


nlp = spacy.load('en_core_web_md')

def get_companies_and_orgs(query):
    # get the entities from the query
    doc = nlp(query)
    # get the entities from the query that are businesses
    entities = [X.text for X in doc.ents if X.label_ in ['GPE']] # gets the entities that are businesses

    return entities



def top_companies(industry=None):
    # constants
    memory_save_mode = False
    # read in the data
    if os.path.exists('./data/top_10000_tech_companies.csv'):
        try:
            print("Loading data for the top 7+ million tech companies in the US as of 2022...")
            df = pd.read_csv('./data/top_10000_tech_companies.csv')
        except Exception as e:
            print(e)
            print("Error loading data for the top 7+ million tech companies in the US as of 2022. Rebooting...")
            # remove the file if it exists
            if os.path.exists('./data/top_10000_tech_companies.csv'):
                os.remove('./data/top_10000_tech_companies.csv')
            # restart the program
            top_companies() # restart the program
    else:
        print("Getting data for the top 7+ million tech companies in the US as of 2022...")
        print("Peeking into the Zip file and taking only: company name, country, linkedin url, and current employees")

        extracted_df = pd.DataFrame() # create an empty dataframe to store the extracted data

        criteria = {
            'country': 'United States',
            'industry': 'Information Technology and Services'
        }
        with ZipFile('data/kaggle_companies.zip') as zf:
            for file in zf.namelist():
                print("Extracting data from file: {}".format(file))
                print(f"This is file {zf.namelist().index(file)+1} of {len(zf.namelist())}") # print the file number
                # only extract the top 10000 tech companies from the zip file
                if not file.endswith('.csv'): # if the file is not a csv file, skip it
                    continue # skip the file
                with zf.open(file) as f: # to minimize memory usage, and follow the KISS principle, we are going to ONLY get the company names from the zip file
                    # in batches of 1000 rows at a time (this is the default for read_csv) read the csv file's company names into a list
                    if memory_save_mode:
                        for df in tqdm(pd.read_csv(f, chunksize=1000)):
                            # filter the dataframe by the criteria
                            df = df[df['country'] == criteria['country']]
                            # append the filtered dataframe to the extracted_df dataframe
                            # use the concat method to append the dataframes
                            extracted_df = pd.concat([extracted_df, df], ignore_index=True)
                            # if the extracted_df dataframe has more than 10000 rows, break out of the loop
                            if extracted_df.shape[0] > 10000:
                                break
                    else:
                        # load only the company name column from the csv file f into a dataframe df
                        #df = pd.read_csv(f, usecols=['company_name','linkedin_url','country','current_employees'])
                        df = pd.read_csv(f, usecols=['name','linkedin url','country'])
                        # filter the dataframe by the criteria for the country USA
                        df = df[df['country'] == criteria['country'].lower()]
                        # filter the dataframe by the criteria for the industry tech (one of the tech options for the industry column)
                        df = df[df['industry'] == criteria['industry'].lower()]
                        # append the filtered dataframe to the extracted_df dataframe
                        # use the concat method to append the dataframes
                        extracted_df = pd.concat([extracted_df, df], ignore_index=True)
                        # if the extracted_df dataframe has more than 10000 rows, break out of the loop.
                        # save the dataframe to a csv file
                        break
                    print("Extracted data from file: {}".format(file)) # print the file number
                    extracted_df.to_csv('./data/top_10000_tech_companies.csv', index=False)

        # save the contents of either df or extracted_df to a csv file whichever is not empty (if both are full, save extracted_df)
        if not extracted_df.empty:
            extracted_df.to_csv('./data/top_10000_tech_companies.csv', index=False)
        elif not df.empty:
            df.to_csv('./data/top_10000_tech_companies.csv', index=False)
        else:
            df.to_csv('./data/top_10000_tech_companies.csv', index=False)
            print("Error: both dataframes are empty. Saved anyway to prevent data loss.")




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


def industry_filterer(string_to_find,other_string=None):
    # read in the industries.csv file
    industries_df = pd.read_csv('./data/industries.csv')
    # only include the unique industries
    industries_df = industries_df.drop_duplicates(subset=['industry'])
    # reset the index
    industries_df = industries_df.reset_index(drop=True)
    # filter to get only tech companies or nonprofits
    if other_string is None:
        industries_df = industries_df[industries_df['industry'].str.contains(string_to_find, case=False)]
    else:
        industries_df = industries_df[industries_df['industry'].str.contains(string_to_find, case=False) | industries_df['industry'].str.contains(other_string, case=False)]
        list_of_results = industries_df['Industry'].to_list()

    # save the list of results to a file called industries.txt
    with open('./data/industries.txt', 'w') as f:
        for item in list_of_results:
            f.write("%s " % item)
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

def scrape_github_search_results(url, companies):
    # get the html
    # html = requests.get(url).text
    # create a soup object
    # read the html file saved in the data folder for these tests
    print("Scraping the Github search results page...")
    with open('./data/testpage.html', 'r') as filetoread:
        html = filetoread.read() # read the html file saved in the data folder for these tests

    soup = BeautifulSoup(html, 'html.parser')
    # find all the divs with the class "d-flex hx_hit-user px-0 Box-row"
    user_divs = soup.find_all('div', {'class': 'd-flex hx_hit-user px-0 Box-row'})
    # create a list to store the data
    users = []
    # loop through each div
    for div in tqdm(user_divs):
        # create a dictionary to store the data for each user
        user = {}
        # get the user's username
        temp_text = div.find('div', {'class': 'f4 text-normal'}).text.strip()
        # replace the \xa0 with a space and the \n with nothing (remove the newline) and strip the whitespace from the ends
        user['username'] = temp_text.replace('\xa0', ' ').replace('\n', ',').strip().split(',')[-1]
        # get the users name
        user['Name'] = div.find('div', {'class': 'f4 text-normal'}).find('a').text.strip()
        # get the user url
        user['url'] = 'https://github.com' + div.find('div', {'class': 'f4 text-normal'}).find('a')['href']
        # get the user image url
        user['image_url'] = div.find('img')['src']
        # get the user description (if available) - this is in the <p> tag with the class containing mb-1
        try:
            user['description'] = div.find('p', {'class': re.compile('mb-1')}).text.strip()
        except:
            user['description'] = 'no description'
        #* More details
        user['company'] = 'non detected'
        original_description = user['description']
        if original_description != 'no description':
            # use spacy to identify the company name in the description
            doc = nlp(original_description)
            # get the entities
            entities = get_companies_and_orgs(doc) # get the entities
            return_string = ' '.join(entities)
            # if the return string is not empty, then we found a company name
            if return_string != '':
                user['company'] = return_string
                # if the company name is in the list of companies, then we found a tech company
                if return_string in companies:
                    user['tech_company'] = True
                else:
                    user['tech_company'] = False
            else:
                user['tech_company'] = False
        else:
            user['tech_company'] = False
        # get the user location


        # get the user location (if available)
        # the user's location is the first div class beneath the div with class "d-flex flex-wrap text-small color-fg-muted" (if available)
        try:
            user['location'] = div.find('div', {'class': 'd-flex flex-wrap text-small color-fg-muted'}).find_all('div')[0].text.strip()
        except AttributeError:
            user['location'] = 'none' # if the user's location is not available, set it to 'none'
        users.append(user)

    print("I found {} users you might want to know!".format(len(users)))
    return users







def top_company_preprocessing():
    # load top companies from csv into memory.
    top_companies()
    # make a list of the companies
    top_companies_df = pd.read_csv('./data/top_10000_tech_companies.csv').rename(columns={'name': 'company_name'}) #  read the csv file into a dataframe and rename the column 'name' to 'company_name' for clarity
    list_of_companies = list(top_companies_df['company_name'].unique()) # make a list of the companies
    # create a list to store the data
    return list_of_companies



def main():

    list_of_companies = top_company_preprocessing() # companies in the chosen industries
    # in this case 'tech' and 'nonprofit'


    query = 'data science'

    url = url_builder(query)

    users = scrape_github_search_results(url, list_of_companies)
    # save the data to a csv file
    df = pd.DataFrame(users)
    df.to_csv('./data/github_users.csv', index=False)


if __name__ == '__main__':
    main()