#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3

from datetime import datetime


class Database:
    def __init__(self):
        have2create = os.path.isfile("../game.db")
        
        self.conn = sqlite3.connect("game.db")
        self.cur = self.conn.cursor()
        
        if have2create:
            self.create_db()


    def create_db(self):
        self.cur.execute("CREATE TABLE games (id INTEGER PRIMARY KEY, name TEXT, exp TEXT, media TEXT, link TEXT)")
        self.conn.commit()

    

    def fetch_data(self) -> list:
        self.cur.execute("SELECT * FROM games")
        return self.cur.fetchall()


    def check_date(self):
        db = self.fetch_data()

        for game in db:
            date_game_fromdb = game[2]

            if date_game_fromdb is not None:
                game_year, game_month, game_day = game[2].split('-')
                game_realdate = datetime(int(game_year), int(game_month), int(game_day))
                today = datetime.now()


                if today > game_realdate:
                    self.cur.execute("DELETE FROM games WHERE id = ?", (game[0], ))
        
        self.conn.commit()
    

    def fetch_from_web(self):
        games = []

        db = self.fetch_data()

        for module in os.listdir("./include"):
            if module.split('.')[-1] == "py" and module not in ["database.py", "__init__.py"]:
                exec("import include.{0} as {0}".format('.'.join(module.split('.')[:-1])))
                
                module = eval(f"{'.'.join(module.split('.')[:-1])}")
                games += module.get_games()
                
                del module
        
        for game in games:
            if game[-1] not in [game[-1] for game in db]:
                self.cur.execute("INSERT INTO games VALUES (NULL, ?, ?, ?, ?)", game)
            
        self.conn.commit()


