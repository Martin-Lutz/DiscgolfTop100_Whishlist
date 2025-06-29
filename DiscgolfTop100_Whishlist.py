import pandas as pd
import folium
import bs4
import requests

url = "https://udisc.com/blog/post/100-european-disc-golf-courses-people-most-want-to-play"
headers = {"User-Agent": "Mozilla/5.0"}

class Course:
    def __init__(self, name, link, rank):
        self.name = name
        self.link = link
        self.rank = rank
        print(f"Lade: {self.link}")
        
        try:
            response = requests.get(self.link, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Fehler: HTTP {response.status_code}")
                self.lat, self.lon = None, None
                return
        except Exception as e:
            print(f"Verbindungsfehler: {e}")
            self.lat, self.lon = None, None
            return

        soup = bs4.BeautifulSoup(response.text, "html.parser")

        # Suche alle Google Maps Links
        google_links = soup.find_all("a", href=lambda href: href and "google.com/maps/place/" in href)
        if not google_links:
            print("Kein Google Maps-Link gefunden.")
            self.lat, self.lon = None, None
            return

        # Extrahiere Koordinaten
        found = False
        for a in google_links:
            href = a["href"]
            try:
                coords_str = href.split("/place/")[-1]
                lat_str, lon_str = coords_str.split(",")[:2]
                self.lat = float(lat_str)
                self.lon = float(lon_str)
                found = True
                break
            except Exception as e:
                print(f"Fehler beim Parsen von Koordinaten: {e}")
                continue

        if not found:
            print("Koordinaten konnten nicht extrahiert werden.")
            self.lat, self.lon = None, None

    def __str__(self):
        return f"{self.name} {self.link} {self.rank} {self.lat}, {self.lon}"


# Hauptseite mit Kursliste scrapen
response = requests.get(url, headers=headers)
soup = bs4.BeautifulSoup(response.text, "html.parser")
tables = soup.find_all("table")
table = tables[1] if len(tables) > 1 else tables[0]  # Fallback

rows = table.find_all("tr")
courses = []

for row in rows:
    try:
        rank = row.find_all("td")[0].text.strip()
        name = row.find_all("td")[1].text.strip()
        link = row.find_all("td")[1].a["href"]
        if not link.startswith("http"):
            link = "https://udisc.com" + link
        c = Course(name, link, rank)
        if c.lat is not None and c.lon is not None:
            courses.append(c)
    except Exception as e:
        print(f"Überspringe einen Eintrag: {e}")
        continue

# Karte erzeugen
m = folium.Map(location=[52, 10], zoom_start=4)

for c in courses:
    folium.Marker(
        location=[c.lat, c.lon],
        popup=f"<a href='{c.link}' target='_blank'>{c.name}</a> - Rank: {c.rank}"
    ).add_to(m)

m.save("map.html")
print("Karte gespeichert als map.html")
