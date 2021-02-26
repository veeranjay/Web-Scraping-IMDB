import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd


OutputFolder = 'Output'
headers = {'Accept-Language': 'en-US, en;q=0.5'}
page = requests.get("https://www.imdb.com/search/title/?genres=thriller&title_type=feature&sort=moviemeter,%20asc", headers = headers)
soup = BeautifulSoup(page.content, 'html.parser')

movies = soup.find_all('div', class_='lister-item mode-advanced')

titles = []
release_years = []
metascores = []
runtimes = []
ratings = []
genres = []
votes = []
descriptions = []

urls = []

for i in movies:
    content = i.find('div', class_='lister-item-content')
    image = i.find('div', class_='lister-item-image')

    title = content.h3.a.text
    titles.append(title)

    release_year = content.find('span', class_ = 'lister-item-year').text
    release_years.append(release_year)


    metascore = content.find('span', class_ = 'metascore').text if content.find('span', class_ = 'metascore') != None else "-"  
    metascores.append(metascore[0:3])


    runtime = content.find('span', class_ = 'runtime').text if content.find('span', class_ = 'runtime') != None else "-"  
    runtimes.append(runtime)


    rating = content.find('strong').text if content.find('strong') != None else "-"  
    ratings.append(rating)


    vote = content.find('span', attrs={'name':'nv'}).text if content.find('span',attrs={'name':'nv'}) != None else "-"  
    votes.append(vote)

    description = content.find_all('p', class_='text-muted')[-1].text.lstrip() if content.find_all('p', class_='text-muted') != None else "-"  
    descriptions.append(description)


    genre = content.find('span', class_='genre').text.rstrip().replace('\n', "") if content.find('span', class_='genre') != None else "-"  
    genres.append(genre)

    url = image.a.img['src'] if image != None else '-'
    urls.append(url)


data = []
df = pd.DataFrame({'Title' : titles, 'Year' : release_years, 'Runtime': runtimes, 'Genres':genres,'Description':descriptions,'Metascore':metascores, 'Rating': ratings, 'Votes': votes})
df.to_csv(OutputFolder + '/movies.csv')