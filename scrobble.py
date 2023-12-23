import managers.lastfm
import managers.icecast
import time
import os
from dotenv import load_dotenv
load_dotenv()

LASTFM_NETWORK = managers.lastfm.get_network()
ICECAST_SOURCE = int(os.getenv("ICECAST_SOURCE"))
UPDATE_FREQUENCY = int(os.getenv("UPDATE_FREQUENCY"))

current_details = ""
# This should really not be a forever loop and should be cleaner later
while True:
  timestamp=int(time.time())
  source = managers.icecast.get_source(ICECAST_SOURCE)
  details = source['title']
  artist, song = details.rsplit(" - ", 1)

  # Clean the artist variable by getting the first artist
  artist = artist.split(",")[0]
  
  # Clean the song variable by removing (Original Mix) if it exists
  song = song.replace("(Original Mix)", "").strip()

  # Update the current now playing every update (songs can be long)
  LASTFM_NETWORK.update_now_playing(
      artist=artist,
      title=song
  )

  # If the song changed, update Last.fm
  if details != current_details:
    print("\nOop, new change!")
    # Update the current now playing
    last_details = current_details
    current_details = details
    print(f"Updated now playing to {artist} - {song}")

    # Scrobble the last song if there was a last song
    if last_details != "":
      last_artist, last_song = last_details.rsplit(" - ", 1)
      last_artist = last_artist.split(",")[0]
      last_song = last_song.replace("(Original Mix)", "").strip()
      managers.lastfm.scrobble(last_artist, last_song, timestamp)
      print(f"Scrobbled {last_artist} - {last_song}")
  time.sleep(UPDATE_FREQUENCY)