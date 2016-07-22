#!/usr/bin/python

import requests
import getpass
import re
import os
from requests.auth import HTTPBasicAuth
import json

contentUrl = "https://confluence.netconomy.net/rest/api/content/"
spaceUrl = "https://confluence.netconomy.net/rest/api/space/"
mainUrl = "https://confluence.netconomy.net"

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

def writeContent(contentid, parentdir):
    content = getJson(contentUrl+contentid, {'expand':'body.view'})
    title = urlify(content['title'])
    print("Write {} in directory {}".format(title, parentdir))
    directory = os.path.join(parentdir,title)
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename=os.path.join(directory, contentid+".html")
    fobj = open(filename, "a")
    fobj.write(content['body']['view']['value'].encode('utf8'))
    fobj.close()
    return directory

def writeChildren(contentid, directory):
    children = getJson(contentUrl+contentid+'/child/page',{})
    attachments = getJson(contentUrl+contentid+'/child/attachment',{})
    for child in children['results']:
        childid=child['id']
        parent = writeContent(childid, directory)
        writeChildren(childid, parent)
    for attachment in attachments['results']:
        downloadUrl=mainUrl+attachment['_links']['download']
        response=requests.get(downloadUrl, auth=myAuth, params={}, verify=False)
        path=os.path.join(directory, attachment['title'])
        print("Write Attachment {} in directory {}".format(attachment['title'], directory))
        fobj=open(path, "wb")
        fobj.write(response.content)
        fobj.close()
        

def urlify(s):
     # Remove all non-word characters (everything except numbers and letters)
     s = re.sub(r"[^\w\s]", '', s)
     # Replace all runs of whitespace with undercore 
     s = re.sub(r"\s+", '_', s)
     return s


# https://confluence.netconomy.net/rest/api/space/SNSLEXT/content?depth=root
root = getJson(spaceUrl+key+'/content',{'depth': 'root'})
rootId = str(root['page']['results'][0]['id'])
directory = writeContent(rootId, os.path.dirname(os.path.realpath(__file__)))
writeChildren(rootId, directory)


