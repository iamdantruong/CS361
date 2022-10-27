import tornado.ioloop
import tornado.web
import tornado.httpclient
from tornado.ioloop import IOLoop
import json
import requests
from bs4 import BeautifulSoup
import wikipedia

class MainHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def get_url(self, search):
        #search is a string of a city. sends api request to wikivoyage to return URL for wikivoyage page.
        entry = "https://en.wikivoyage.org/w/api.php"
        req = {
            "action": "opensearch",
            "format": "json",
            "search": search,
            "limit": "1",
            "formatversion": "latest"
        }
        response = requests.get(entry, params= req)
        if response.status_code==200:
            data= response.json()
            return(data[3][0])
        else:
            return None

    def get_cities(self, url):
        #url is a wikivoyage url for a country. passes this into a html parser that finds popular tourist cities in the country.
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        cities_object = soup.find_all(class_="fn org listing-name")

        def parse_text(string):
            #helper function to find cities in the wikivoyage page.
            cut = string[38:58]
            for i in range(len(cut)):
                if cut[i]=='"':
                    return cut[0:i]
            else:
                return cut

        cities = []
        for i in range(0,9):
            city = str(cities_object[i])
            new = parse_text(city)
            cities.append(new)
        return(cities)

    def wiki_summary(self, country):
        #passes a country name and pulls the summary from the tourism in the country page.
        search = "Tourism in" + country
        try:
            #page = (wikipedia.page(search))
            #return(page.summary(sentences=5))
            return wikipedia.summary(search, sentences=5)
        except:
            return "Page not found"


    def get(self):
            self.write({'message':'Send a POST request to localhost:5001'})

    async def post(self):
        country_list = self.request.arguments['country']
        country = country_list[0].decode('utf-8')
        summary = self.wiki_summary(country)
        wiki_url = self.get_url(country)
        cities = self.get_cities(wiki_url)
        response_dict = {'summary': summary, 'cities': cities, }
        response = json.dumps(response_dict)
        print(response_dict)
        self.write(response)

def make_app():
    return tornado.web.Application({
        (r"/", MainHandler),
        
    })

if __name__ == "__main__":
    app = make_app()
    app.listen(5001)
    print("Server listening on port 5001, make a POST request to use the Wiki Scraper")
    IOLoop.instance().start()