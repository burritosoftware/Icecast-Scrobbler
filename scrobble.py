import pylast
import managers.lastfm
import managers.icecast
import time
import os
import re
from dotenv import load_dotenv
load_dotenv()

LASTFM_NETWORK = managers.lastfm.get_network()
UPDATE_FREQUENCY = int(os.getenv("UPDATE_FREQUENCY"))

current_details = {}
last_details = {}

# This should really not be a forever loop and should be cleaner later
while True:
  # Get the current song and associated details
  source = managers.icecast.get_source()
  details = source['title']
   # Check for both " - " and " -- " when splitting
  if " -- " in details:
    artist, song = details.rsplit(" -- ", 1)
  else:
    artist, song = details.rsplit(" - ", 1)
  artist = artist.split(",")[0]
  
  # Use provided regex, if none provided use the current FNT regex
  pattern = os.getenv("TAG_REGEX", r"\(Original Mix\)|\[Explicit\]|\[FNT.*?Edit\]")

  # Remove matching substrings
  song = re.sub(pattern, "", song).strip()
  
  current_details['artist'] = artist
  current_details['song'] = song
  
  if 'album' in current_details:
    if current_details['album'] != "icecast-scrobbler.albumnotfound":
      LASTFM_NETWORK.update_now_playing(
          artist=artist,
          title=song,
          album=current_details['album']
      )
    else:
      LASTFM_NETWORK.update_now_playing(
          artist=artist,
          title=song
      )

  # If the song changed, update Last.fm
  if last_details != current_details:
    # Update the current now playing
    print(f"Updated now playing: {artist} - {song}")

    # Update the current now playing every update (songs can be long) (only if album key does not exist and isn't pylast.WSError)
    try:
      current_details['album'] = LASTFM_NETWORK.get_track(artist=artist, title=song).get_album().get_title()
      print(f"Retrieved album for {song}: {current_details['album']}")
    except:
      current_details['album'] = "icecast-scrobbler.albumnotfound"
      print(f"Couldn't find album: {song}")

    # Scrobble the last song if there was a last song
    if last_details != {}:
      timestamp=int(time.time())
      managers.lastfm.scrobble(artist=last_details['artist'], song=last_details['song'], timestamp=timestamp)
      print(f"Scrobbled: {last_details['artist']} - {last_details['song']}")

    last_details = current_details.copy()
    print("Finished updating\n")

  time.sleep(UPDATE_FREQUENCY)