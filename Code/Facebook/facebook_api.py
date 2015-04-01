# This file contains some essential functions for mining data from Facebook
import requests
import sqlite3
import os
from datetime import datetime
import facebook
import json

# A helper function to pretty-print Python objects as JSON
def pretty_print(o): 
        print json.dumps(o, indent=1)


