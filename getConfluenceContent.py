#!/usr/bin/python

import requests
import getpass
from requests.auth import HTTPBasicAuth
import json

contentUrl = "https://confluence.netconomy.net/rest/api/content"
user = raw_input("User:")
password = getpass.getpass("Password:")
myAuth = HTTPBasicAuth(user,password);
key = 'SNSLEXT'

myResponse = requests.get(contentUrl,auth=myAuth, params={'spaceKey': key, 'limit': '1000'}, verify=False)

# For successful API call, response code will be 200 (OK)
if(myResponse.ok):

    jData = myResponse.json()

    print("The response contains {0} properties".format(len(jData)))
    print("\n")
    for key in jData['results']:
        print(key['title'] )
else:
    myResponse.raise_for_status()
