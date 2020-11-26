import dash
import dash_core_components as dcc
import dash_html_components as html
from src.graph_stuff import UscisGraphBuilder, GraphCommon


ug = UscisGraphBuilder()
ug.describe()
G = ug.digraph(form="Common")


GraphCommon.describe_graph_degree(g=G)

GraphCommon.add_colors(g=G, d={
    "Case Was Approved": "red",
    "Case Was Approved And My Decision Was Emailed": "orange",
    "Case Was Denied": "magenta",
    "Case Was Received": "green",
})

enhanced_pos = GraphCommon.find_layout(g=G)
sub_g = GraphCommon.problematic_subgraph(g=G)
even_better_pos = GraphCommon.find_even_better_layout(g=G)


graphs = [
    dcc.Graph(figure=GraphCommon.build_figure_from_graph(
        G=G, pos=enhanced_pos, title="Status Oriented Graph"))
]

if "sub_g" in locals():
    graphs.append(dcc.Graph(figure=GraphCommon.build_figure_from_graph(
        G=sub_g, pos=enhanced_pos, title="Cycle subset - Raw")))
    graphs.append(dcc.Graph(figure=GraphCommon.build_figure_from_graph(
        G=sub_g, pos=GraphCommon.find_shell_layout(g=sub_g), title="Cycle subset - Circle")))


app = dash.Dash()
app.layout = html.Div(graphs)
server = app.server


if __name__ == '__main__':
    app.run_server(debug=False, port=8850, host="0.0.0.0")
