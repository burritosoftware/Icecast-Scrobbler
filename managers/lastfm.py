import pylast
import os
from dotenv import load_dotenv
load_dotenv()

def get_network():
  API_KEY = os.getenv("LASTFM_API_KEY")
  API_SECRET = os.getenv("LASTFM_API_SECRET")

  SESSION_KEY_FILE = os.path.join(os.path.curdir, ".lfm-session-key")
  network = pylast.LastFMNetwork(API_KEY, API_SECRET)
  if not os.path.exists(SESSION_KEY_FILE):
      import time
      skg = pylast.SessionKeyGenerator(network)
      url = skg.get_web_auth_url()

      print(f"We're now opening up Last.fm to authorize access.\nIf your web browser didn't open, copy the URL below and paste into a web browser to authorize!\n\n{url}\n")
      import webbrowser

      webbrowser.open(url)

      while True:
          try:
              session_key = skg.get_web_auth_session_key(url)
              with open(SESSION_KEY_FILE, "w") as f:
                  f.write(session_key)
              break
          except pylast.WSError:
              time.sleep(1)
  else:
      session_key = open(SESSION_KEY_FILE).read()

  network.session_key = session_key
  return network

def scrobble(artist, song, timestamp):
  # Make a manual request to Last.fm to scrobble the song using the network.session_key for auth
  params = {
    "artist": artist,
    "track": song,
    "timestamp": timestamp,
    "chosenByUser": 0
  }
  pylast._Request(get_network(), "track.scrobble", params).execute()