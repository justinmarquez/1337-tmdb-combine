#!/usr/bin/env python3

'''
Author: Justin Marquez
Date of Submission: 03 December 2020

Summary: Programatically use tmdb's API to grab additional data
'''

from methods import *

def tmdb():
    print('\nPulling tmdb_id, title, and keywords from TMDB API...')

    # Selects all imdb_id's from torrents_1337 and adds imdb_id's to list to use in TMDB API
    connection = create_connection()

    # Extract all imdb_id's from scrapping 1337x.to
    try:
        with connection.cursor() as cursor:

            sql = "SELECT `imdb_id` FROM `torrents_1337` WHERE `imdb_id` LIKE 'tt%'"
            cursor.execute(sql)
            result = cursor.fetchall()

            imdb_id_list = [i['imdb_id'] for i in result]
    except:
        pass

    # Requesting and retrieving JSON from TMDB API
    API_KEY = get_tmdb_api_key()

    for imdb_id in imdb_id_list:
        api_request = 'https://api.themoviedb.org/3/find/' + imdb_id + '?api_key=' + API_KEY + \
                      '&language=en-US&external_source=imdb_id'
        json_response = json_response_api(api_request, 'movie_results')

        # Variables retrieved from TMDB API
        try:
            api_request = 'https://api.themoviedb.org/3/find/' + imdb_id + '?api_key=' + API_KEY + \
                          '&language=en-US&external_source=imdb_id'
            json_response = json_response_api(api_request,'movie_results')

            # tmdb_id and title
            tmdb_id = json_response['id']
            title = json_response['title']

            # Keywords
            api_request_keywords = 'https://api.themoviedb.org/3/movie/' + str(tmdb_id) + '/keywords?api_key=' + API_KEY
            keywords = json_response_api(api_request_keywords,'keywords')
            keywords_list = []
            for i in range(len(keywords)):
                keywords_list.append(keywords[i].get('name'))
            keywords_list = str(keywords_list)

            # Insert into database
            connection = create_connection()
            try:
                with connection.cursor() as cursor:
                    # Handles if tmdb_id is already in database
                    try:
                        sql = "INSERT INTO `tmdb` (`tmdb_id`, `imdb_id`, `title`, `keywords`) VALUES (%s, %s, %s, %s)"
                        cursor.execute(sql, (tmdb_id, imdb_id, title, keywords_list))
                    except:
                        pass
                connection.commit()

            finally:
                connection.close()

        except:
            pass