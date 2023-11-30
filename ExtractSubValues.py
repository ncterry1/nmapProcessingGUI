''' extract values from a nested JSON structure in Python, you can use the built-in 
json module to parse the JSON file and then access the nested keys. 
Let's assume you have a JSON file with the following structure:'''

#json
{
    "Key1": {
        "Subkey1": {
            "SubSubKey1": ["value1", "value2", "value3", "value4", "value5"]
        }
    }
}

'''To extract the values under SubSubKey1, you can do the following:

    Read the JSON file.
    Parse the JSON content using json.load() or json.loads().
    Access the nested keys to get to SubSubKey1.

#Here's a sample Python script to achieve this:
'''

#python
import json

# Assuming your JSON data is stored in a file named 'data.json'
with open('data.json', 'r') as file:
    data = json.load(file)

# Accessing the values under SubSubKey1
values = data['Key1']['Subkey1']['SubSubKey1']

print(values)
'''This script will output the list ['value1', 'value2', 'value3', 'value4', 'value5'], 
which are the values under SubSubKey1. Make sure to handle exceptions 
such as KeyError in case some keys are missing in your JSON data.'''


#################
#################
'''This script defines a function find_hosts_with_ostype which takes a dictionary 
(your JSON data) and returns a dictionary mapping hosts to their OS types. 
It then reads a JSON file, processes it, and prints out the host names 
with their corresponding OS types.
python'''

import json

def find_hosts_with_ostype(data):
    hosts_ostype = {}
    
    for host, details in data.items():
        if 'ostype' in details:
            hosts_ostype[host] = details['ostype']
    
    return hosts_ostype

# Assuming your JSON data is stored in a file named 'data.json'
with open('data.json', 'r') as file:
    data = json.load(file)

hosts_ostype = find_hosts_with_ostype(data)

for host, ostype in hosts_ostype.items():
    print(f"Host: {host}, OS Type: {ostype}")

