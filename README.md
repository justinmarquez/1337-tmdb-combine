# 1337-tmdb-combine

## run instructions
0. Install any needed requirements
1. Download ZIP
2. Extract ZIP
3. Run 'python3 <extracted_folder_path>/python/main.py' on terminal 

## summary
### part one - scraper
Using Python to programatically scrape top 100 movie torrents from a provided link (https://www.1337x.to/top-100-movies) to pull the following:
1. Name of torrent
2. IMDB ID
3. Size of torrent
4. Seeders
5. Leechers
6. Infohash
The above is stored in a MySQL database

### part two - tmdb
Using themoviedb API to retrieve TMDB data (using the IMDB ID from the previous part):
1. TMDB ID
2. Title
3. Keywords
The above is stored in a MySQL database.

### part three - combine
Using the data from Part 1 and Part 2, a new table with the data above is stored.

### useful information
#### MySQL
The MySQL database is hosted on AWS
#### python
Different python packages were used in the code
1. beautifulsoup4: used to parse elements from return HTML
2. pymysql: facilitate connection from code to MySQL database
3. urllib3: grab HTML from webpage
4. requests: grab JSON responses from TMDB API 

Exception handling is implemented at different stages in the python scripts, examples include:
1. Using a backup 1337x.to website, in case primary website does not want to connect
2. Inserting data into database table, if data already exists, it does not try to insert it
