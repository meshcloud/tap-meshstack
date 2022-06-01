import yaml
import json

# this script is a hack to produce semi-legit meshObject tag json schemas for the tap's configuration
# there will probably have to be a better way going forward

with open('tags.json') as d:
  response = json.load(d)

def extract(meshObject:str, type:str):
    tags = [x for x in response["_embedded"]["tags"] if x["type"] == type]
    # print(tags)

    props = dict() 
    for x in tags: 
        tagConfig = {
            'type': x["attributes"]["type"],
        }

        items = x["attributes"].get("items", None)
        if items:
            tagConfig["items"] = items

        props[x["tagKey"]] = tagConfig
    
    return {
        'type': 'object',
        'properties': props,
        # never make any field required, data may be inconsistent
        # 'required': [x["tagKey"] for x in tags if x["attributes"]["mandatory"]]
    }

config = {
    'meshCustomer': extract("meshCustomer", "CUSTOMER"),
    'meshProject': extract("meshProject", "PROJECT"),
    'meshPaymentMethod': extract("meshProject", "PAYMENT_METHOD"),
    # tbd: tenant is the intersection of all three
}


print(yaml.dump(config))