import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import Filters

data = pd.read_pickle('Data/combined.pkl')
test_type = Filters.get_test_types()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='test_type',
                options=test_type,
                value=test_type[0]['value']
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
    [Input('reference', 'value')])
def update_graph(chosen_test):
    chosen_data = data.loc[data['TestId'] == chosen_test]
    fig = px.box(data_frame=chosen_data, x='ASSETID', y='DATAVALUE', color='TestSubRef')
    lower, upper = chosen_data['Lower'].iloc[0], chosen_data['Upper'].iloc[0]
    fig.update_layout(shapes=[
        dict(type="line", xref="paper", yref="y", x0=0, y0=lower, x1=1, y1=lower, line_width=3),
        dict(type="line", xref="paper", yref="y", x0=0, y0=upper, x1=1, y1=upper, line_width=3)])
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
