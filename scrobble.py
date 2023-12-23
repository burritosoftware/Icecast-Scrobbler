import pylast
import managers.lastfm
import managers.icecast
import time
import os
from dotenv import load_dotenv
load_dotenv()

LASTFM_NETWORK = managers.lastfm.get_network()
ICECAST_SOURCE = int(os.getenv("ICECAST_SOURCE"))
UPDATE_FREQUENCY = int(os.getenv("UPDATE_FREQUENCY"))

current_details = {}
last_details = {}

# This should really not be a forever loop and should be cleaner later
while True:
  # Get the current song and associated details
  source = managers.icecast.get_source(ICECAST_SOURCE)
  details = source['title']
  artist, song = details.rsplit(" - ", 1)
  artist = artist.split(",")[0]
  remove_tags = ["(Original Mix)", "[FNT Edit]"]
  for tag in remove_tags:
    song = song.replace(tag, "").strip()
  
  current_details['artist'] = artist
  current_details['song'] = song
  
  # Update the current now playing every update (songs can be long) (only if album key does not exist and isn't pylast.WSError)
  if 'album' not in current_details:
    try:
      current_details['album'] = LASTFM_NETWORK.get_track(artist=artist, title=song).get_album().get_title()
      print(f"Retrieved album for {song}: {current_details['album']}")
    except:
      current_details['album'] = "icecast-scrobbler.albumnotfound"
      print(f"Couldn't find album: {song}")

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

    # Scrobble the last song if there was a last song
    if last_details != {}:
      timestamp=int(time.time())
      managers.lastfm.scrobble(artist=last_details['artist'], song=last_details['song'], timestamp=timestamp)
      print(f"Scrobbled: {last_details['artist']} - {last_details['song']}")

    last_details = current_details
    print()
  
  time.sleep(UPDATE_FREQUENCY)