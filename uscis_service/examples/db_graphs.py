import dash
import dash_core_components as dcc
import dash_html_components as html
from src.graph_stuff import UscisGraphBuilder, GraphCommon


ug = UscisGraphBuilder()
ug.describe()
G = ug.digraph(form="Common")
G.describe_graph_degree()
G.add_colors(d={
    "Case Was Approved": "red",
    "Case Was Approved And My Decision Was Emailed": "orange",
    "Case Was Denied": "magenta",
    "Case Was Received": "green",
})

sub_g = G.problematic_subgraph()

graphs = [
    dcc.Graph(figure=G.build_figure_from_graph(
        pos=G.find_layout(), title="Status Oriented Graph")),
    dcc.Graph(figure=sub_g.build_figure_from_graph(
        pos=G.find_layout(), title="Cycle subset - Raw")),
    dcc.Graph(figure=sub_g.build_figure_from_graph(
        pos=sub_g.find_shell_layout(), title="Cycle subset - Circle")),
    dcc.Graph(figure=G.build_figure_from_graph(
        pos=G.find_even_better_layout(), title="Status Oriented Graph - Improved")),
]

app = dash.Dash()
app.layout = html.Div(graphs)
server = app.server


if __name__ == '__main__':
    app.run_server(debug=False, port=8850, host="0.0.0.0")
