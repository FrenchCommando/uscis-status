import pandas as pd
import requests
import json
import networkx as nx
import matplotlib.pyplot as plt
from src.constants import port_number, host_uscis_service


r = requests.get(f'http://{host_uscis_service}:{port_number}/graph')
data = json.loads(r.text)

print(f"Number of Items:\t{data['number_of_items']}")
graph = data['graph']
print(f"Graph\t{graph}")

for form, v in graph.items():
    print(f"Form:\t{sum(sum(vv.values()) for vv in v.values())}\t{form}")

common = graph["Common"]
common = graph["Form I-129, Petition for a Nonimmigrant Worker"]
# common = graph["Form I-290B, Notice of Appeal or Motion"]

for old_status, vv in common.items():
    print(old_status)
    print(vv)


plt.figure("Status Graph")
G = nx.DiGraph()
G.add_weighted_edges_from(ebunch_to_add=[
    (old_status, new_status, number) for old_status, v in common.items() for new_status, number in v.items()
])
nx.set_node_attributes(G=G, name='favorite_color', values={
    "Case Was Approved": "red",
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
                # print(y_from, y_to, node_from, node_to, y_from - (y_to - y_from))
                enhanced_pos[node_to][direction] = y_from - (y_to - y_from)
                return False
    return True


i = 0
while not direction_consistent() and i < 100:
    i += 1
print(i)

for (n1, p1), (n2, p2) in zip(pos.items(), enhanced_pos.items()):
    print(p1, p2, n1, n2)
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
plt.show()
