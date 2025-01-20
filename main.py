import pandas as pd
from taipy.gui import Gui
import plotly.graph_objects as go


colors = {
    "DeNA": "blue",
    "阪神": "yellow",
    "ヤクルト": "purple",
    "広島": "red",
    "巨人": "orange",
    "中日": "black",
    "ロッテ": "black",
    "オリックス": "blue",
    "西武": "purple",
    "ソフトバンク": "yellow",
    "楽天": "red",
    "日本ハム": "grey",
}


def create_plot(df, selected_teams, column="順位"):
    figure = go.Figure()
    for team in selected_teams:
        team_df = df[df["チーム名"] == team]
        figure.add_trace(
            go.Scatter(
                x=team_df["date"],
                y=team_df[column],
                mode="lines",
                line=dict(color=colors[team]),
                name=team,
            )
        )

    figure.update_layout(
        title=f"Selected: {column}",
        xaxis_title="Date",
        yaxis_title=column,
        legend_title="Teams",
        yaxis=dict(autorange="reversed" if column == "順位" else None),
    )
    return figure


# Define allowed leagues
ALLOWED_LEAGUES = {"central", "pacific"}
# define initial filters
league = "central"


def switch_data(league):
    league = league.lower()
    if league not in ALLOWED_LEAGUES:
        raise ValueError("Invalid league selected")
    df = pd.read_csv(f"./data/sample_{league}.csv")
    return df


# Define the GUI layout
layout = """
# Baseball Data Visualization

<|
### League
<|{league}|selector|lov=Central;Pacific|on_change=update_data|>
|>
### Standing 
<|{df.drop_duplicates(subset=['チーム名'],keep='last').sort_values('順位')}|table|>

### Plot 
#####Column
<|{selected_column}|selector|lov={columns}|on_change=update_column|dropdown|>
#####Teams
<|{selected_teams}|selector|lov={teams}|on_change=update_teams|multiple|>
<|chart|figure={figure}|>
"""

# Create a Taipy GUI application
gui = Gui(page=layout)


# Bind dynamic updates


def update_data(state):
    state.df = switch_data(state.league)
    state.teams = (
        state.df.drop_duplicates(subset=["チーム名"], keep="last")
        .sort_values("順位")["チーム名"]
        .tolist()
    )
    state.selected_teams = state.teams
    state.figure = create_plot(state.df, state.selected_teams, state.selected_column)


def update_column(state):
    state.figure = create_plot(state.df, state.selected_teams, state.selected_column)


def update_teams(state):
    state.figure = create_plot(state.df, state.selected_teams, state.selected_column)


df = switch_data(league)
columns = df.columns.to_list()
columns.pop(1)
teams = (
    df.drop_duplicates(subset=["チーム名"], keep="last")
    .sort_values("順位")["チーム名"]
    .tolist()
)
# teams = df["チーム名"].unique().tolist()
selected_column = columns[0]
selected_teams = teams
figure = create_plot(df, teams)


# Bind the update function to the GUI
gui.run(title="Baseball Data Viz", dark_mode=False)
