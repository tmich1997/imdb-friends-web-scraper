# Inspired by this post on LinkedIn: https://www.linkedin.com/feed/update/urn:li:activity:7132835328045830144/
# Used this as a reference: https://abdulrwahab.medium.com/how-to-build-a-python-web-scraper-to-capture-imdb-top-100-movies-908bf9b6bc19

# All the ncessary 
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

seasons_list = list(range(1,11))
seasons_list = list(map(str, seasons_list))

imdb_url_base = 'https://www.imdb.com/title/tt0108778/episodes/?season='
imdb_url_list = []

for season in seasons_list:
    imdb_url_list.append(imdb_url_base + season)

episode_title = []
episode_rating = []
episode_air_date = []
episode_description = []

for url in imdb_url_list:

    imdb_url = url
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
           "Accept-Language": "en-US, en;q=0.5"}

    response = requests.get(imdb_url, headers=headers)
    html_content = response.content

    friends_soup = BeautifulSoup(html_content, 'html.parser')

    episode_title_html = friends_soup.find_all('div', {"class": "ipc-title__text"})
    episode_rating_html = friends_soup.find_all('span', {"class": "ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating"})
    

    episode_title_list = []
    for url in episode_title_html:
        episode_title_list.append(url.getText())
    
    episode_title.extend(episode_title_list)
    
    df = pd.DataFrame({
        'title': episode_title
    })

# df.to_csv('test', index=False)

# print(df)

