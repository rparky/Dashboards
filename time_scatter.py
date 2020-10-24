import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

data = pd.read_pickle('Data/combined.pkl')
refs = pd.read_csv('Data/References.csv')

assets = data['ASSETID'].unique()
test_type = data['TestTypeId'].unique()
assets.sort()
test_type.sort()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='asset',
                options=[{'label': i, 'value': i} for i in assets],
                value=assets[0]
            )
        ],
        style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='test_type',
                options=[{'label': i, 'value': i} for i in test_type],
                value=test_type[0]
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
    references = refs.loc[refs['TestTypeId'] == chosen_test_type, 'Reference'].unique()
    references.sort()
    return [{'label': i, 'value': i} for i in references], references[0]

@app.callback(
    Output('scatter', 'figure'),
    [Input('asset', 'value'),
     Input('test_type', 'value'),
     Input('reference', 'value')])
def update_graph(chosen_asset, chosen_test_type, chosen_ref):
    asset_data = data.loc[data['ASSETID'] == chosen_asset]
    test_data = asset_data.loc[asset_data['TestTypeId'] == chosen_test_type]
    ref_data = test_data.loc[test_data['Reference'] == chosen_ref]
    fig = px.scatter(data_frame=ref_data, x='EVENTTIME', y='DATAVALUE', color='TestSubRef')
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
