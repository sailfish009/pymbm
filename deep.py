"""
information tag
"""

import os.path
import datetime
import re
from urllib.parse import urlparse
import webbrowser
import dearpygui.dearpygui as dpg
import pandas as pd
import pyperclip
import requests

WINDOW_TAG1 = "Deep Window"

def create_deep_window(TAG, SIDE_WIDTH, WIDTH, HEIGHT): # pylint: disable=C0103,R0912
    """
    create_deep_window: 
    """
    with dpg.window(tag=TAG, pos=[SIDE_WIDTH,0],width=WIDTH-SIDE_WIDTH, no_title_bar=True,
            height=HEIGHT, no_resize=True, no_move=True, no_close=True):
        print('TODO: Something that might help ')