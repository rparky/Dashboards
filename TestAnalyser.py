import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import Names
import Links

data = pd.read_pickle('Data/combined.pkl')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='test_type',
                options=Names.test_types_dict,
                value=Names.test_types_dict[0]['value']
            )
        ], style={'width': '48%', 'float': 'middle', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='reference'
            )
                  ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),

    html.Div([dcc.Graph(id='bar')]),
    html.Div([dcc.Graph(id='scatter')])
])


@app.callback(
    [Output('reference', 'options'),
     Output('reference', 'value')],
    Input('test_type', 'value'))
def get_test_options(chosen_test_type):
    ref_dict = Links.get_test_refs(chosen_test_type)
    return ref_dict, ref_dict[0]['value']

@app.callback(
    Output('bar', 'figure'),
    [Input('reference', 'value')])
def update_graph(chosen_test):
    chosen_data = data.loc[data['TestId'] == chosen_test]
    chosen_data = chosen_data.merge(Names.assets, left_on='ASSETID', right_on='ASSETID')
    fig = px.box(data_frame=chosen_data, x='VALUE', y='DATAVALUE',
                 color='TestSubRef', notched=True, hover_name='ASSETID')
    lower, upper = Links.get_thresholds_for_a_test(chosen_test)
    fig.update_layout(shapes=[
        dict(type="line", xref="paper", yref="y", x0=0, y0=lower, x1=1, y1=lower, line_width=3),
        dict(type="line", xref="paper", yref="y", x0=0, y0=upper, x1=1, y1=upper, line_width=3)])
    fig.update_layout(margin={'l': 10, 'b': 10, 't': 10, 'r': 10}, hovermode='closest')

    return fig

@app.callback(
    Output('scatter', 'figure'),
    [Input('bar', 'clickData'),
     Input('reference', 'value')])
def display_click_data(clickData, chosen_test):
    asset_name = clickData['points'][0]['x']
    chosen_asset = Names.assets.loc[Names.assets['VALUE'] == asset_name, 'ASSETID'].iloc[0]
    chosen_data = data.loc[(data['ASSETID'] == chosen_asset) & (data['TestId'] == chosen_test)]
    fig = px.scatter(data_frame=chosen_data, x='EVENTTIME', y='DATAVALUE', color='TestSubRef', title=asset_name)
    lower, upper = Links.get_thresholds_for_a_test(chosen_test)
    fig.update_layout(shapes=[
        dict(type="line", xref="paper", yref="y", x0=0, y0=lower, x1=1, y1=lower, line_width=3),
        dict(type="line", xref="paper", yref="y", x0=0, y0=upper, x1=1, y1=upper, line_width=3)])
    fig.update_layout(margin={'l': 10, 'b': 10, 't': 40, 'r': 10}, hovermode='closest')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
