import pandas as pd
from taipy.gui import Gui

# import matplotlib.pyplot as plt

# Define allowed leagues
ALLOWED_LEAGUES = {"central", "pacific"}

# define initial filters
league = "central"


def switch_data(league):
    if league not in ALLOWED_LEAGUES:
        raise ValueError("Invalid leaque selected")
    df = pd.read_csv(f"./data/sample_{league}.csv")
    return df


# Define the GUI layout
layout = """
# Baseball Data Visualization

<|
### Filters
League: <|{league}|selector|lov=central;pacific|on_change=update_data|>
|>

<|
### Filtered Data
<|{df.drop_duplicates(subset=['チーム名'],keep='last').sort_values('順位')}|table|>
|>
"""

# Create a Taipy GUI application
gui = Gui(page=layout)


# Bind dynamic updates
def update_data(state):
    state.df = switch_data(state.league)


df = switch_data(league)

# Bind the update function to the GUI
gui.run(title="Baseball Data Viz", dark_mode=False, state={"df": df, "league": league})
