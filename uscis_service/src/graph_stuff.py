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
        enhanced_pos = self.find_shell_layout()
        i = 0
        i_max = 100
        while not self.direction_consistent(pos=enhanced_pos, direction=1) and i < i_max:
            i += 1
        i = 0
        i_max = 100
        while not self.direction_consistent(pos=enhanced_pos, direction=0) and i < i_max:
            i += 1
        return enhanced_pos

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

    def build_figure_from_graph(self, pos, title, metric):
        G = self.g
        pos = {node: value for node, value in pos.items() if node in G.nodes()}

        # https://stackoverflow.com/questions/57482878/plotting-a-directed-graph-with-dash-through-matplotlib

        elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 10]
        esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 10]

        # pos = nx.spring_layout(G)  # positions for all nodes

        x_n = [pos[k][0] for k in pos]
        y_n = [pos[k][1] for k in pos]

        data = []
        if metric == "Connections":
            adjacency_dict = {node: len(adjacency) for node, adjacency in G.adjacency()}
            node_text = [f'{node}<br># of connections: {adjacency_dict[node]}' for node in pos]
            node_adjacencies = [adjacency_dict[node] for node in pos]

            nodes = dict(
                type='scatter', x=x_n, y=y_n, mode='markers+text',
                marker=dict(
                    showscale=True,
                    symbol='arrow-up',
                    colorscale='YlGnBu',
                    reversescale=True,
                    color=node_adjacencies,
                    size=10,
                    colorbar=dict(
                        thickness=15,
                        title='Node Connections',
                        xanchor='left',
                        titleside='right'
                    ),
                    line_width=2
                ),
                textfont=dict(size=3, color='blue'),
                text=node_text,
                hoverinfo='text',
            )
            data.append(nodes)
        if metric == "Up-Down":
            in_degree_dict = {node: degree for node, degree in G.in_degree()}
            out_degree_dict = {node: degree for node, degree in G.out_degree()}
            node_text = [f'{node}<br># of in: {in_degree_dict[node]}<br># of out: {out_degree_dict[node]}'
                         for node in pos]
            node_up = [out_degree_dict[node] for node in pos]

            nodes_up = dict(
                type='scatter', x=x_n, y=y_n, mode='markers+text',
                marker=dict(
                    showscale=True,
                    symbol='arrow-up',
                    colorscale='YlGnBu',
                    reversescale=True,
                    color=node_up,
                    size=10,
                    colorbar=dict(
                        thickness=15,
                        title='Node Up',
                        xanchor='left',
                        titleside='right'
                    ),
                    line_width=2
                ),
                textfont=dict(size=3, color='blue'),
                text=node_text,
                hoverinfo='text',
            )
            data.append(nodes_up)

            node_down = [in_degree_dict[node] for node in pos]

            nodes_down = dict(
                type='scatter', x=x_n, y=y_n, mode='markers',
                marker=dict(
                    showscale=True,
                    symbol='arrow-down',
                    colorscale='RdYlGn',
                    reversescale=True,
                    color=node_down,
                    size=10,
                    colorbar=dict(
                        thickness=5,
                        title='Node Down',
                        xanchor='left',
                        titleside='right'
                    ),
                    line_width=1
                ),
            )
            data.append(nodes_down)

        annotateELarge = [dict(
            showarrow=True, arrowsize=1, arrowwidth=1, arrowhead=1, standoff=10, startstandoff=10,
            ax=pos[arrow[0]][0], ay=pos[arrow[0]][1], axref='x', ayref='y',
            x=pos[arrow[1]][0], y=pos[arrow[1]][1], xref='x', yref='y',
        ) for arrow in elarge]
        annotateESmall = [dict(
            showarrow=True, arrowsize=1, arrowwidth=1, arrowhead=1, opacity=0.5, standoff=10, startstandoff=10,
            ax=pos[arrow[0]][0], ay=pos[arrow[0]][1], axref='x', ayref='y',
            x=pos[arrow[1]][0], y=pos[arrow[1]][1], xref='x', yref='y'
        ) for arrow in esmall]

        layout = dict(
            title=f'<br>{title}',
            showlegend=False,
            hovermode='closest',
            plot_bgcolor='#E5ECF6',
            annotations=annotateELarge + annotateESmall,  # arrows
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        )

        plotly_fig = dict(data=data, layout=layout, margin=dict(b=20, l=5, r=5, t=40),)
        return plotly_fig
