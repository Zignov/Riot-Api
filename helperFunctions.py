import requests
from config import *
import time

#Helper function for getting all player puuids from a given match (matchID -> list(puuids)) 
def extractPlayers(matchId):
    url = (
        f"https://{REGION}.api.riotgames.com"
        f"/lol/match/v5/matches/{matchId}"
    )
    
    
    response = requests.get(url, headers = HEADERS)

    if response.status_code == 429:
        time.sleep(61)
        return extractPlayers(matchId)
    elif response.status_code == 200:
        data = response.json()
        participants = data["metadata"]["participants"]
        return participants
    else:
        print_api_error("extractPlayers", response)
        return None
    
    
    
#helper function for getting acc name from puuid (puuid -> account name)
def getAccount(puuid):
    url = (
        f"https://{REGION}.api.riotgames.com"
        f"/riot/account/v1/accounts/by-puuid/{puuid}"
    )
    
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 429:
        time.sleep(61)
        return getAccount(puuid)
    elif response.status_code == 200:
        data = response.json()
        return data["gameName"]
    else:
        print_api_error("getAccount", response)
        return None

