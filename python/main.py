#!/usr/bin/env python3

'''
Author: Justin Marquez
Date of Submission: 03 December 2020

Summary: Main python file to run coding assessment
'''

from scraper import scraper as scraper
from tmdb import tmdb as tmdb
from combine import combine as combine

def coding_challenge():
    scraper()
    tmdb()
    combine()

if __name__ == '__main__':
    coding_challenge()