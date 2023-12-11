# Inspired by this post on LinkedIn: https://www.linkedin.com/feed/update/urn:li:activity:7132835328045830144/
# Used this as a reference: https://abdulrwahab.medium.com/how-to-build-a-python-web-scraper-to-capture-imdb-top-100-movies-908bf9b6bc19

# Importing libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Making a list using the "range" method
# There are 10-seasons for Friends
seasons_list = list(range(1,11))
seasons_list = list(map(str, seasons_list))

# Base url with NO season number at the end
# An empty url list
imdb_url_base = 'https://www.imdb.com/title/tt0108778/episodes/?season='
imdb_url_list = []

# Using a FOR loop to to append the season number to the base url
# Storing all the possible url's into the empty url list
for season in seasons_list:
    imdb_url_list.append(imdb_url_base + season)

# Empty lists for all the info that are requried which will be filled later
episode_title = []
episode_rating = []
episode_air_date = []
episode_description = []

# FOR loop to loop through each url from the list
for url in imdb_url_list:

    imdb_url = url
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
           "Accept-Language": "en-US, en;q=0.5"}

    response = requests.get(imdb_url, headers=headers)
    html_content = response.content

    # Creating the Friends soup 
    friends_soup = BeautifulSoup(html_content, 'html.parser')

    # From the soup it will find the relevant information from the CSS (will require opening the dev console on your browser)
    episode_title_html = friends_soup.find_all('div', {"class": "ipc-title__text"})
    episode_rating_html = friends_soup.find_all('span', {"class": "ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating"})
    episode_air_date_html = friends_soup.find_all('span', {"class": "sc-9115db22-10 fyHWhz"})
    episode_description_html = friends_soup.find_all('div', {"class": "ipc-html-content-inner-div"})
    
    # The data that have been extracted from the soup will be appended to a list
    episode_title_list = []
    for url in episode_title_html:
        episode_title_list.append(url.getText())
    
    episode_rating_list = []
    for url in episode_rating_html:
        episode_rating_list.append(url.getText())

    episode_air_date_list = []
    for url in episode_air_date_html:
        episode_air_date_list.append(url.getText())
    
    episode_description_list = []
    for url in episode_description_html:
        episode_description_list.append(url.getText())
    
    episode_title.extend(episode_title_list)
    episode_rating.extend(episode_rating_list)
    episode_air_date.extend(episode_air_date_list)
    episode_description.extend(episode_description_list)
    
# Putting the info into a dataframe
df = pd.DataFrame({
    'title': episode_title,
    'rating': episode_rating,
    'description': episode_description,
    'air_date': episode_air_date
})

# Writing to a .csv file ready to be cleaned
csv_file = 'friends_initial.csv'
df.to_csv(csv_file, index=False)

print(f'All data has been saved to {csv_file}')

