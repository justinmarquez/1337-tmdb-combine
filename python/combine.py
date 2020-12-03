#!/usr/bin/env python3

'''
Author: Justin Marquez
Date of Submission: 03 December 2020

Summary: Combine 1337x.to's data with tmdb's API
'''

from methods import *

def combine():
    print('\nCombining data from 1337x.to and TMDB API...')
    connection = create_connection()

    # Handles if record is already in database
    try:
        with connection.cursor() as cursor:
            sql = "insert into `torrent_tmdb_join` select `torrent_name`, `title`, `torrents_1337`.`imdb_id`, `tmdb_id`," \
                    " `size`, `seeders`, `leechers`, `infohash`, `keywords` " \
                  "from `torrents_1337` " \
                  "left join `tmdb` on `torrents_1337`.`imdb_id` = `tmdb`.`imdb_id`;"

            cursor.execute(sql)

        connection.commit()
        connection.close()

    except:
        pass
    print('\nProcess Complete!')
