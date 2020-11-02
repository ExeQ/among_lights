import requests
import json
from settings import PONTS
import time

red = {"on": True,
       "bri": 100,
       "hue": 126,
       "sat": 247,
       "effect": "none",
       "xy": [
           0.6804,
           0.3121
       ],
       "ct": 153
       }

normal = {"on": True,
          "bri": 103,
          "hue": 129,
          "sat": 247,
          "effect": "none",
          "xy": [
              0.5019,
              0.4152
          ],
          "ct": 447
          }


def get_all_group_id(pont):
    lights_url = "http://{}/api/{}/groups".format(pont["ip"], pont["token"])
    r = requests.get(lights_url)
    #return 10
    return int(next((x for x in r.json() if r.json()[x]["name"] == "all"), None))


def alert():
    for pont in PONTS:
        all_group_id = get_all_group_id(pont)
        lights_url = "http://{}/api/{}/groups".format(pont["ip"], pont["token"])
        light_state_url = "{}/{}/action".format(lights_url, str(all_group_id))
        message = json.dumps(red)
        requests.put(light_state_url, data=message)

        for i in range(0, 15):
            r = requests.get(lights_url)
            new_state = not r.json()[str(all_group_id)]["state"]["all_on"]
            message = json.dumps({"on": new_state})
            light_state_url = "{}/{}/action".format(lights_url, str(all_group_id))
            action = requests.put(light_state_url, data=message)
            time.sleep(0.75)

        message = json.dumps(normal)
        light_state_url = "{}/{}/action".format(lights_url, str(all_group_id))
        action = requests.put(light_state_url, data=message)


def sabotage():
    for pont in PONTS:
        all_group_id = get_all_group_id(pont)
        lights_url = "http://{}/api/{}/groups".format(pont["ip"], pont["token"])
        message = json.dumps({"on": False})
        light_state_url = "{}/{}/action".format(lights_url, str(all_group_id))
        action = requests.put(light_state_url, data=message)


def fix():
    for pont in PONTS:
        all_group_id = get_all_group_id(pont)
        lights_url = "http://{}/api/{}/groups".format(pont["ip"], pont["token"])
        message = json.dumps(normal)
        light_state_url = "{}/{}/action".format(lights_url, str(all_group_id))
        action = requests.put(light_state_url, data=message)

