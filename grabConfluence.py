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


def getJson(url, parameters):
    response = requests.get(url, auth=myAuth, params=parameters, verify=False)
    if (response.ok):
        return response.json()
    else:
        response.raise_for_status()



# https://confluence.netconomy.net/rest/api/space/SNSLEXT/content?depth=root
root = getJson(spaceUrl+key+'/content',{'depth': 'root'})
rootId = root['page']['results'][0]['id']

# https://confluence.netconomy.net/rest/api/content/80746397?expand=body.view
content = getJson(contentUrl+str(rootId), {'expand':'body.view'})
print(content['body']['view']['value'])
