import os
import requests
import json

import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog


class IEXAPI:

    def __init__(self, tokenConfigPath: str = None):
        if tokenConfigPath == None:
            self.tokenPath = "./iextoken.txt"
        else:
            self.tokenPath = tokenConfigPath
        self.__test_token()

    def get_symbolList(self):
        try:
            self.__get_token()
            symbolList = self.__get_symbol_list(self.token)
            return symbolList
        except:
            self.__ask_token()
            self.__save_token()

    def __test_token(self):
        """
        This function get data from a free api source for testing validation of token.
        """
        while True:
            try:
                self.__get_token()
                url = "https://cloud.iexapis.com/stable/ref-data/iex/symbols?token={}".format(
                    self.token)
                r = requests.get(url)
                result = json.loads(r.text)
                if len(result) > 0:
                    break
            except:
                self.__ask_token()
                self.__save_token()

    def __get_symbol_list(self, token: str):
        url = "https://cloud.iexapis.com/stable/ref-data/symbols?token={}".format(
            token)
        r = requests.get(url)
        result = json.loads(r.text)
        symbols = []
        for item in result:
            symbols.append(item["symbol"].replace(".", "-"))
        return symbols

    def __get_token(self):
        if not os.path.exists(self.tokenPath):
            self.token = ""
            self.__save_token()
        with open(self.tokenPath, 'r') as f:
            self.token = f.read()

    def __save_token(self):
        with open(self.tokenPath, 'w') as f:
            f.write(self.token)

    def __ask_token(self):

        def show_dialog(self):
            root.withdraw()
            self.token = simpledialog.askstring(
                "IEX Cloud Token",
                "Please provide IEX Cloud token:"
            )
            root.destroy()

        root = tk.Tk()
        root.after(1, lambda: show_dialog(self))
        root.mainloop()
