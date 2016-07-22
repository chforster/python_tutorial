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
    print(response.url)
    if (response.ok):
        return response.json()
    else:
        response.raise_for_status()

def writeContent(contentid):
    content = getJson(contentUrl+contentid, {'expand':'body.view'})
    fobj = open(contentid+'.html', "a")
    fobj.write(content['body']['view']['value'].encode('utf8'))
    fobj.close()



# https://confluence.netconomy.net/rest/api/space/SNSLEXT/content?depth=root
root = getJson(spaceUrl+key+'/content',{'depth': 'root'})
rootId = str(root['page']['results'][0]['id'])
writeContent(rootId)
children = getJson(contentUrl+rootId+'/child/page',{})
for child in children['results']:
    writeContent(child['id'])


