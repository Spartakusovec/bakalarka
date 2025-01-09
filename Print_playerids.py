import time
import requests
from bs4 import BeautifulSoup

# Seznam zemí
countries = [
    "Albania",
    "Austria",
    "Belgium",
    "Croatia",
    "Czechia",
    "Denmark",
    "England",
    "France",
    "Germany",
    "Hungary",
    "Italy",
    "Netherlands",
    "Poland",
    "Romania",
    "Scotland",
    "Serbia",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Switzerland",
    "Türkiye",
    "Ukraine",
    "Georgia",
    "Portugal",
]

# Slovník pro ukládání hráčů
players = {}

# Procházení každé země a každé stránky
for country in countries:
    for i in range(1, 3):
        time.sleep(3)
        r = requests.get(f"https://pesdb.net/efootball/?nationality={country}&page={i}")
        soup = BeautifulSoup(r.content, "html.parser")

        rows = soup.find_all("tr")

        # Procházení všech řádků
        for row in rows:
            cells = row.find_all("td")

            if len(cells) > 3:
                player_link = cells[1].find("a")
                team_link = cells[2].find("a")

                if player_link and team_link:
                    player_id = player_link["href"].split("=")[1]
                    player_name = player_link.text.strip()
                    team_name = team_link.text.strip()

                    # Extrakce výšky a váhy
                    height = cells[4].text.strip()
                    weight = cells[5].text.strip()

                    # Klíč je tuple (jméno, výška, váha)
                    key = (player_name, height, weight)

                    # Pokud hráč již existuje v dictionary a má tým, neprovádíme změny
                    if key in players:
                        # Pokud stávající hráč je free agent a nový má tým, nahradíme ho
                        if (
                            players[key]["team"] == "Free Agents"
                            and team_name != "Free Agents"
                        ):
                            players[key] = {"id": player_id, "team": team_name}
                    else:
                        # Uložíme hráče do dictionary
                        players[key] = {"id": player_id, "team": team_name}

# Zápis do souboru pouze s ID hráčů
with open("player_ids_w_free_agents_2025_01_06.txt", "w") as f:
    for info in players.values():
        f.write(f"{info['id']}\n")
