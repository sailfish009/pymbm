"""
bookmark information
"""

import os.path
import datetime
import webbrowser
import dearpygui.dearpygui as dpg
import pandas as pd
import pyperclip
import re
import requests
from urllib.parse import urlparse

WINDOW_TAG1 = "Main Window"
TABLE_TAG1 = "Main Table"
INPUT_TAG1 = "Input Text"
INPUT_TAG2 = "Input Note"
FILENAME = "data.csv"
DF = None
SELECTED_LIST = []
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def validators(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False

def update_table():
    global WINDOW_TAG1, TABLE_TAG1, DF
    dpg.delete_item(TABLE_TAG1, children_only=False)
    with dpg.table(parent=WINDOW_TAG1, tag=TABLE_TAG1, label='DataFrame', header_row=False, resizable=False, scrollY=True):
        if DF is not None:
            arr = DF.to_numpy()   
            for i in range(DF.shape[1]):
                if i == 0:
                    dpg.add_table_column(label=DF.columns[i], width_stretch=True, init_width_or_weight=0.02)
                elif i == 1:
                    dpg.add_table_column(label=DF.columns[i], width_stretch=True, init_width_or_weight=0.72)
                else:
                    dpg.add_table_column(label=DF.columns[i])
            for i in range(DF.shape[0]):
                with dpg.table_row(filter_key=f"{arr[i,1]}"):
                    for j in range(DF.shape[1]):
                        if j == 0:
                            dpg.add_checkbox(callback=row_select, user_data=[i, f"{arr[i,1]}", f"{arr[i,2]}"])
                        else:
                            dpg.add_input_text(default_value=f"{arr[i,j]}", width=2000)

def data_open():
    global INPUT_TAG1, INPUT_TAG2, HEADERS
    url = dpg.get_value(INPUT_TAG1)
    if validators(url):
        webbrowser.open(url)

def data_add():
    global INPUT_TAG1, DF
    url = dpg.get_value(INPUT_TAG1)
    if validators(url):
        note = dpg.get_value(INPUT_TAG2)
        d = dict()
        d['ID'], d['URL'], d['NOTE'] = datetime.datetime.now(), url, note
        df = pd.DataFrame([d])
        if DF is None:
            DF = df.copy()
        else:
            if DF[DF['URL'].str.contains(url)].shape[0] == 0:
                DF = pd.concat([DF,df])
            else:
                DF[DF['URL'].str.contains(url)]['NOTE'] = note
        update_table()

def data_remove():
    global SELECTED_LIST, DF
    if len(SELECTED_LIST) > 0:
        SELECTED_LIST = [*{*SELECTED_LIST}] 
        DF = DF[~DF['URL'].isin(SELECTED_LIST)].copy()
        DF.sort_values(by='ID', ascending=True, inplace=True)
        update_table()
        SELECTED_LIST = []
        pyperclip.copy('')
        dpg.set_value(INPUT_TAG1, '')
        dpg.set_value(INPUT_TAG2, '')

def data_paste():
    global INPUT_TAG1
    url = pyperclip.paste()
    dpg.set_value(INPUT_TAG1, url)
    if validators(url):
        r = requests.get(url, headers=HEADERS) 
        d = re.search('<\W*title\W*(.*)</title', r.text, re.IGNORECASE)
        if d is not None:
            dpg.set_value(INPUT_TAG2, d.group(1))

def data_save():
    global DF, FILENAME 
    DF = DF[['ID','URL','NOTE']].copy()
    DF.to_csv(FILENAME, encoding='utf-8-sig')

def row_select(sender, app_data, user_data):
    global INPUT_TAG1, INPUT_TAG2, SELECTED_LIST
    dpg.set_value(INPUT_TAG1, user_data[1])
    dpg.set_value(INPUT_TAG2, user_data[2])
    if app_data:
        SELECTED_LIST.append(user_data[1])
    else:
        SELECTED_LIST.remove(user_data[1])

def create_main_window(dpg, TAG, SIDE_WIDTH, WIDTH, HEIGHT):
    global TABLE_TAG1, INPUT_TAG2, HEADERS, DF, FILENAME
    with dpg.window(tag=TAG, pos=[SIDE_WIDTH,0], width=WIDTH-SIDE_WIDTH, no_title_bar=True, height=HEIGHT, no_resize=True, no_move=True, no_close=True):
        url = pyperclip.paste()
        with dpg.group(horizontal=True):
            dpg.add_text("URL")
            dpg.add_input_text(width=700, tag=INPUT_TAG1)
            dpg.add_input_text(width=200, tag=INPUT_TAG2)
            dpg.add_button(label='PASTE', callback=data_paste)
            dpg.add_button(label='OPEN', callback=data_open)
            dpg.add_button(label='ADD', callback=data_add)
            dpg.add_button(label='REMOVE', callback=data_remove)
            dpg.add_button(label='SAVE', callback=data_save)
            dpg.add_text("FILTER")
            dpg.add_input_text(user_data=TABLE_TAG1, callback=lambda s, a, u: dpg.set_value(u, dpg.get_value(s)))

        if validators(url) == False:
            pyperclip.copy('')
        else:
            dpg.set_value(INPUT_TAG1, url)
            r = requests.get(url, headers=HEADERS) 
            d = re.search('<\W*title\W*(.*)</title', r.text, re.IGNORECASE)
            if d is not None:
                dpg.set_value(INPUT_TAG2, d.group(1))

        with dpg.table(tag=TABLE_TAG1, label='DataFrame', header_row=False, resizable=False, scrollY=True):
            if os.path.exists(FILENAME):
                DF = pd.read_csv(FILENAME, encoding='utf-8-sig')
                if DF is None or len(DF) == 0:
                    DF = None
                else:
                    DF = DF.fillna('')
                    DF = DF[['ID','URL','NOTE']].copy()

            if DF is not None:
                arr = DF.to_numpy()   
                for i in range(DF.shape[1]):
                    if i == 0:
                        dpg.add_table_column(label=DF.columns[i], width_stretch=True, init_width_or_weight=0.02)
                    elif i == 1:
                        dpg.add_table_column(label=DF.columns[i], width_stretch=True, init_width_or_weight=0.72)
                    else:
                        dpg.add_table_column(label=DF.columns[i])
                for i in range(DF.shape[0]):
                    with dpg.table_row(filter_key=f"{arr[i,1]}"):
                        for j in range(DF.shape[1]):
                            if j == 0:
                                dpg.add_checkbox(callback=row_select, user_data=[i, f"{arr[i,1]}", f"{arr[i,2]}"])
                            else:
                                dpg.add_input_text(default_value=f"{arr[i,j]}", width=2000)
