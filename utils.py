# Utility functions for app.py and others.
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

logo = """
        ============
        ============
        ----
        ----
        ----
    ============
        ----
        ----
        ----
============
============
"""

message = f"\nEpo Playground v{config.get('General', 'version')}"

def printlogo(printmesg=False, custommesg=None):
    if printmesg:
        if custommesg is not None:
            return print(logo + message + custommesg)
        return print(logo + message)
    return print(logo)