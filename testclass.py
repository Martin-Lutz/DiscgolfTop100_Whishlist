import requests
import bs4

class Course:
    def __init__(self, name, link, rank):
        self.name = name
        self.link = link
        self.rank = rank

        print(f"Rufe Kursseite auf: {self.link}")
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(self.link, headers=headers, timeout=10)
        except Exception as e:
            print(f"Fehler beim Laden der Seite: {e}")
            self.lat, self.lon = None, None
            return

        if response.status_code != 200:
            print(f"Fehler: HTTP {response.status_code}")
            self.lat, self.lon = None, None
            return

        soup = bs4.BeautifulSoup(response.text, "html.parser")

        # Suche alle <a>-Tags mit Google Maps-Koordinatenlink
        google_links = soup.find_all("a", href=lambda href: href and "google.com/maps/place/" in href)
        if not google_links:
            print("Kein Google Maps-Link gefunden.")
            self.lat, self.lon = None, None
            return

        found_coords = False
        for a in google_links:
            href = a["href"]
            print(f"Gefundener Maps-Link: {href}")
            try:
                # Extrahiere Koordinaten aus URL
                coords_str = href.split("/place/")[-1]
                lat_str, lon_str = coords_str.split(",")[:2]
                self.lat = float(lat_str)
                self.lon = float(lon_str)
                found_coords = True
                print(f"Koordinaten extrahiert: {self.lat}, {self.lon}")
                break
            except Exception as e:
                print(f"Fehler beim Parsen: {e}")
                continue

        if not found_coords:
            print("Keine gültigen Koordinaten gefunden.")
            self.lat, self.lon = None, None

    def __str__(self):
        return f"{self.name} (Rang {self.rank}): {self.lat}, {self.lon}"

# 🔗 Test mit Kurs-Link
test_name = "Test Course"
test_rank = "1"
test_link = "https://app.udisc.com/applink/course/24578"

test_course = Course(test_name, test_link, test_rank)
print(test_course)
