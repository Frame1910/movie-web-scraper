import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.grandcinemas.com.au/Page/Sessions"


db = []

r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib')
movie_group = soup.find('div', attrs={'id' : 'sessionsDiv'}) # Container of all movies on page
movie_list = movie_group.findAll('div', attrs={'class': 'session-film'}) # Array of indivdual movies + info

for movie in movie_list:
    movie_info = {} # Contains movie name and session_info dict
    title = movie.find('h5').text
    movie_info["title"] = title.strip()
    session_times_table = movie.find('table')
    days = session_times_table.findAll('tr', attrs={'class' : 'Z zAll zTD zTW fAll'})
    session_info = {} # Contains dates with repective times of sessions ***belongs inside movie_info***
    session_days = []
    day_info = {}
    for day in days:
        date = day.find('h4').text
        day_info["date"] = date.strip()
        times = day.findAll('st', attrs={'class' : 'sesstime'})
        session_times = []
        for time in times:
            session_times.append(time.find('a').text.strip())
        day_info["times"] = session_times
        session_days.append(day_info)
        session_info["days"] = session_days

    movie_info["sessions"] = session_info
    db.append(movie_info)

with open('test.txt', 'w+') as f:
    json.dump(db, f, indent=4)