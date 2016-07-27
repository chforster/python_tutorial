#!/usr/bin/python

import requests
import getpass
import re
import os
from requests.auth import HTTPBasicAuth
import json
import time

contentUrl = "https://confluence.netconomy.net/rest/api/content/"
spaceUrl = "https://confluence.netconomy.net/rest/api/space/"
mainUrl = "https://confluence.netconomy.net"

user = raw_input("User:")
password = getpass.getpass("Password:")
myAuth = HTTPBasicAuth(user,password);

keys = {'SNSLEXT','SACXT','SWAEXT','CHAEXT'}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

commentCount = 0
pageCount = 0
attachmentCount = 0


def getJson(url, parameters):
    response = requests.get(url, auth=myAuth, params=parameters, verify=False)
    if (response.ok):
        return response.json()
    else:
        response.raise_for_status()

def writeContent(contentid, parentdir, comment=False):
    content = getJson(contentUrl+contentid, {'expand':'body.view'})
    title = urlify(content['title'])
    commentPostfix=""
    directory = os.path.join(parentdir,title)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if (comment):
        commentPostfix="_comment"
        print("\tWrite {}Comment{} {} in directory {}".format(bcolors.BOLD, bcolors.ENDC, bcolors.WARNING + title + bcolors.ENDC, directory))
    else:
        print("Write {} in directory {}".format(bcolors.OKGREEN +title +bcolors.ENDC, parentdir))

    filename=os.path.join(directory, contentid+commentPostfix+".html")
    fobj = open(filename, "w")
    fobj.write(content['body']['view']['value'].encode('utf8'))
    fobj.close()
    return directory

def writeChildren(contentid, directory, comment=False):
    global pageCount
    global attachmentCount
    global commentCount
    if (not comment):
        children = getJson(contentUrl+contentid+'/child/page',{'limit':'500'})
        for child in children['results']:
            childid=child['id']
            parent = writeContent(childid, directory)
            pageCount = pageCount + 1
            writeChildren(childid, parent)
        
        attachments = getJson(contentUrl+contentid+'/child/attachment',{'limit':'500'})
        for attachment in attachments['results']:
            downloadUrl=mainUrl+attachment['_links']['download']
            response=requests.get(downloadUrl, auth=myAuth, params={}, verify=False)
            title = attachment['title'].encode('utf8')
            path=os.path.join(directory, title)
            print("\tWrite {}Attachment{} {} in directory {}".format(bcolors.BOLD, bcolors.ENDC, bcolors.OKBLUE + title + bcolors.ENDC, directory))
            fobj=open(path, "wb")
            fobj.write(response.content)
            fobj.close()
            attachmentCount = attachmentCount + 1

    comments = getJson(contentUrl+contentid+'/child/comment',{'limit':'500'})
    for comment in comments['results']:
        commentid=comment['id']
        parent = writeContent(commentid, directory, True)
        commentCount = commentCount + 1
        writeChildren(commentid, parent, True)

def urlify(s):
     # Remove all non-word characters (everything except numbers and letters)
     s = re.sub(r"[^\w\s]", '', s)
     # Replace all runs of whitespace with undercore 
     s = re.sub(r"\s+", '_', s)
     return s.encode('utf8')

jobInfo = {}
# https://confluence.netconomy.net/rest/api/space/SNSLEXT/content?depth=root
for key in keys:
    start = time.time()
    commentCount = 0
    pageCount = 0
    attachmentCount = 0
    root = getJson(spaceUrl+key+'/content',{'depth': 'root'})
    rootId = str(root['page']['results'][0]['id'])
    directory = writeContent(rootId, os.path.dirname(os.path.realpath(__file__)))
    writeChildren(rootId, directory)
    end = time.time()
    elapsed = end - start
    jobInfo[key] = {"elapsed": elapsed, "commentCount":commentCount, "pageCount":pageCount, "attachmentCount":attachmentCount} 

print("Space\t\tPages\tAttachments\tcomments\tElapsed Time")
for space in jobInfo:
    elapsed = jobINfo[space]["elapsed"]
    print("{}\t\t{}\t\t\t{}\t\t{}\t\t{}min {}sec".format(space, jobInfo[space]["pageCount"], jobInfo[space]["attachmentCount"], jobInfo[space]["commentCount"], int(elapsed)/60, int(elapsed%60)))



