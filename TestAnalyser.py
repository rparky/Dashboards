import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import Filters

data = pd.read_pickle('Data/combined.pkl')
assets = Filters.get_assets()
test_type = Filters.get_test_types()

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
        style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='test_type',
                options=test_type,
                value=test_type[0]['value']
            )
        ], style={'width': '30%', 'float': 'middle', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='reference'
            )
                  ], style={'width': '30%', 'float': 'right', 'display': 'inline-block'})
        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),

        html.Div([dcc.Graph(id='scatter')])
    ])


@app.callback(
    [Output('reference', 'options'),
     Output('reference', 'value')],
    Input('test_type', 'value'))
def set_cities_options(chosen_test_type):
    ref_dict = Filters.get_test_refs(chosen_test_type)
    return ref_dict, ref_dict[0]['value']

@app.callback(
    Output('scatter', 'figure'),
    [Input('asset', 'value'),
     Input('reference', 'value')])
def update_graph(chosen_asset, chosen_test):
    chosen_data = data.loc[(data['ASSETID'] == chosen_asset) & (data['TestId'] == chosen_test)]
    fig = px.scatter(data_frame=chosen_data, x='EVENTTIME', y='DATAVALUE', color='TestSubRef')
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
