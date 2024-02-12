"""
information tag : First attempt
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
from search import search

WINDOW_TAG1 = "Deep Window"
WINDOW_TAG2 = "Main Window"
TABLE_TAG1 = "Deep Table"
STATE = 0
INPUT_TAG1 = "Input TAG Text"
INPUT_TAG2 = "Input TAG Note"
INPUT_TAG3 = "Input Text"
INPUT_TAG4 = "Input Note"
CURRENT_URL = ''
CURRENT_NOTE = ''
CURRENT_CATEGORY = ''
FILENAME = "tag.csv"
DF = None
TAG = ''

def update_table(df): # pylint: disable=C0103
    """
    update_table: 
    """
    global WINDOW_TAG1, TABLE_TAG1 # pylint: disable=W0602
    dpg.delete_item(TABLE_TAG1, children_only=False)
    with dpg.table(parent=WINDOW_TAG1,
        tag=TABLE_TAG1, label='DataFrame', header_row=False, resizable=False, scrollY=True):
        if df is not None:
            arr = df.to_numpy()
            for i in range(df.shape[1]):
                if i == 0:
                    dpg.add_table_column(label=df.columns[i],
                        width_stretch=True, init_width_or_weight=0.02)
                elif i == 1:
                    dpg.add_table_column(label=df.columns[i],
                        width_stretch=True, init_width_or_weight=0.52)
                else:
                    dpg.add_table_column(label=df.columns[i])
            for i in range(df.shape[0]):
                with dpg.table_row(filter_key=f"{arr[i,1]}"):
                    for j in range(df.shape[1]):
                        if j == 0:
                            dpg.add_checkbox(callback=row_select,
                                user_data=[i, f"{arr[i,1]}", f"{arr[i,2]}"])
                        else:
                            dpg.add_input_text(default_value=f"{arr[i,j]}", width=2000)

def data_save():
    """
    data_save: 
    """
    global DF, FILENAME # pylint: disable=W0602
    DF = DF[['URL','TITLE','NOTE','REF']].copy()
    DF.reset_index(drop=True, inplace=True)
    DF.to_csv(FILENAME, encoding='utf-8-sig')

def data_search():
    global DF, CURRENT_URL, INPUT_TAG1 # pylint: disable=W0602
    keyword = dpg.get_value(INPUT_TAG1)
    result = search(keyword)
    print(result)

    for r in result:
        d = {}
        d['URL'], d['TITLE'], d['NOTE'], d['REF'] = CURRENT_URL, r['title'], r['body'], r['href']
        df = pd.DataFrame([d])
        if DF is None or len(DF) == 0:
            DF = df.copy()
        else:
            DF = pd.concat([DF,df])
    data_save()
    update_table(DF)

def data_paste():
    print('')

def data_add():
    print('')

def data_remove():
    print('')

def row_select(sender, app_data, user_data): # pylint: disable=W0613
    """
    row_select: 
    """
    print('')

def data_tag(sender, app_data, user_data):
    global STATE, WINDOW_TAG1, WINDOW_TAG2, WINDOW_TAG3, WINDOW_TAG4, CURRENT_URL, CURRENT_NOTE, CURRENT_CATEGORY # pylint: disable=W0602
    if STATE == 0:
        STATE = 1
        url = dpg.get_value(INPUT_TAG3)
        note = dpg.get_value(INPUT_TAG4)
        CURRENT_URL, CURRENT_NOTE, CURRENT_CATEGORY = url, note, user_data
        dpg.focus_item(WINDOW_TAG1)
        dpg.set_value(INPUT_TAG1, CURRENT_NOTE)
        # dpg.set_value(INPUT_TAG2, tag)
    else:
        STATE = 0
        dpg.focus_item(WINDOW_TAG2)

def create_deep_window(TAG, SIDE_WIDTH, WIDTH, HEIGHT): # pylint: disable=C0103,R0912
    """
    create_deep_window: 
    """
    global TABLE_TAG1, INPUT_TAG2, DF, FILENAME, CURRENT_URL, CURRENT_CATEGORY # pylint: disable=W0602
    with dpg.window(tag=TAG, pos=[SIDE_WIDTH,0],width=WIDTH-SIDE_WIDTH, no_title_bar=True,
            height=HEIGHT, no_resize=True, no_move=True, no_close=True):
        with dpg.group(horizontal=True):
            dpg.add_button(label='SEARCH', callback=data_search)
            dpg.add_input_text(width=700, tag=INPUT_TAG1)
            dpg.add_input_text(width=200, tag=INPUT_TAG2)
            dpg.add_button(label='PASTE', callback=data_paste)
            dpg.add_button(label='ADD', callback=data_add)
            dpg.add_button(label='REMOVE', callback=data_remove)
            dpg.add_button(label='BACK', callback=data_tag, user_data=CURRENT_CATEGORY)
            dpg.add_text("FILTER")
            dpg.add_input_text(user_data=TABLE_TAG1,
                callback=lambda s, a, u: dpg.set_value(u, dpg.get_value(s)))

        with dpg.table(tag=TABLE_TAG1,
            label='DataFrame', header_row=False, resizable=False, scrollY=True):
            if os.path.exists(FILENAME):
                DF = pd.read_csv(FILENAME, encoding='utf-8-sig')
                DF = DF[DF['URL'].isin([CURRENT_URL])].copy()
                if DF is None or len(DF) == 0:
                    DF = CURRENT_DF = None
                else:
                    DF = DF.fillna('')
                    DF = DF[['URL','TITLE','NOTE','REF']].copy()

            if DF is not None:
                arr = DF.to_numpy()
                for i in range(DF.shape[1]):
                    if i == 0:
                        dpg.add_table_column(label=DF.columns[i],
                            width_stretch=True, init_width_or_weight=0.02)
                    elif i == 1:
                        dpg.add_table_column(label=DF.columns[i],
                            width_stretch=True, init_width_or_weight=0.52)
                    else:
                        dpg.add_table_column(label=DF.columns[i])
                for i in range(DF.shape[0]):
                    with dpg.table_row(filter_key=f"{arr[i,1]}"):
                        for j in range(DF.shape[1]):
                            if j == 0:
                                dpg.add_checkbox(callback=row_select,
                                    user_data=[i, f"{arr[i,1]}", f"{arr[i,2]}"])
                            else:
                                dpg.add_input_text(default_value=f"{arr[i,j]}", width=2000)
