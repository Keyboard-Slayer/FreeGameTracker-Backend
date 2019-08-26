#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from flask import (
    Flask,
    jsonify,
    render_template
)

app = Flask(__name__)

def init() -> dict:
    modules = {}
    for module in os.listdir("./include"):
        if module.split('.')[-1] == "py" and module != "__init__.py":
            exec("import include.{0} as {0}".format('.'.join(module.split('.')[:-1])))
            modules['.'.join(module.split('.')[:-1])] = eval(f"{'.'.join(module.split('.')[:-1])}")
    return modules

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/')
def api():
    data = [module.get_json() for module in globals()['modules'].values()]
    return jsonify(data)

if __name__ == "__main__":
    globals()['modules'] = init()
    app.run(port=80)
