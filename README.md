# 25.1.2025
## Co je nového a moje myšlenky abych na něco nezapomněl.
- Ošetřil jsem vyjímky, aby se při nějakém erroru u printování playerIDs, počkalo 10 sekund a pak se zkusilo znovu přečíst ID hráče.
- Ohledně toho jaká data používat k simulaci:
  
    - Přemýšel jsem, do toho zakomponovat i únavu hráčů, to bych měřil, podle termínu, kdy se odehrály zápasy. Pokud by tam byl veliký rozdil mezi daty nastavil bych jako defaultní hodnotu týden. K tomu velkému rozdílu může dojít, když se předtím hraje normální liga
    - Převedení názvů týmu na čísla, simulace s tím bude umět lépe pracovat a pak pomocí mapy bych těm číslům zase načetl zpátky názvy týmů nebo udělat One-Hot encoding, ale to úplně nevím co je a vzhledem k tomu, že to trénuju na datech, která obsahují více než 100 týmu, tak bych tam musel přidat 100*2 sloupců :D 
    - Nastavení domácí výhody např. podle čísel 1,0,-1. 1 - týmA hraje zápas na domácím hřišti, tj týmB -1, hraje zápas na venkovním hřišti. 0 - neutrální půda. Z toho budu moct udělat i analýzu toho, jak moc týmům pomáhá domácí výhoda
    - U toho minulého modelu, jsem si stěžoval, že má přesnost 28,9 %. Reálně to možná nemusí být tak špatné, já jsem zkoušel odhadovat přesné výsledky a pokud se ten model trefuje kolem 30 %, tak je to celkem fajn. Možná mám už dost dat, abych zkusil nasimulovat ten turnaj, ale chtěl bych ještě udělat ty úpravy, které jsem zmiňoval výše.

# 19.1.2025
## Co je potřeba a co je hotovo?
- [x] Scrapování playerIDs - tj. jsem schopen si z webovky stáhnout data co potřebuju
- [x] Scrapování dat fotbalistů - pomocí playerIDs si vytáhnu veškerá potřebná data o fotbalistech
- [x] Vytvoření nejlepší jedenáctky každého týmu
- [x] Spočítání průměrného útoku, zálohy, obrany
- [ ] Simulace turnaje
- [ ] Datová analýza
- [ ] Webová aplikace
## Zkouším simulovat skóre zápasů pomoci scikit-learn. 
### Absoultně to nefunguje, toto jsou moje výsledky:
- Mean Absolute Error (MAE): 0.8797931785195938
- Mean Squared Error (MSE): 1.4275321843251088
- R-squared (R²): 0.2890892677737615
## UEFA EURO 2020 Forecast via Nested Zero-Inflated Generalized Poisson Regression
- Hodně vycházím z tohoto PDF, jako ELO bych chtěl používat hodnocení jedenáctky hráčů z "create_best_team.py", no jenže to budu muset nějak normalizovat asi, ještě uvidím co s tím udělám.
- To že se v historických datech bere v potaz lokace a typ turnaje je jednoduché 
```
def set_location_value(row):
    if row["Location"] == row["TeamA"]:
        return 1
    elif row["Location"] == row["TeamB"]:
        return -1
    else:
        return 0


# Funkce pro změnu hodnoty v sloupci 'Tournament'
def set_tournament_value(row):
    if "World Cup" in row["Tournament"]:
        return 4
    elif (
        "European Championship" in row["Tournament"]
        or "Confederation Cup" in row["Tournament"]
        or "Asian Cup" in row["Tournament"]
        or "African Nations Cup" in row["Tournament"]
        or "Southeast Asian Championship" in row["Tournament"]
        or "Gold Cup" in row["Tournament"]
        or "Copa America" in row["Tournament"]
        or "Oceania Nations Cup" in row["Tournament"]
        or "COSAFA Cup" in row["Tournament"]
    ):
        return 3
    elif "qualifier" in row["Tournament"] or "Nations League" in row["Tournament"]:
        return 2.5
    else:
        return 1
```
- To jaké typy turnajů jsou tam jsem moc nekontroloval a nechal to copilota ve vs code doplnit, pak to přečtu pořádně.
- Problém ale je, že taky vůbec netuším jak tam zakomponovat ten útok a obranu, já jsem si v pythonu napsal kód, který mi spočítá průměrné hodnocení útoku/obrany/zálohy, jenže historická data s tím nepočítají a co jsem se díval, tak je nemožné dostat se k datům z minulé hry efootball. Tj zatím mě nenapadá jak to doplnit do toho výsledného modelu. Já si myslím, že v té práci, ze které chci použít ten vzorec použili pro hodnocení útoku a obrany počet vstřelených a počet obdržených gólů, to bych mohl udělat, ale já bych chtěl radši pracovat s daty z té hry.
- kód tu dodám později, protože ho stejně budu muset celý předělat, ta přesnost té simulace je fakt extremně slabá.



nejprve spustit print_playerids, pak player_informations a nakonec create_best_team

# Football Team Optimization Project

This project is designed to analyze and select the best football teams based on player statistics. The scripts and datasets included facilitate data collection, processing, and optimization to create top-performing teams for various nationalities and formations.

## Project Overview

### Key Features

**Data Scraping:**

- Player data is collected from the website pesdb.net using Python scripts.

- Details such as name, nationality, team, rating, positions, and various attributes are extracted.

**Team Optimization:**

- Optimal teams are created based on predefined football formations.

- Player positions, overall ratings, and flexibility in positions are considered.

**Result Export:**

- The best teams and their corresponding data are saved in CSV files for further analysis and sharing.
