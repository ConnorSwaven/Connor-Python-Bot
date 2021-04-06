import os
import random
from googleapiclient.discovery import build

def get_meme():

    cxvalue = os.getenv('REDDITKEYFORSTUFF')
    

    service = build("customsearch", "v1",
               developerKey=os.getenv('GOOGLEAPIKEY'))
    
    res = service.cse().list(
         q='meme', #'lectures',
         cx=cxvalue,
         searchType='image',
         rights='',
       ).execute()

    urls = [item['link'] for item in res['items']]
    print(urls)
    return random.choice(urls)