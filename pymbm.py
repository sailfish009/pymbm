"""
pymbm : minimal bookmark manager
"""

import sys
import dearpygui.dearpygui as dpg
from side import create_side_window, set_side_category, category_add
from win import create_main_window, get_category

PROGRAM_TITLE = 'Minimal bookmark manager'
PROGRAM_W = 1920
PROGRAM_H = 1080
SIDE_PANEL_W = 200
WINDOW_TAG1 = "Main Window"
WINDOW_TAG2 = "Side Window"

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

dpg.create_context()

###################################################################################################

create_side_window(WINDOW_TAG2, SIDE_PANEL_W, PROGRAM_H)
create_main_window(WINDOW_TAG1, SIDE_PANEL_W, PROGRAM_W, PROGRAM_H)
category = get_category()
set_side_category(category)
category_add()

# # custom font : Korean Hangul Font
# with dpg.font_registry():
#     # with dpg.font(".\\NotoSansKR-Medium.ttf", 16) as default_font:
#     # with dpg.font(".\\NotoSerifCJKkr-Medium.otf", 16) as default_font:
#     with dpg.font("C:\\Windows\\Fonts\\Malgun.ttf", 20) as default_font:
#         dpg.add_font_range_hint(dpg.mvFontRangeHint_Korean)
#     dpg.bind_font(default_font)

###################################################################################################

dpg.create_viewport(title=PROGRAM_TITLE, x_pos=0, y_pos=0, width=PROGRAM_W, height=PROGRAM_H)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.maximize_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
