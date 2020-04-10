import requests,json,os.path
from Elastic_Search import ElasticSearch

# We do not need an API Key since we are not doing many
# requests to download the file. 
PHISHTANK_URL = 'http://data.phishtank.com/data/online-valid.json'
FILE_NAME     = 'online-valid.json'

def save_file(content):
    with open(FILE_NAME, 'w') as f:
        json.dump(content, f)

def read_from_disk():
    with open(FILE_NAME) as f:
        return json.load(f)

# Downloads and saves the file
def download_and_save():
    r       = requests.get(PHISHTANK_URL)
    data    = r.json()
    save_file(data)

# fetch Phishtank phishes
def get_phishtank_data():
    if not os.path.exists(FILE_NAME):
        download_and_save()
    return read_from_disk()

# parses Phishtank phishes
def import_phishtank_phishes_to_elk():
    print('Downloading Phishtank dataset')
    
    phishes          = get_phishtank_data()
    
    # Getting the size of the dataset 

    phishes_length   = len(phishes)

    print(f'Parsing {phishes_length} Phishes')
    
    phish_index  = ElasticSearch('phishtank').delete_index().create_index()

    phish_index.add_bulk(phishes)
    
    print(f'{phishes_length} Phishtank Phishes imported to ELK')

import_phishtank_phishes_to_elk()