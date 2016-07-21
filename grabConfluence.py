#!/usr/bin/python

import requests
import getpass
from requests.auth import HTTPBasicAuth
import json

contentUrl = "https://confluence.netconomy.net/rest/api/content/"
spaceUrl = "https://confluence.netconomy.net/rest/api/space/"

user = raw_input("User:")
password = getpass.getpass("Password:")
myAuth = HTTPBasicAuth(user,password);

key = 'SNSLEXT'

rootResponse = requests.get(spaceUrl+key+'/content',auth=myAuth, params={'depth': 'root'}, verify=False)
print(rootResponse.url)
if(rootResponse.ok):
    jData = rootResponse.json()
    rootId = jData['page']['results'][0]['id']
    content = requests.get(contentUrl+str(rootId), auth=myAuth, params={'expand':'body.view'}, verify=False)
    print(content.json()['body']['view']['value'])
else:
    rootResponse.raise_for_status()

