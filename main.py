import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# Request the webpage
url = "https://www.pro-football-reference.com/years/2022/scrimmage.htm"
page = requests.get(url)

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(page.content, "html.parser")

# Get all player codes and names
names = []
players = []
for tr in soup.find_all("tr")[1:]:
    try:
        name = tr.find("td").text
        names.append(name)
        player = tr.find_all("td")[0].find("a")
        players.append(player["href"])
    except:
        pass

print(names)
print(players)


# Function to retrieve rushing & receiving table for each player
def collect_data(name, player):
    player_url = f"https://www.pro-football-reference.com{player}"
    response = requests.get(player_url)
    soup = BeautifulSoup(response.content, "html.parser")
    name = re.sub("[@#$*&+]", "", name, 0, re.IGNORECASE)

    data = []
    try:
        # Find rushing & receiving table
        rushrec = soup.find("table", id="rushing_and_receiving")

        # Get the rows from the table
        rows = rushrec.find_all("tr")[2:]

        # Variables
        print(name)
        for row in rows:
            year = row.find("th").text
            year = re.sub("[@#$*&+]", "", year, 0, re.IGNORECASE)
            try:
                year = int(year)
                temp = []
                for item in row.find_all('td')[0:]:
                    if item.text != "":
                        temp.append(item.text)
                    else:
                        item = "0"
                        temp.append(item)
                pos = temp[2]
                if pos == "FB" or pos == "0":
                    pos = "RB"
                scrim = float(temp[27])
                tot_td = float(temp[28])
                fmbl = float(temp[29])
                rec = float(temp[15])
                g = float(temp[4])
                gs = float(temp[5])

                actual = scrim * 0.1 + tot_td * 6 + fmbl * -2 + rec

                scrim = scrim / g
                tot_td = tot_td / g
                fmbl = fmbl / g
                rec = rec / g
                tgt = float(temp[14]) / g
                att = float(temp[6]) / g
                age = float(temp[0])
                rush_yds = float(temp[7]) / g
                rec_yds = float(temp[16]) / g
                yds_rec = float(temp[17])
                rec_td = float(temp[18]) / g
                catch = re.sub("[%]", "", temp[23], 0, re.IGNORECASE)
                catch = float(catch)
                rush_td = float(temp[8]) / g
                yards_att = float(temp[11])
                touch = float(temp[25]) / g
                yards_touch = float(temp[26])

                c_g = 0
                c_gs = 0
                c_scrim = 0
                c_tot_td = 0
                c_fmbl = 0
                c_rec = 0
                c_tgt = 0
                c_att = 0
                c_rush_yds = 0
                c_rec_yds = 0
                c_yds_rec = 0
                c_rec_td = 0
                c_catch = 0
                c_rush_td = 0
                c_yards_att = 0
                c_touch = 0
                c_yards_touch = 0
                career_avg = []
                if data:
                    for stat in zip(*data):
                        try:
                            career_avg.append(sum(stat) / len(stat))
                        except:
                            pass

                    c_scrim = career_avg[2]
                    c_tot_td = career_avg[3]
                    c_fmbl = career_avg[4]
                    c_rec = career_avg[5]
                    c_tgt = career_avg[6]
                    c_att = career_avg[7]
                    c_rush_yds = career_avg[9]
                    c_rec_yds = career_avg[10]
                    c_yds_rec = career_avg[11]
                    c_rec_td = career_avg[12]
                    c_catch = career_avg[13]
                    c_rush_td = career_avg[14]
                    c_yards_att = career_avg[15]
                    c_touch = career_avg[16]
                    c_yards_touch = career_avg[17]
                    c_g = career_avg[18]
                    c_gs = career_avg[19]

                if pos != "RB" and pos != "WR" and pos != "TE":
                    break
                data.append(
                    [name, year, pos, actual, scrim, tot_td, fmbl, rec, tgt, att, age, rush_yds, rec_yds, yds_rec,
                     rec_td, catch, rush_td, yards_att, touch, yards_touch, g, gs, c_scrim, c_tot_td, c_fmbl, c_rec,
                     c_tgt, c_att, c_rush_yds, c_rec_yds, c_yds_rec, c_rec_td, c_catch, c_rush_td, c_yards_att, c_touch,
                     c_yards_touch, c_g, c_gs])
                print(year)
            except:
                pass

        year = "test"
        career_avg = []
        if data:
            for stat in zip(*data):
                try:
                    career_avg.append(sum(stat) / len(stat))
                except:
                    pass

            c_scrim = career_avg[2]
            c_tot_td = career_avg[3]
            c_fmbl = career_avg[4]
            c_rec = career_avg[5]
            c_tgt = career_avg[6]
            c_att = career_avg[7]
            c_rush_yds = career_avg[9]
            c_rec_yds = career_avg[10]
            c_yds_rec = career_avg[11]
            c_rec_td = career_avg[12]
            c_catch = career_avg[13]
            c_rush_td = career_avg[14]
            c_yards_att = career_avg[15]
            c_touch = career_avg[16]
            c_yards_touch = career_avg[17]
            c_g = career_avg[18]
            c_gs = career_avg[19]

            data.append(
                [name, year, pos, actual, scrim, tot_td, fmbl, rec, tgt, att, age, rush_yds, rec_yds, yds_rec,
                 rec_td, catch, rush_td, yards_att, touch, yards_touch, g, gs, c_scrim, c_tot_td, c_fmbl, c_rec,
                 c_tgt, c_att, c_rush_yds, c_rec_yds, c_yds_rec, c_rec_td, c_catch, c_rush_td, c_yards_att, c_touch,
                 c_yards_touch, c_g, c_gs])
            print(year)
    except:
        try:
            # Find rushing & receiving table
            rushrec = soup.find("table", id="receiving_and_rushing")

            # Get the rows from the table
            rows = rushrec.find_all("tr")[2:-1]

            # Variables
            print(name)
            for row in rows:
                year = row.find("th").text
                year = re.sub("[@#$*&+]", "", year, 0, re.IGNORECASE)
                try:
                    year = int(year)
                    temp = []
                    for item in row.find_all('td')[0:]:
                        if item.text != "":
                            temp.append(item.text)
                        else:
                            item = "0"
                            temp.append(item)
                    pos = temp[2]
                    if pos == "FB" or pos == "0":
                        pos = "WR"
                    scrim = float(temp[27])
                    tot_td = float(temp[28])
                    fmbl = float(temp[29])
                    rec = float(temp[7])
                    g = float(temp[4])
                    gs = float(temp[5])

                    actual = scrim * 0.1 + tot_td * 6 + fmbl * -2 + rec

                    scrim = scrim / g
                    tot_td = tot_td / g
                    fmbl = fmbl / g
                    rec = rec / g
                    tgt = float(temp[6]) / g
                    att = float(temp[18]) / g
                    age = float(temp[0])
                    rush_yds = float(temp[19]) / g
                    rec_yds = float(temp[8]) / g
                    yds_rec = float(temp[9]) / g
                    rec_td = float(temp[10]) / g
                    catch = re.sub("[%]", "", temp[15], 0, re.IGNORECASE)
                    catch = float(catch) / g
                    rush_td = float(temp[20]) / g
                    yards_att = float(temp[23]) / g
                    touch = float(temp[25]) / g
                    yards_touch = float(temp[26]) / g

                    c_g = 0
                    c_gs = 0
                    c_scrim = 0
                    c_tot_td = 0
                    c_fmbl = 0
                    c_rec = 0
                    c_tgt = 0
                    c_att = 0
                    c_rush_yds = 0
                    c_rec_yds = 0
                    c_yds_rec = 0
                    c_rec_td = 0
                    c_catch = 0
                    c_rush_td = 0
                    c_yards_att = 0
                    c_touch = 0
                    c_yards_touch = 0
                    career_avg = []
                    if data:
                        for stat in zip(*data):
                            try:
                                career_avg.append(sum(stat) / len(stat))
                            except:
                                pass

                        c_scrim = career_avg[2]
                        c_tot_td = career_avg[3]
                        c_fmbl = career_avg[4]
                        c_rec = career_avg[5]
                        c_tgt = career_avg[6]
                        c_att = career_avg[7]
                        c_rush_yds = career_avg[9]
                        c_rec_yds = career_avg[10]
                        c_yds_rec = career_avg[11]
                        c_rec_td = career_avg[12]
                        c_catch = career_avg[13]
                        c_rush_td = career_avg[14]
                        c_yards_att = career_avg[15]
                        c_touch = career_avg[16]
                        c_yards_touch = career_avg[17]
                        c_g = career_avg[18]
                        c_gs = career_avg[19]

                    if pos != "RB" and pos != "WR" and pos != "TE":
                        break
                    data.append(
                        [name, year, pos, actual, scrim, tot_td, fmbl, rec, tgt, att, age, rush_yds, rec_yds, yds_rec,
                         rec_td, catch, rush_td, yards_att, touch, yards_touch, g, gs, c_scrim, c_tot_td, c_fmbl, c_rec,
                         c_tgt, c_att, c_rush_yds, c_rec_yds, c_yds_rec, c_rec_td, c_catch, c_rush_td, c_yards_att,
                         c_touch, c_yards_touch, c_g, c_gs])
                    print(year)
                except:
                    pass

            year = "test"
            career_avg = []
            if data:
                for stat in zip(*data):
                    try:
                        career_avg.append(sum(stat) / len(stat))
                    except:
                        pass

                c_scrim = career_avg[2]
                c_tot_td = career_avg[3]
                c_fmbl = career_avg[4]
                c_rec = career_avg[5]
                c_tgt = career_avg[6]
                c_att = career_avg[7]
                c_rush_yds = career_avg[9]
                c_rec_yds = career_avg[10]
                c_yds_rec = career_avg[11]
                c_rec_td = career_avg[12]
                c_catch = career_avg[13]
                c_rush_td = career_avg[14]
                c_yards_att = career_avg[15]
                c_touch = career_avg[16]
                c_yards_touch = career_avg[17]
                c_g = career_avg[18]
                c_gs = career_avg[19]

                data.append(
                    [name, year, pos, actual, scrim, tot_td, fmbl, rec, tgt, att, age, rush_yds, rec_yds, yds_rec,
                     rec_td, catch, rush_td, yards_att, touch, yards_touch, g, gs, c_scrim, c_tot_td, c_fmbl, c_rec,
                     c_tgt, c_att, c_rush_yds, c_rec_yds, c_yds_rec, c_rec_td, c_catch, c_rush_td, c_yards_att, c_touch,
                     c_yards_touch, c_g, c_gs])
                print(year)
        except:
            pass
    df = pd.DataFrame(data,
                      columns=["Player", "Year", "Pos", "Actual", "Scrim", "TOT TD", "Fmbl", "Rec", "Tgt", "Att", "Age",
                               "Rush yds", "Rec yds", "Y/R", "Rec TD", "Catch%", "Rush TD", "Yards/att", "Touch", "Y/T",
                               "G", "GS", "cScrim", "cTOT TD", "cFmbl", "cRec", "cTgt", "cAtt", "cRush yds", "cRec yds",
                               "cY/R", "cRec TD", "cCatch%", "cRush TD", "cY/A", "cTouch", "cY/T", "cG", "cGS"])
    return df


# Combine all player data
df_list = []
for name, player in zip(names, players):
    df = collect_data(name, player)
    if not df.empty:
        df_list.append(df)
    time.sleep(3)

if df_list:
    df = pd.concat(df_list, ignore_index=True)
    train = df[df["Year"] != "test"]
    print(train.head(10))
    train.to_csv("train.csv", index=False)
    test = df[df["Year"] == "test"]
    print(test.head(10))
    test.to_csv("test.csv", index=False)
else:
    print("No data to concatenate")
