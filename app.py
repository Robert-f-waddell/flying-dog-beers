import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go


covid_df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
covid_df = covid_df[["continent",
                     "location",
                     "date",
                     "total_cases",
                    "new_cases",
                    "new_cases_smoothed",
                    "total_deaths",
                    "new_deaths",
                    "new_deaths_smoothed",]]

covid_df = covid_df[covid_df["total_cases"].notna()]


app = dash.Dash(__name__)
server = app.server
country_names =covid_df.location.unique()
country_names.sort()

app.layout = html.Div([
    html.Div([dcc.Dropdown(id='group-select', options=[{'label': i, 'value': i} for i in country_names],
                           value='TOR', style={'width': '140px'})]),
    dcc.Graph('country statistics', config={'displayModeBar': False})])

@app.callback(
    Output('country statistics', 'figure'),
    [Input('group-select', 'value')]
)
def update_graph(name):  
    country_df = covid_df[covid_df["location"].str.contains(name)]
    country_df = country_df.sort_values(by="date",ascending=True)


    fig = make_subplots(rows=2, cols=2,
                       subplot_titles=("Total Cases", "Daily Cases","Total Deaths","Daily Deaths"))

    fig.add_trace(
        go.Scatter(x=country_df["date"], y=country_df["total_cases"]),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=country_df["date"], y=country_df["total_deaths"]),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(x=country_df["date"], y=country_df["new_cases"]),
        row=1, col=2
    )

    fig.add_trace(
        go.Scatter(x=country_df["date"], y=country_df["new_deaths"]),
        row=2, col=2
    )

    fig.update_layout(height=800, width=800, title_text= name,showlegend=False)
    return fig
    
if __name__ == '__main__':
    app.run_server(debug=False)
