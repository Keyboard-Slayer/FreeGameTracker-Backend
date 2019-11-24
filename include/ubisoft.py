#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import (
    Request,
    urlopen
)

import json

def get_name() -> str:
    return "ubisoft"

def get_json() -> str:
    feed_link = ""
    app_id = ""
    free_game = []

    data = urlopen("https://free.ubisoft.com/configuration.js").read()
    for line in data.decode().split('\n'):
        if 'prod' in line and 'https' in line:
            feed_link = ':'.join(line.split(':')[-2:]).replace('\'', '')
        if 'appId' in line:
            app_id = line.split(':')[-1].replace('\'', '')[:-1]

    req = Request(feed_link)
    req.add_header('ubi-localecode', 'en-US')
    req.add_header('ubi-appid', app_id)


    for game in json.loads(urlopen(req).read().decode())['news']:
        
        if game['type'] == "freegame" or game['type'] == "freeweekend":
            free_game.append({"name": game["body"],
                              "expiration": game["expirationDate"],
                              "mediaURL": game["mediaURL"],
                              "publicationDate": game["publicationDate"],
                              "link": game["links"][0]["param"]})
    return free_game
