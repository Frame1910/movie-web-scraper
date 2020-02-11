import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.grandcinemas.com.au/Page/Sessions"

class Bot():
    def __init__(self, url):
        self.URL = url
        r = requests.get(self.URL)
        self.soup = BeautifulSoup(r.content, 'html5lib')
        self.movie_sections = self.soup.find('div', attrs={'id' : 'sessionsDiv'})
    
    def getCurrentlyShowing(self):
        movie_names = []
        print("Currently Showing Films written to: movie_names.txt")
        for movie in self.movie_sections.findAll('span', attrs= {'class':'moviename'}):
            movie_names.append(movie.text)

        with open("movie_names.txt", "w+") as f:
            json.dump(movie_names, f, indent=4)
    
    def writeTo(self, data):
        with open("movie_names.txt", "a") as f:
            json.dump(data, f, indent=4)
    
    def getSessionTimes(self):
        open("movie_names.txt", "w").close()
        for movie in self.movie_sections.findAll('div', attrs={'class' : 'session-film Z zAll zTD zTM zTW fAll'}):
            movie_info = {}
            movie_info["title"] = movie.find('span', attrs={'class' : 'moviename'}).text
            session_sections = self.soup.find('div', attrs={'class' : 'session-film Z zAll zTD zTM zTW fAll'})
            session_times = []
            for session in session_sections.findAll('st', attrs={'class' : 'sesstime'}):
                session_times.append(session.text.strip())
            movie_info["times"] = session_times
            self.writeTo(movie_info)
    

bot = Bot(URL)
bot.getSessionTimes()