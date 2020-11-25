import pandas as pd
import requests
import json
import networkx as nx
import matplotlib.pyplot as plt
from src.constants import port_number, host_uscis_service
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html


r = requests.get(f'http://{host_uscis_service}:{port_number}/graph')
data = json.loads(r.text)

print(f"Number of Items:\t{data['number_of_items']}")
graph = data['graph']
print(f"Graph\t{graph}")

for form, v in graph.items():
    print(f"Form:\t{sum(sum(vv.values()) for vv in v.values())}\t{form}")

common = graph["Common"]
# common = graph["Form I-129, Petition for a Nonimmigrant Worker"]
# common = graph["Form I-290B, Notice of Appeal or Motion"]

for old_status, vv in common.items():
    print(old_status)
    print(vv)

G = nx.DiGraph()
G.add_weighted_edges_from(ebunch_to_add=[
    (old_status, new_status, number) for old_status, v in common.items() for new_status, number in v.items()
])
nx.set_node_attributes(G=G, name='favorite_color', values={
    "Case Was Approved": "red",
    "Case Was Received": "green",
    "Case Was Approved And My Decision Was Emailed": "orange",
    "Case Was Denied": "magenta",

})
for (n, d), (nn, dd), (nnn, ddd) in zip(G.degree(), G.out_degree(), G.in_degree()):
    print(d, dd, ddd, n, nn, nnn)
print(nx.info(G))
pos = nx.shell_layout(G=G)
enhanced_pos = nx.shell_layout(G=G)


def direction_consistent(direction=1):
    for node_from in enhanced_pos:
        y_from = enhanced_pos[node_from][direction]
        for node_to in G.successors(n=node_from):
            y_to = enhanced_pos[node_to][direction]
            if node_from in G.successors(node_to):
                # if y_to != y_from:
                #     print("equal", y_from, y_to, node_from, node_to)
                #     enhanced_pos[node_from][direction] = min(y_from, y_to)
                #     enhanced_pos[node_to][direction] = min(y_from, y_to)
                #     return False
                continue
            if y_from <= y_to:
                print(y_from, y_to, node_from, node_to, y_from - (y_to - y_from))
                enhanced_pos[node_to][direction] = y_from - (y_to - y_from)
                return False
    return True


i = 0
while not direction_consistent() and i < 100:
    i += 1
print(i)

for (n1, p1), (n2, p2) in zip(pos.items(), enhanced_pos.items()):
    print(p1, p2, n1, n2)

if i == 100:
    i = 0
    while not direction_consistent(direction=0) and i < 100:
        i += 1

    subG = G.subgraph(nodes=(n for n in enhanced_pos if enhanced_pos[n][1] < -20))

    def draw_internal(sub_layout):
        nx.draw(
            subG,
            with_labels=True, font_size=5, node_size=200, width=1,
            pos=sub_layout,
        )
        for node, val in subG.nodes.data():
            if "favorite_color" in val:
                color_value = val["favorite_color"]
                nx.draw_networkx_nodes(
                    G, sub_layout, nodelist=[node], node_color=color_value, node_size=100, alpha=0.8
                )

    plt.figure(num="Cycle subset - Raw")
    draw_internal(sub_layout=enhanced_pos)

    plt.figure(num="Cycle subset - Circle")
    draw_internal(sub_layout=nx.shell_layout(G=subG))

plt.figure(num="Status Oriented Graph")
nx.draw(
    G,
    with_labels=True, font_size=5, node_size=200, width=1,
    pos=enhanced_pos,
)
for node, val in G.nodes.data():
    if "favorite_color" in val:
        color_value = val["favorite_color"]
        nx.draw_networkx_nodes(
            G, enhanced_pos, nodelist=[node], node_color=color_value, node_size=100, alpha=0.8
        )

# plt.show()


def build_figure_from_graph(G, pos, title):
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: '+str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                    title=f'<br>{title}',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    return fig


graphs = [
    dcc.Graph(figure=build_figure_from_graph(G=G, pos=enhanced_pos, title="Status Oriented Graph"))
]

if "subG" in locals():
    graphs.append(dcc.Graph(figure=build_figure_from_graph(
        G=subG, pos=enhanced_pos, title="Cycle subset - Raw")))
    graphs.append(dcc.Graph(figure=build_figure_from_graph(
        G=subG, pos=nx.shell_layout(G=subG), title="Cycle subset - Circle")))


app = dash.Dash()
app.layout = html.Div(graphs)

server = app.server


if __name__ == '__main__':
    app.run_server(debug=False, port=8850, host="0.0.0.0")
