"""
bookmark category
"""

import os.path
import uuid
import dearpygui.dearpygui as dpg
import pandas as pd
from win import set_category

WINDOW_TAG1 = "Side Window"
TABLE_TAG1 = "Side Table"
INPUT_TAG1 = "Input Category"
INPUT_TAG2 = "Check Box "
FILENAME = "cat.csv"
DF = None

def set_side_category(category):
    """
    set_side_category:
    """
    global INPUT_TAG1 # pylint: disable=W0602
    dpg.set_value(INPUT_TAG1, category)

def row_select(sender, app_data, user_data): # pylint: disable=W0613
    """
    row_select:
    """
    global INPUT_TAG1 # pylint: disable=W0602
    dpg.set_value(INPUT_TAG1, user_data[1])
    set_category(user_data[1])
    for i in range(len(DF)):
        if i == int(user_data[0]):
            dpg.set_value(f'{INPUT_TAG2}{i}', True)
        else:
            dpg.set_value(f'{INPUT_TAG2}{i}', False)

def data_save():
    """
    data_save:
    """
    global DF, FILENAME # pylint: disable=W0602
    DF = DF[['ID','CATEGORY']].copy() # pylint: disable=E1136
    DF.to_csv(FILENAME, encoding='utf-8-sig')

def update_table():
    """
    update_table:
    """
    global WINDOW_TAG1, TABLE_TAG1, DF # pylint: disable=W0602
    dpg.delete_item(TABLE_TAG1, children_only=False)
    with dpg.table(parent=WINDOW_TAG1, tag=TABLE_TAG1,
            label='DataFrame', header_row=False, resizable=False, scrollY=True):
        if DF is not None:
            arr = DF.to_numpy()
            for i in range(DF.shape[1]):
                if i == 0:
                    dpg.add_table_column(label=DF.columns[i],
                        width_stretch=True, init_width_or_weight=0.1)
                else:
                    dpg.add_table_column(label=DF.columns[i])
            for i in range(DF.shape[0]):
                with dpg.table_row(filter_key=f"{arr[i,1]}"):
                    for j in range(DF.shape[1]):
                        if j == 0:
                            dpg.add_checkbox(callback=row_select,
                                user_data=[i, f"{arr[i,1]}"], tag=f'{INPUT_TAG2}{i}')
                        else:
                            dpg.add_input_text(default_value=f"{arr[i,j]}", width=2000)

def category_add():
    """
    category_add:
    """
    global INPUT_TAG1, DF # pylint: disable=W0602
    category = dpg.get_value(INPUT_TAG1)
    d = {}
    d['ID'], d['CATEGORY'] = str(uuid.uuid4()), category
    df = pd.DataFrame([d])
    if DF is None:
        DF = df.copy()
    else:
        if DF[DF['CATEGORY'].str.contains(category)].shape[0] == 0:
            DF = pd.concat([DF,df])
    update_table()
    data_save()

def create_side_window(TAG, SIDE_WIDTH, HEIGHT):# pylint: disable=C0103
    """
    create_side_window:
    """
    with dpg.window(tag=TAG, pos=[0,0], width=SIDE_WIDTH, height=HEIGHT,
            no_title_bar=True, no_resize=True, no_move=True, no_close=True):
        global TABLE_TAG1, INPUT_TAG2, HEADERS, DF, FILENAME # pylint: disable=W0602
        with dpg.group(horizontal=True):
            dpg.add_input_text(width=130, tag=INPUT_TAG1)
            dpg.add_button(label='ADD', callback=category_add)

        with dpg.group(horizontal=True):
            dpg.add_input_text(user_data=TABLE_TAG1,
                callback=lambda s, a, u: dpg.set_value(u, dpg.get_value(s)))
            dpg.add_text("FILTER")

        with dpg.table(tag=TABLE_TAG1, label='DataFrame',
                header_row=False, resizable=False, scrollY=True):
            if os.path.exists(FILENAME):
                DF = pd.read_csv(FILENAME, encoding='utf-8-sig')
                if DF is None or len(DF) == 0:
                    DF = None
                else:
                    DF = DF.fillna('')
                    DF = DF[['ID','CATEGORY']].copy()

            if DF is not None:
                arr = DF.to_numpy()
                for i in range(DF.shape[1]):
                    if i == 0:
                        dpg.add_table_column(label=DF.columns[i],
                            width_stretch=True, init_width_or_weight=0.1)
                    else:
                        dpg.add_table_column(label=DF.columns[i])
                for i in range(DF.shape[0]):
                    with dpg.table_row(filter_key=f"{arr[i,1]}"):
                        for j in range(DF.shape[1]):
                            if j == 0:
                                dpg.add_checkbox(callback=row_select,
                                    user_data=[i, f"{arr[i,1]}"], tag=f'{INPUT_TAG2}{i}')
                            else:
                                dpg.add_input_text(default_value=f"{arr[i,j]}", width=2000)
