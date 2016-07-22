#!/usr/bin/python

import requests
import getpass
import re
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
    title = urlify(content['title'])
    fobj = open(contentid+"-"+title+'.html', "a")
    fobj.write(content['body']['view']['value'].encode('utf8'))
    fobj.close()

def writeChildren(contentid):
    children = getJson(contentUrl+contentid+'/child/page',{})
    for child in children['results']:
        childid=child['id']
        writeContent(childid)
        writeChildren(childid)

def urlify(s):
     # Remove all non-word characters (everything except numbers and letters)
     s = re.sub(r"[^\w\s]", '', s)
     # Replace all runs of whitespace with undercore 
     s = re.sub(r"\s+", '_', s)
     return s


# https://confluence.netconomy.net/rest/api/space/SNSLEXT/content?depth=root
root = getJson(spaceUrl+key+'/content',{'depth': 'root'})
rootId = str(root['page']['results'][0]['id'])
writeContent(rootId)
writeChildren(rootId)


