"""
pymbm : minimal bookmark manager
"""

import sys
import dearpygui.dearpygui as dpg
import pandas as pd
from side import create_side_window
from win import create_main_window

PROGRAM_W = 1920
PROGRAM_H = 1080
SIDE_PANEL_W = 200
WINDOW_TAG1 = "Main Window"
WINDOW_TAG2 = "Side Window"

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

dpg.create_context()

##########################################################################################################

create_side_window(dpg, WINDOW_TAG2, SIDE_PANEL_W, PROGRAM_W, PROGRAM_H)
create_main_window(dpg, WINDOW_TAG1, SIDE_PANEL_W, PROGRAM_W, PROGRAM_H)

##########################################################################################################

dpg.create_viewport(title='Minimal bookmark manager', x_pos=0, y_pos=0, width=PROGRAM_W, height=PROGRAM_H)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.maximize_viewport()
dpg.start_dearpygui()
dpg.destroy_context()