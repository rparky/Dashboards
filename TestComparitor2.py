import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import Names

data = pd.read_pickle('Data/combined.pkl')
assets = Names.get_assets()
directions = Names.get_direction()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='asset',
                options=assets,
                value=assets[0]['value']
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='direction',
                options=directions,
                value=directions[0]['value']
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),

        html.Div([dcc.Graph(id='scatter')])
    ])

@app.callback(
    Output('scatter', 'figure'),
    [Input('asset', 'value'),
     Input('direction', 'value')])
def update_graph(chosen_asset, chosen_direction):
    chosen_data = data.loc[(data['ASSETID'] == chosen_asset) & (data['DIRECTIONID'] == chosen_direction)]
    testids = chosen_data['TestId'].unique()
    pivoted = pd.pivot(chosen_data, index=['EVENTTIME', 'TestSubRef'], columns=['TestId'], values='DATAVALUE').reset_index()
    pivoted = pivoted.loc[~pivoted['TestSubRef'].isna()]
    fig = px.scatter_matrix(data_frame=pivoted, dimensions=testids, color='TestSubRef')
    fig.update_traces(diagonal_visible=False)
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
