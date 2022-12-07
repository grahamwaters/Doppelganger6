import requests
from bs4 import BeautifulSoup
import os
import time
import pandas as pd
# configparser
import configparser


# Helper Functios
def get_profile_links(soup):
    """
    get_profile_links is a function that takes in a BeautifulSoup object and returns a list of profile links.

    :param soup: BeautifulSoup object
    :type soup: BeautifulSoup
    :return: list of profile links
    :rtype: list
    """
    links = soup.find_all('a', class_='mr-1')
    return links

def get_profile_data(soup):
    """
    get_profile_data is a function that takes in a BeautifulSoup object and returns a dictionary of profile data.

    :param soup: BeautifulSoup object
    :type soup: BeautifulSoup
    :return: dictionary of profile data
    :rtype: dict
    """
    data = {}
    data['name'] = soup.find('h1', class_='h3').text
    data['title'] = soup.find('h2', class_='h5').text
    data['location'] = soup.find('span', class_='text-black-50').text
    data['bio'] = soup.find('div', class_='mb-4').text
    return data

def get_profile_skills(soup):
    """
    get_profile_skills is a function that takes in a BeautifulSoup object and returns a list of profile skills.

    :param soup: BeautifulSoup object
    :type soup: BeautifulSoup
    :return: list of profile skills
    :rtype: list
    """
    skills = soup.find_all('span', class_='badge badge-light mr-1')
    return skills

def process_page(job_title,company_target,page_number=''):
    # begin by making a request to the website with the search query
    # job_title = 'Data Scientist'
    # company_target = 'IBM'

    # create the company and title strings
    company = company_target.replace(' ', '+')
    job = job_title.replace(' ', '+')

    # create the search query
    github_search_query = 'https://github.com/search?{}q={}+{}&type=users'.format(str(page_number),company, job)

    # make a request to the website
    response = requests.get(github_search_query)
    # this object contains (1) the status code of the request and (2) the content of the request (the HTML).
    page_response = response.status_code # 200 means the request was successful
    if page_response != 200:
        print('Error: Request was not successful.')
        return
    # get the HTML content of the request
    page_html = response.content

    # create a BeautifulSoup object
    soup = BeautifulSoup(page_html, 'html.parser')

    # get the profile links
    profile_links = get_profile_links(soup)

    return profile_links # return the profile links

def main():
    """
    main is the main function of the program.

    :return: None
    :rtype: None
    """

    # read your profile to an html file and save it to the data folder.
    # the profile url is in the config.ini file
    # read the config.ini file
    config = configparser.ConfigParser()
    config.read('config.ini')
    profile_url = config['default']['secondary_url']
    print('profile_url: ', profile_url, ' loaded from config.ini file')






    # begin by making a request to the website with the search query
    job_title = 'Data Scientist'
    company_target = 'IBM'

    # use the process_page function to get the profile links
    profile_links = process_page(job_title, company_target)

    # create a list to store the profile data
    profile_data = []

    # loop through the profile links
    for link in profile_links:
        time.sleep(3)
        print(f"scanning {link['href']}")
        # get the profile link
        profile_link = link['href']

        # add https://github.com/ as the base url to the profile link
        profile_link = 'https://github.com' + profile_link
        # make a request to the profile link

        # do not make a request if the html is already downloaded and saved. this is located in the data/{company}/{job_title} folder
        # check if the file exists

        if not os.path.exists(f'./data/{company_target}/{job_title}/{link["href"][1:]}.html'):
            response = requests.get(profile_link)
            # this object contains (1) the status code of the request and (2) the content of the request (the HTML).
            page_response = response.status_code
            if page_response != 200:
                print('Error: Request was not successful.')
                continue
                # get the HTML content of the request
            page_html = response.content

            # save that html to a file in the data/{company}/{job_title} folder with the name {link['href'][1:]}.html
            # save the html to a file
            # if the company and job title folder does not exist, then create it
            if not os.path.exists(f'data/{company_target}/{job_title}'):
                os.makedirs(f'data/{company_target}/{job_title}')
            # save the html to a file
            with open(f'data/{company_target}/{job_title}/{link["href"][1:]}.html', 'w+') as f:
                f.write(page_html.decode('utf-8'))
        else:
            # if the file exists, then read the file and save it to the response variable
            with open(f'data/{company_target}/{job_title}/{link["href"][1:]}.html', 'r') as f:
                response = f.read()





        # create a BeautifulSoup object
        #soup = BeautifulSoup(page_html, 'html.parser')

        # get the profile data
        #data = get_profile_data(soup)

        # get the profile skills
        #skills = get_profile_skills(soup)

        # add the profile data to the list
        #profile_data.append(data)

    # print the profile data
    print(profile_data)

if __name__ == '__main__':

    main()