from taipy.gui import Gui, navigate
import player_analysis_gui
import global_analysis_gui

pages = {
    "/": "<|menu|lov={page_names}|on_action=menu_action|>",
    "global_home": global_analysis_gui,
    "global_home": global_analysis_gui,
}
page_names = [page for page in pages.keys() if page != "/"]

def menu_action(state, action, payload):
    page = payload["args"][0]
    navigate(state, page)

gui = Gui(pages=pages)
gui.run(port=2425)