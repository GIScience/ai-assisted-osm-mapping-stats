# Input/Output configs
INPUTDIR = "../data/"
INPUTFILES = [
    "blds_world-states-2024.geojson"
]  # leave empty to use all files in input dir
PLOTDIR = "../plots/mapping-saturation/"

# OQAPI configs
NO_OF_RETRIES = 3
NO_PARALLEL_REQUESTS = 5
base_url = "https://api.quality.ohsome.org/v1"
endpoint = "/indicators"
indicator = "/mapping-saturation"
OQAPIURLINDICATOR = base_url + endpoint + indicator
TOPIC = "building-count"
HEADERS = {"accept": "application/json"}
