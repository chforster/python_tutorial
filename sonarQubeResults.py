#!/usr/bin/python

import requests
import getpass
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json

resourcesUrl = "https://ebizqms.swarovski.com/sonar/api/resources"
metrics = ['ncloc','violations','duplicated_lines_density','sqale_index','tests','line_coverage','branch_coverage']

idcol = {"java" : ['com.swarovski.enfinity:swa_cartridges','com.swarovski.enfinity:sco_cartridges','com.swarovski.enfinity:lag_cartridges','com.swarovski.enfinity:sop_cartridges','com.swarovski.enfinity:cha_cartridges'],
"isml" : ['com.swarovski.enfinity:swa_templates','com.swarovski.enfinity:sco_templates','com.swarovski.enfinity:lag_templates','com.swarovski.enfinity:sop_templates','com.swarovski.enfinity:cha_templates'],
"js" : ['com.swarovski.enfinity:swa_js','com.swarovski.enfinity:sco_js','com.swarovski.enfinity:lag_js','com.swarovski.enfinity:sop_js','com.swarovski.enfinity:cha_js']}

keys = {"swa": ['com.swarovski.enfinity:swa_cartridges','com.swarovski.enfinity:swa_templates','com.swarovski.enfinity:swa_js'],
"sco": ['com.swarovski.enfinity:sco_cartridges','com.swarovski.enfinity:sco_templates','com.swarovski.enfinity:sco_js'],
"sop": ['com.swarovski.enfinity:sop_cartridges','com.swarovski.enfinity:sop_templates','com.swarovski.enfinity:sop_js'],
"cha": ['com.swarovski.enfinity:cha_cartridges','com.swarovski.enfinity:cha_templates','com.swarovski.enfinity:cha_js'],
"lag": ['com.swarovski.enfinity:lag_cartridges','com.swarovski.enfinity:lag_templates','com.swarovski.enfinity:lag_js']}

result = {}

user = input("User:")
password = getpass.getpass("Password:")
myAuth = HTTPBasicAuth(user,password)


def getJson(url, parameters):
    response = requests.get(url, auth=myAuth, params=parameters, verify=False)
    if (response.ok):
        return response.json()
    else:
        response.raise_for_status()
		
def formatDate(dateString):
    year = dateString[:4]
    month = dateString[5:7]
    day = dateString[8:10]
    return day + "." + month + "." + year
		
for shopID in keys:
    result[shopID] = {}
    for id in keys[shopID]:
        resources = getJson(resourcesUrl,{'resource': id,'metrics':",".join(metrics)})
        myId = ""
        if (id in idcol["java"]):
            myId = "java"
        if (id in idcol["isml"]):
            myId = "isml"
        if (id in idcol["js"]):
            myId = "js"
        result[shopID][myId] = {}
        for resource in resources:
            version = resource["version"]
            if "version" in result[shopID] and result[shopID]["version"] != version:
                print("Different Version detected!", result[shopID]["version"])
                break
            else:
                result[shopID]["version"] = version
                result[shopID]["date"] = formatDate(resource["date"])
            for msr in resource["msr"]:
                msrKey = msr["key"]
                msrValue = int(msr["val"])
                if msrKey == "line_coverage" or msrKey == "branch_coverage" or msrKey == "duplicated_lines_density":
                    msrValue = msr["frmt_val"]
                    msrValue = msrValue.replace(".",",")
                if msrKey == "sqale_index":
                    msrValue = "%.2f" % (msrValue / 8 / 60)
                    msrValue = msrValue.replace(".",",")
                result[shopID][myId][msrKey] = msrValue

shopsystems = ["swa","sco","lag","sop","cha"]
for shop in shopsystems:
    print(shop)
    print(result[shop]["version"])
    print(result[shop]["date"])
    print(result[shop]["java"]["ncloc"])
    print(result[shop]["isml"]["ncloc"])
    print(result[shop]["js"]["ncloc"])
    print(result[shop]["java"]["violations"])
    print(result[shop]["isml"]["violations"])
    print(result[shop]["js"]["violations"])
    print(result[shop]["java"]["sqale_index"])
    print(result[shop]["isml"]["sqale_index"])
    print(result[shop]["js"]["sqale_index"])
    print(result[shop]["java"]["duplicated_lines_density"])
    print(result[shop]["isml"]["duplicated_lines_density"])
    print(result[shop]["js"]["duplicated_lines_density"])
    print(result[shop]["java"]["tests"])
    print("")
    print(result[shop]["java"]["line_coverage"])
    print(result[shop]["java"]["branch_coverage"])
    print("")
    print("")
    print("")
    input("anykey")

			
			