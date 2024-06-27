
import json
import os

from dotenv import load_dotenv
import base64
from requests import post, get

load_dotenv()

#calling data from .env file using dotenv
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

## ------ module complete worked ------- ##

## print (client_secret, client_id) ## testing-calling id and secret keys


def auth_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode ("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")


    url = "https://accounts.spotify.com/api/token"

## calling headers -- for API authenetication
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"

    }

    data = {"grant_type": "client_credentials"} ## request authorization data
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

#token = auth_token()
#print(token)

## ----- module 2 -- test complete ---------##

def auth_header(token):
    return{"Authorization": "Bearer " + token}

def search_an_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = auth_header(token)
    query = f"?q= {artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    ##no Name
    if len(json_result) == 0:
        print("Please type a valid name")
        return None
    
    return json_result[0]
    
def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=IN"
    headers = auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result
    

token = auth_token()
result = search_an_artist(token, "Arijit Singh ")
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)
print(songs)