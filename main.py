import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
from pprint import pprint

CLIENT_ID = "c408a1d9535e4d12a0851ab3b7b26a3f"
CLIENT_SECRET = "e4cb7dc3515a4419a27445bb37ef7055"

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

spty = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="http://example.com",
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = spty.current_user()["id"]
print(user_id)


response = requests.get("https://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(response.text, 'html.parser')

song_names_spans = soup.select(".o-chart-results-list__item h3.c-title")
song_names = [song.getText().strip() for song in song_names_spans]
print(song_names)

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = spty.search(q=f"track:{song} year:{year}", type="track")
    pprint(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify
playlist = spty.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

#Adding songs found into the new playlist
spty.playlist_add_items(playlist_id=playlist["id"], items=song_uris)