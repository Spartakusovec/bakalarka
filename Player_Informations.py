import requests
from bs4 import BeautifulSoup
import csv
import time

players = open("player_ids_w_free_agents_2025_01_06.txt", "r").read().splitlines()
player_info = []
players_info = []
i = 1

for id in players:
    success = False
    while not success:
        try:
            r = requests.get(f"https://pesdb.net/efootball/?id={id}")
            soup = BeautifulSoup(r.content, "html.parser")
            time.sleep(3)

            player_name = (
                soup.find("th", string="Player Name:")
                .find_next_sibling("td")
                .text.strip()
            )

            # Extracting the team name
            team_name = (
                soup.find("th", string="Team Name:")
                .find_next_sibling("td")
                .text.strip()
            )

            # Extracting the nationality
            nationality = (
                soup.find("th", string="Nationality:")
                .find_next_sibling("td")
                .text.strip()
            )

            # Extracting the rating
            rating = (
                soup.find("th", string="Rating:").find_next_sibling("td").text.strip()
            )

            # Extracting the position
            main_position = (
                soup.find("th", string="Position:")
                .find_next_sibling("td")
                .div.text.strip()
            )

            # Extracting all pos1 positions
            pos1_list = [div["title"] for div in soup.find_all("div", class_="pos1")]

            # Extracting all pos2 positions
            pos2_list = [div["title"] for div in soup.find_all("div", class_="pos2")]

            # Extracting the overall rating
            overall_rating = int(
                soup.find("th", string="Overall Rating:")
                .find_next_sibling("td")
                .text.strip()
            )

            # Extracting additional information
            league = (
                soup.find("th", string="League:").find_next_sibling("td").text.strip()
            )
            region = (
                soup.find("th", string="Region:").find_next_sibling("td").text.strip()
            )
            height = int(
                soup.find("th", string="Height:").find_next_sibling("td").text.strip()
            )
            weight = int(
                soup.find("th", string="Weight:").find_next_sibling("td").text.strip()
            )
            age = int(
                soup.find("th", string="Age:").find_next_sibling("td").text.strip()
            )
            foot = soup.find("th", string="Foot:").find_next_sibling("td").text.strip()

            # Extracting attributes
            attributes = [
                "Offensive Awareness",
                "Ball Control",
                "Dribbling",
                "Tight Possession",
                "Low Pass",
                "Lofted Pass",
                "Finishing",
                "Heading",
                "Set Piece Taking",
                "Curl",
                "Defensive Awareness",
                "Tackling",
                "Aggression",
                "Defensive Engagement",
                "Speed",
                "Acceleration",
                "Kicking Power",
                "Jumping",
                "Physical Contact",
                "Balance",
                "Stamina",
                "GK Awareness",
                "GK Catching",
                "GK Parrying",
                "GK Reflexes",
                "GK Reach",
                "Weak Foot Usage",
                "Weak Foot Accuracy",
                "Form",
                "Injury Resistance",
            ]

            player_attributes = {
                attr.lower().replace(" ", "_"): (
                    int(
                        soup.find("th", string=attr + ":")
                        .find_next_sibling("td")
                        .text.strip()
                    )
                    if soup.find("th", string=attr + ":")
                    .find_next_sibling("td")
                    .text.strip()
                    .isdigit()
                    else soup.find("th", string=attr + ":")
                    .find_next_sibling("td")
                    .text.strip()
                )
                for attr in attributes
            }

            # Combining all extracted information into a dictionary
            player_info = {
                "Player Name": player_name,
                "Team Name": team_name,
                "Nationality": nationality,
                "Height": height,
                "Weight": weight,
                "Age": age,
                "Foot": foot,
                "Rating": rating,
                "Primary position": main_position,
                "Secondary positions": pos2_list,
                "Backup positions": pos1_list,
                "Overall Rating": overall_rating,
                "League": league,
                "Region": region,
            }

            # Přidání atributů do player_info
            player_info.update(player_attributes)

            # Append each player's info to the players_info list
            players_info.append(player_info)

            print(f"Player {i} extracted")
            i += 1
            success = True  # Nastavíme success na True, pokud se vše povede

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            print(f"Error occurred: {e}")
            print("Waiting for 10 seconds before retrying...")
            time.sleep(10)  # Počkáme 10 sekund před opakováním

# saving the extracted information to a CSV file
with open(
    "info_with_free_agents_2025_01_06.csv", "w", newline="", encoding="utf-8"
) as file:
    fieldnames = players_info[0].keys() if players_info else []
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for player in players_info:
        writer.writerow(player)
