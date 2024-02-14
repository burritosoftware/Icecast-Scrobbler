import requests
import os
from dotenv import load_dotenv
load_dotenv()

def get_status():
    response = requests.get(os.getenv("ICECAST_URL") + "/status-json.xsl")
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        print("Error: Failed to retrieve JSON from URL")
        return None
    
def get_source():
    if os.getenv("ICECAST_MULTI_SOURCE") == 'True':
        return get_status()["icestats"]["source"][int(os.getenv("ICECAST_SOURCE"))]
    else:
        return get_status()["icestats"]["source"]