import os
import csv
import requests
from datetime import date
from data.toplist_data import toplists


# Fetch API token
token_resp = requests.post(
    url="https://accounts.spotify.com/api/token",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data=f"grant_type=client_credentials&client_id={os.getenv('CLIENT_ID')}&client_secret={os.getenv('CLIENT_SECRET')}",
)

if token_resp.status_code == 200:
    token_data = token_resp.json()
    token = token_data["access_token"]
else:
    print(f"Error fetching token: {token_resp.reason}")
    exit()


# Generic Spotify GET request
def spotify_get(url, base=False):
    url = url if base else f"https://api.spotify.com/v1/{url}"

    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})

    if resp.status_code == 200:
        return resp.json()
    print(f"Error making request to {url}: {resp}")
    exit()


# Generate CSV files
top_artists = set()
with open(f'../data/country_artists-{date.today()}.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Country', 'Sex Ratio', 'GDP per Capita', 'Unique Top Artists'])

    for country, playlist_id in toplists.items():
        playlist = spotify_get(f"playlists/{playlist_id}")
        tracks = spotify_get(playlist["tracks"]["href"], base=True)["items"]
        country_artists = set()
        for track in tracks:
            country_artists |= set([artist["name"] for artist in track["track"]["artists"]])
        writer.writerow([country, '', '', country_artists])
        print(country, "\n", country_artists, "\n")
        top_artists |= set(country_artists)

with open(f'../data/top_artists-{date.today()}.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Artist', 'Sex'])
    for artist in top_artists:
        writer.writerow([artist, ''])
    print(top_artists)
