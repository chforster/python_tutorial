import json

with open('data.json') as data_file:    
    data = json.load(data_file)

for x in data["maps"]:
    for y in x:	
        print(x[y])

