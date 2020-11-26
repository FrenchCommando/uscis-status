import json
import networkx as nx
import requests
import plotly.graph_objects as go
from src.constants import port_number, host_uscis_service


class UscisGraphBuilder:
    def __init__(self):
        r = requests.get(f'http://{host_uscis_service}:{port_number}/graph')
        data = json.loads(r.text)
        self.graph = data['graph']
        self.number_of_items = data['number_of_items']
        self.forms = list(self.graph.keys())
        self.form_count = {form: sum(sum(vv.values()) for vv in v.values()) for form, v in self.graph.items()}

    def describe(self):
        print(f"Number of Items:\t{self.number_of_items}")
        print(f"Graph:\t{self.graph}")
        for f in self.forms:
            print(f"Form:\t{self.form_count[f]:9d}\t{f}")

    def digraph(self, form="Common"):
        if form not in self.forms:
            raise ValueError("UscisGraph - digraph - form not in forms")
        common = self.graph[form]
        g = nx.DiGraph()
        g.add_weighted_edges_from(ebunch_to_add=[
            (old_status, new_status, number) for old_status, v in common.items() for new_status, number in v.items()
        ])
        return GraphCommon(g)


class GraphCommon:
    def __init__(self, g):
        self.g = g

    def describe_graph_degree(self):
        for (n, d), (nn, dd), (nnn, ddd) \
                in zip(self.g.degree(), self.g.out_degree(), self.g.in_degree()):
            print(d, dd, ddd, n, nn, nnn)
        print(nx.info(self.g))

    def problematic_subgraph(self):
        enhanced_pos = self.find_layout()
        sub_g = self.g.subgraph(nodes=(n for n in enhanced_pos if enhanced_pos[n][1] < -20))
        return GraphCommon(g=sub_g)

    def add_colors(self, d):
        nx.set_node_attributes(G=self.g, name='favorite_color', values=d)

    def direction_consistent(self, pos, direction):
        for node_from in pos:
            y_from = pos[node_from][direction]
            for node_to in self.g.successors(n=node_from):
                y_to = pos[node_to][direction]
                if node_from in self.g.successors(node_to):
                    continue
                if y_from <= y_to:
                    # print(y_from, y_to, node_from, node_to, y_from - (y_to - y_from))
                    pos[node_to][direction] = y_from - (y_to - y_from)
                    return False
        return True

    def find_shell_layout(self):
        return nx.shell_layout(G=self.g)

    def find_layout(self):
        enhanced_pos = self.find_shell_layout()
        i = 0
        i_max = 100
        while not self.direction_consistent(pos=enhanced_pos, direction=1) and i < i_max:
            i += 1
        return enhanced_pos

    def find_even_better_layout(self):
        return self.find_shell_layout()

    @staticmethod
    def draw_internal(sub_g, sub_layout):  # used in conjonction with matplotlib
        nx.draw(
            sub_g.g,
            with_labels=True, font_size=5, node_size=200, width=1,
            pos=sub_layout,
        )
        for node, val in sub_g.g.nodes.data():
            if "favorite_color" in val:
                color_value = val["favorite_color"]
                nx.draw_networkx_nodes(
                    sub_g.g, sub_layout, nodelist=[node], node_color=color_value, node_size=100, alpha=0.8
                )

    def build_figure_from_graph(self, pos, title):
        G = self.g
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
            node_text.append('# of connections: ' + str(len(adjacencies[1])))

        node_trace.marker.color = node_adjacencies
        node_trace.text = node_text

        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title=f'<br>{title}',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )
        )
        return fig
