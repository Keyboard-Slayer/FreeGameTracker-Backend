#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from datetime import datetime
from include.database import Database

from flask import (
    Flask,
    jsonify,
    render_template
)

app = Flask(__name__)


def beautify(data: list) -> list:
    result = []

    for game in data:
        result.append({"name": game[1],
                       "expiration": game[2],
                       "mediaURL": game[3],
                       "link": game[4],
                       "source": game[5],
                       "color": game[6]})
    
    return result

def init() -> list:
    day = datetime.today().weekday()
    database = Database()

    if day in [0, 4]: 
        database.fetch_from_web()

    database.check_date()
    data = beautify(database.fetch_data())

    return data


@app.route("/")
def index():
    data = init()
    
    return jsonify(data)

if __name__ == "__main__":
    app.run()