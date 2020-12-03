#!/usr/bin/env python3

'''
Author: Justin Marquez
Date of Submission: 03 December 2020

Summary: Centralized location for all written methods and imports
'''

import pymysql.cursors
import requests
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen, Request
from secret import secret as secret


def get_tmdb_api_key():
    API_KEY = secret.API_KEY

    return API_KEY

def page_soup_req(url):
    # Pipe it through Mozilla, to circumvent 403 errors and to emulate browser
    req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})

    # Grab HTML from URL
    url_html = urlopen(req).read().decode('utf-8')
    page_soup = soup(url_html,'html.parser')

    return page_soup

def create_connection():
    connection = pymysql.connect(
        host=secret.host,
        user=secret.user,
        password=secret.password,
        db=secret.db,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    return connection

def json_response_api(api_request,key):
    response = requests.get(api_request)
    response.raise_for_status()

    if key == 'keywords':
        json_response = response.json()[key]
    else:
        json_response = response.json()[key][0]

    return json_response