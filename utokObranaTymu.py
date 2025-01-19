import pandas as pd


# Define a function to calculate averages for each nationality
def calculate_averages_by_nationality(data):
    results = []

    for nationality in data["Nationality"].unique():
        # Filter data for each nationality
        nationality_data = data[data["Nationality"] == nationality]

        # Determine defenders and attackers based on position keywords
        defenders = nationality_data[
            nationality_data["Position"].str.contains("Back|Goalkeeper", case=False)
        ]

        midfielders = nationality_data[
            nationality_data["Position"].str.contains("Midfielder", case=False)
        ]

        attackers = nationality_data[
            nationality_data["Position"].str.contains("Forward|Striker", case=False)
        ]

        # Calculate averages
        avg_defense = defenders["Overall Rating"].mean() if not defenders.empty else 0
        avg_midfielders = (
            midfielders["Overall Rating"].mean() if not midfielders.empty else 0
        )
        avg_attack = attackers["Overall Rating"].mean() if not attackers.empty else 0

        results.append(
            {
                "Nationality": nationality,
                "Average Defense": round(avg_defense, 2),
                "Average Midfielders": round(avg_midfielders, 2),
                "Average Attack": round(avg_attack, 2),
            }
        )

    return pd.DataFrame(results)


# Load data
data = pd.read_csv("best_teamsjedenactky.csv")
nationality_averages = calculate_averages_by_nationality(data)
nationality_averages.to_csv("nationality_averages.csv", index=False)
print(nationality_averages)
