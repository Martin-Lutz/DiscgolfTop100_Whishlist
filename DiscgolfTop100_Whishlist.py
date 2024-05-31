import pandas as pd
import folium
url = "https://udisc.com/blog/post/100-european-disc-golf-courses-people-most-want-to-play"
import bs4
import requests


class course:
    def __init__(self,name, link, rank):
        self.name = name
        self.link = link
        self.rank = rank
        print(self.link)
        response = requests.get(self.link)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        a = soup.find_all("a", string="Get directions")[0]
        a = a["href"]
        coordinates = a.split("/")[-1].split(",")
        self.lat = float(coordinates[0])
        self.lon = float(coordinates[1])
       
    
    def __str__(self):
        return self.name + " " + self.link + " " + self.rank + " " + str(self.lat) + " " + str(self.lon)


response = requests.get(url)
soup = bs4.BeautifulSoup(response.text, "html.parser")
table = soup.find_all("table")
table = table[1]

#split the table into rows
rows = table.find_all("tr")
courses = []
for row in rows:
    try:
        #get the rank
        rank = row.find_all("td")[0].text
        #get the name
        name = row.find_all("td")[1].text
        #get the link
        link = row.find_all("td")[1].a["href"]
        #if link starts with http, use it, otherwise add the base url
        if not link.startswith("https"):
            link = "https://udisc.com" + link

        courses.append(course(name, link, rank))
    except:
        pass


#create a map with coordinates
m = folium.Map(location=[0, 0], zoom_start=2)
for c in courses:
    folium.Marker([c.lat, c.lon], popup=f"<a href='{c.link}'>{c.name}</a> - Rank: {c.rank}").add_to(m)

m.save("map.html")


