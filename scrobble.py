import managers.lastfm
import managers.icecast
import time
import os
from dotenv import load_dotenv
load_dotenv()

LASTFM_NETWORK = managers.lastfm.get_network()
ICECAST_SOURCE = int(os.getenv("ICECAST_SOURCE"))
UPDATE_FREQUENCY = int(os.getenv("UPDATE_FREQUENCY"))

# This should really not be a forever loop and should be cleaner later
while True:
  timestamp=int(time.time())
  source = managers.icecast.get_source(ICECAST_SOURCE)
  print(source['title'])
  # network.update_now_playing(artist="")
  time.sleep(UPDATE_FREQUENCY)