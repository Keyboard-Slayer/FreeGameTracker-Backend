#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import (
    Request,
    urlopen
)

import json


def get_siteinfo() -> tuple:
    return ("Ubisoft", "#879fcd")


def get_games() -> list:
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
            expiration = None if game["expirationDate"] is None else game["expirationDate"].split('T')[0]
            free_game.append((game["body"],
                              expiration,
                              game["mediaURL"],
                              game["links"][0]["param"]) + get_siteinfo())

    return free_game
