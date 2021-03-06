import dash
import dash_core_components as dcc
import dash_html_components as html
from src.graph_stuff import UscisGraphBuilder, GraphCommon


ug = UscisGraphBuilder()
ug.describe()

graphs = [
    dcc.Graph(id='graph1'),
    dcc.Graph(id='graph2'),
    dcc.Graph(id='graph3'),
    dcc.Graph(id='graph4'),
    dcc.Graph(id='graph5'),
]

form_chooser = dcc.Dropdown(
    id='crossfilter-form', options=[dict(label=i, value=i) for i in ug.forms],
    value="Common", multi=False,
)
metric_chooser = dcc.RadioItems(
    id='metric-radio',
    options=[dict(label=i, value=i) for i in [
        "Connections", "Up-Down",
    ]],
    value="Up-Down",
    labelStyle={'display': 'inline-block'}
)

app = dash.Dash()
app.layout = html.Div(children=[
    html.Div(form_chooser),
    html.Div(metric_chooser),
    html.Div(graphs)
])
server = app.server


@app.callback(
    [
        dash.dependencies.Output('graph1', 'figure'),
        dash.dependencies.Output('graph2', 'figure'),
        dash.dependencies.Output('graph3', 'figure'),
        dash.dependencies.Output('graph4', 'figure'),
        dash.dependencies.Output('graph5', 'figure'),
     ],
    [
        dash.dependencies.Input('crossfilter-form', 'value'),
        dash.dependencies.Input('metric-radio', 'value'),
    ]
)
def update_graph(form_value, metric_value):
    G = ug.digraph(form=form_value)
    G.describe_graph_degree()
    G.add_colors(d={
        "Case Was Approved": "red",
        "Case Was Approved And My Decision Was Emailed": "orange",
        "Case Was Denied": "magenta",
        "Case Was Received": "green",
    })
    sub_g = G.problematic_subgraph()

    return \
        G.build_figure_from_graph(pos=G.find_shell_layout(),
                                  title="Status Oriented Graph - Shell", metric=metric_value),\
        G.build_figure_from_graph(pos=G.find_even_better_layout(),
                                  title="Status Oriented Graph - Improved", metric=metric_value),\
        G.build_figure_from_graph(pos=G.find_layout(),
                                  title="Status Oriented Graph", metric=metric_value),\
        sub_g.build_figure_from_graph(pos=G.find_layout(),
                                      title="Cycle subset - Raw", metric=metric_value),\
        sub_g.build_figure_from_graph(pos=sub_g.find_shell_layout(),
                                      title="Cycle subset - Circle", metric=metric_value),


if __name__ == '__main__':
    app.run_server(debug=False, port=8850, host="0.0.0.0")
