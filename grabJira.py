#!/usr/bin/python

import requests
import getpass
import re
import os
from requests.auth import HTTPBasicAuth
import json
import time

searchUrl = "https://jira-new.netconomy.net/rest/api/2/search"
mainUrl = "https://confluence.netconomy.net"

user = input("User:")
password = getpass.getpass("Password:")
myAuth = HTTPBasicAuth(user,password);

keys = {'SNSL','SWA','SAC','SGP','CHA'}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

pageCount = 0
attachmentCount = 0

def getJson(url, parameters):
    response = requests.get(url, auth=myAuth, params=parameters, verify=False)
    if (response.ok):
        return response.json()
    else:
        response.raise_for_status()

def writeIssue(issueNr, issueLink, path):
    print("Write issue {} in directory {}".format(bcolors.OKGREEN +issueNr +bcolors.ENDC, path))

    global attachmentCount
    issueContent = getJson(issueLink,{})
    filename=os.path.join(path, issueNr+".json")
    with open(filename, 'w') as outfile:
        json.dump(issueContent, outfile)
        
    for attachment in issueContent['fields']['attachment']:
        directory = os.path.join(path, issueNr)
        if not os.path.exists(directory):
            os.makedirs(directory)

        downloadUrl=attachment['content']
        response=requests.get(downloadUrl, auth=myAuth, params={}, verify=False)
        fileName = attachment['filename'].encode('utf8')
        attachmentFile=os.path.join(directory, fileName)
        print("\tWrite {}Attachment{} {} in directory {}".format(bcolors.BOLD, bcolors.ENDC, bcolors.OKBLUE + fileName + bcolors.ENDC, directory))
        fobj=open(attachmentFile, "wb")
        fobj.write(response.content)
        fobj.close()
        attachmentCount = attachmentCount + 1

jobInfo = {}
path =  os.path.dirname(os.path.realpath(__file__))
for key in keys:
    start = time.time()
    pageCount = 0
    attachmentCount = 0
    projectPath = os.path.join(path, key)
    if not os.path.exists(projectPath):
        os.makedirs(projectPath)
    # https://jira-new.netconomy.net/rest/api/2/search?jql=project%3DSNSL&maxResults=5000 
    root = getJson(searchUrl,{'jql': 'project=' + key,'maxResults':'5000'})
    for ids in root['issues']:
        issueNr = ids['key']
        issueLink = ids['self']
        writeIssue(issueNr, issueLink, projectPath)
        pageCount = pageCount + 1
    end = time.time()
    elapsed = end - start
    jobInfo[key] = {"elapsed": elapsed, "pageCount":pageCount, "attachmentCount":attachmentCount} 

print("Space\t\tIssues\tAttachments\tElapsed Time")
for space in jobInfo:
    elapsed = jobInfo[space]["elapsed"]
    print("{}\t\t{}\t\t{}\t\t{}min {}sec".format(space, jobInfo[space]["pageCount"], jobInfo[space]["attachmentCount"],int(elapsed)/60, int(elapsed%60)))



