import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import datetime

today = datetime.datetime.today()
#print(datetime.datetime.strftime(today,'%m/%d/%Y'))

date = datetime.datetime.strftime(today,'%m/%d/%Y')

page = requests.get(f'https://www.yallakora.com/match-center?date={date}')

def main(page):    
    src = page.content
    soup = BeautifulSoup(src, 'lxml')
    details = []
    
    champs = soup.find_all('div', {'class':'matchCard'}) ##2783 matchCard matchesList
    
    def get_info(champs):
        champ_title = champs.contents[1].find('h2').text.strip()
        all_games = champs.contents[3].find_all('li')
        num_of_game = len(all_games)
        
        #print(num_of_game)
    ### 
        for i in range(num_of_game):
            # get teams nmaes
            teamA = all_games[i].find('div',{'class':'teamA'}).text.strip()
            teamB = all_games[i].find('div',{'class':'teamB'}).text.strip()
            
            # get score
            game_result = all_games[i].find('div', {'class':'MResult'}).find_all('span', {'class':'score'})
            score = f"{game_result[0].text.strip()} - {game_result[1].text.strip()}"
            
            #get game time 
            game_time = all_games[i].find('div', {'class':'MResult'}).find('span', {'class':'time'}).text.strip()
            
            #add info to details[]
            details.append({"Champion title":champ_title, "first team":teamA, "game result":score, "second team":teamB, "game time":game_time})
               
    ###
    for i in range(len(champs)):
        get_info(champs[i])
        
    keys = details[0].keys()
    
    with open ("yallakora.csv", "w", encoding="utf-8") as file:
        dictw = csv.DictWriter(file, keys)
        dictw.writeheader()
        dictw.writerows(details)

main(page)