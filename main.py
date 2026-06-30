import json
import requests
from urllib.parse import quote
from helperFunctions import *
from config import *
import time
from FriendsGraph import *

#Simple function for getting player Puuids (name, tagline -> puuid)
def getPuuid(game_name, tag_line):
    
    url = (
    f"https://{REGION}.api.riotgames.com"
    f"/riot/account/v1/accounts/by-riot-id/"
    f"{quote(game_name)}/{quote(tag_line)}"
    )
    
    
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        #print("PUUID:", data["puuid"])
        #print("Game Name:", data["gameName"])
        #print("Tag Line:", data["tagLine"])
        return data["puuid"]
    else:
        print_api_error("getPuuid", response)
        
        
        
#Simple function for getting player's match history IDs (puuid, count (def: 20) -> list of game IDs)  
def getMatchHistory(puuid, count = 20):
    
    url = (
        f"https://{REGION}.api.riotgames.com"
        f"/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    )
    
    
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        #print("Game IDs:", data)
        return data
    else:
        print_api_error("getMatchHistory", response)
        
        
        

    
        
        
        
#Function for getting data for a player in a given match for every minute (matchId, puuid -> frames(time, gold, level, pos))
def playersGold(matchId, puuid):
    url = (
        f"https://{REGION}.api.riotgames.com"
        f"/lol/match/v5/matches/{matchId}/timeline"
    )

    times = []
    gold_over_time = []
    
    response = requests.get(url, headers = HEADERS)
     
    if response.status_code == 200:
        data = response.json()
        participants = data["metadata"]["participants"]
        

        
        for i in range(len(participants)):
            #print(participants[i])
            if puuid == participants[i]:
                player = i
                break
            else:
                player = -1
                
                
        if player == -1:
            print("error, player not found")
            return data
        
        participant_id = player + 1
        
        frames = data["info"]["frames"]
        
        for frame in frames:
            timestamp = frame["timestamp"]
            player_frame = frame["participantFrames"][str(participant_id)]
            gold = player_frame["totalGold"]
            
            #print("Timestamp:", timestamp)
            times.append(int(timestamp/100000))
            
            #print("Gold:", gold)
            gold_over_time.append(gold)
            
            #print("Level:", player_frame["level"])
            #print("Position:", player_frame.get("position"))
            #print()
              
        #print(times)
        return gold_over_time, times

    else:
        print_api_error("Timeline", response)
        return 0,0
    
    
    
    
def buildingPlayerBase(puuid, count = 10, min = 2):
    
    gamesList = getMatchHistory(puuid, count)
    playerCounts = {}
    
    for game in gamesList:
        players = extractPlayers(game)
        
        
        for player in players:
            #if player == puuid:
                #continue
            
            playerCounts[player] = playerCounts.get(player, 0) + 1
                
                
    sorted_counts = sorted(
        playerCounts.items(),
        key=lambda item: item[1],
        reverse=True
    )
    
    filtered = [(player, count) for player, count in sorted_counts if count >= min]
    
    '''for player, count in sorted_counts:
        
        if count >= 2:
            
            
            
            #print(player, count)
            print(getAccount(player), count)
            time.sleep(0.5)'''
    
    #print (filtered)
    return filtered

        
        
    

        
        
if __name__ == "__main__":
    
    #print("test")
    #Puuid = getPuuid("main", "talon")
    #Puuid = getPuuid("Ektrik", "bruh") 
    Puuid = getPuuid("LivelyHarsh", "3145")
    match = getMatchHistory(Puuid, 1)[0]
    
    
    print(match)
    data = getTimeline(match)
    
    with open("example_timeline.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent = 4)
    
    #buildingPlayerBase(Puuid, 30)
    
    #connections = buildingPlayerBase(Puuid, 100, 2)
    #drawFriendsGraph(Puuid, connections)
    


    
    #playersTimeline("EUN1_3968150250", Puuid)
    
    
    