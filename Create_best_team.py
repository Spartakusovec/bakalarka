import pandas as pd

# Load data
data = pd.read_csv("info_with_free_agents_2025_01_06.csv")
data["Position"] = ""

# Define possible formations (20 most common formations)
formations_df = pd.read_csv("formations.csv")
formations = dict(
    zip(formations_df["Formation"], formations_df["Positions"].apply(eval))
)


# Function to check if a player can play a certain position
def can_play(player_positions, position):
    return position in player_positions


# Function to find the best team for a given formation
def find_best_team(formation, players):
    best_team = []
    best_team_positions = []
    filled_positions = []

    # Iteratively select the player with the highest overall rating who can play the next available position in the formation
    for position in formation:
        eligible_players = players[
            players["Secondary positions"].apply(lambda x: can_play(eval(x), position))
            & ~players["Position"].isin(filled_positions)
        ]
        if eligible_players.empty:
            # If there are no eligible players for the position, check backup positions
            backup_players = players[
                players["Backup positions"].apply(lambda x: can_play(eval(x), position))
                & ~players["Position"].isin(filled_positions)
            ]
            if backup_players.empty:
                # If there are no eligible players for the position in backup positions, skip it
                continue
            best_player = backup_players.loc[
                backup_players["Overall Rating"].idxmax()
            ].copy()
            best_player["Overall Rating"] -= 1
        else:
            best_player = eligible_players.loc[
                eligible_players["Overall Rating"].idxmax()
            ]
        best_team.append(best_player)
        best_team_positions.append(position)
        filled_positions.append(position)
        players = players.drop(best_player.name)

    best_team_df = pd.concat(best_team, axis=1).T
    best_team_df["Position"] = best_team_positions
    best_team_rating = best_team_df["Overall Rating"].sum()

    return best_team_df, best_team_rating


# Finding the best formation and team for each nationality
best_teams = {}

for nationality in data["Nationality"].unique():
    nationality_data = data[data["Nationality"] == nationality].copy()
    nationality_data.loc[:, "Position"] = ""

    best_formation = None
    best_team = None
    best_team_rating = 0

    for formation_name, formation_positions in formations.items():
        team, rating = find_best_team(formation_positions, nationality_data)
        if rating > best_team_rating:
            best_team_rating = rating
            best_team = team
            best_formation = formation_name

    best_teams[nationality] = (
        best_team[["Player Name", "Nationality", "Position", "Overall Rating"]],
        best_team_rating,
        best_formation,
    )

# Printing the best team for each nationality, the sum of their overall ratings, and the formation that was chosen
for nationality, (team, rating, formation) in best_teams.items():
    print(f"Best team for {nationality} with formation {formation}:")
    print(team)
    print(f"Sum of overall ratings: {rating}")
    print()

# Save the best teams to a CSV file

with open("best_teamsjedenactky.csv", "w") as f:
    f.write("Player Name,Nationality,Position,Overall Rating, Formation\n")
    for nationality, (team, rating, formation) in best_teams.items():
        team["Nationality"] = nationality
        team["Formation"] = formation
        team.to_csv(f, mode="a", header=False, index=False)

# save nationality and formation to a CSV file
nationality_formation_df = pd.DataFrame(columns=["Nationality", "Formation"])

for nationality, (team, rating, formation) in best_teams.items():
    new_row = pd.DataFrame({"Nationality": [nationality], "Formation": [formation]})
    nationality_formation_df = pd.concat(
        [nationality_formation_df, new_row], ignore_index=True
    )

# Writing the nationality and formation to a CSV file
nationality_formation_df.to_csv("narodnostaformace_2025_01_06.csv", index=False)
