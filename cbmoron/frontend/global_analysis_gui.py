from taipy.gui import Gui,notify
import taipy as tp
import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc, Wedge
############################3
from dotenv import load_dotenv
import os

import pandas as pd
import io


with tgb.Page() as global_home:
    tgb.text("Sales Insights", class_name="h1")



