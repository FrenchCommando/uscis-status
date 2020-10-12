import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import requests
from src.constants import port_number, port_number_dash


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

r = requests.get(f'http://uscis_service:{port_number}/all')
l_text = [x.split("\t") for x in r.text.split("\n")]
print(f"Number of items:\t{l_text[0]}")
print(f"Number of lines:\t{len(l_text[1:])}")
df = pd.DataFrame(l_text[1:], columns=["ReceiptNumber", "StatusName", "FormName", "Date"])
df["PreIndex"] = df["ReceiptNumber"].apply(lambda x: x[:9])
df["PostIndex"] = df["ReceiptNumber"].apply(lambda x: int(x[9:]))


available_indicators = df.columns
available_status = df["StatusName"].unique()
available_form = df["FormName"].unique()
pre_index_list = sorted(df["PreIndex"].unique())


app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                multi=True,
                options=[{'label': i, 'value': i} for i in available_status],
                value=available_status[:4],
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value=available_indicators[1],
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_form],
                value=available_form[:4],
                multi=True,
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value=available_indicators[2],
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'Japan'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div(dcc.RangeSlider(
        id='crossfilter-year--slider',
        min=0,
        max=len(pre_index_list) - 1,
        value=[0, len(pre_index_list) - 1],
        marks={i: {'label': pre_index_list[i],
                   'style': {'writing-mode': 'vertical-lr'}}
               for i in range(0, len(pre_index_list), 10)},
        step=None
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
])


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(
        xaxis_column_name, yaxis_column_name,
        xaxis_type, yaxis_type,
        year_value
):
    dff = df[df["PreIndex"].isin(pre_index_list[year_value[0]:year_value[-1]])]
    dff = dff[dff['StatusName'].isin(xaxis_column_name)]
    dff = dff[dff['FormName'].isin(yaxis_column_name)]

    fig = px.scatter(
        x=dff['StatusName'],
        y=dff['FormName'],
        # hover_name=dff[dff['FormName'] == yaxis_column_name]['PreIndex']
    )
    # fig.update_traces(customdata=dff[dff['FormName'] == yaxis_column_name]['Date'])
    # fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')
    # fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')
    # fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    return fig


def create_time_series(dff, axis_type, title):
    fig = px.scatter(dff, x='PreIndex', y='PostIndex')
    # fig.update_traces(mode='lines+markers')
    # fig.update_xaxes(showgrid=False)
    # fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')
    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)
    # fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})
    return fig


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [
        dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
        dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
        dash.dependencies.Input('crossfilter-xaxis-type', 'value')
    ])
def update_y_timeseries(
        hoverData,
        xaxis_column_name,
        axis_type
):
    y_selection = hoverData['points'][0]['y']
    dff = df[df['StatusName'].isin(xaxis_column_name)]
    dff = dff[dff['FormName'] == y_selection]
    title = '<b>{}</b><br>{}'.format(y_selection, xaxis_column_name)
    return create_time_series(dff, axis_type, title)


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [
        dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
        dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
        dash.dependencies.Input('crossfilter-yaxis-type', 'value')
    ])
def update_x_timeseries(
        hoverData,
        yaxis_column_name,
        axis_type
):
    x_selection = hoverData['points'][0]['x']
    dff = df[df['FormName'].isin(yaxis_column_name)]
    dff = dff[dff['StatusName'] == x_selection]
    title = '<b>{}</b><br>{}'.format(x_selection, yaxis_column_name)
    return create_time_series(dff, axis_type, title)


if __name__ == '__main__':
    app.run_server(debug=False, port=port_number_dash)
