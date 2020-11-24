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

G = nx.DiGraph()
G.add_weighted_edges_from(ebunch_to_add=[
    (old_status, new_status, number) for old_status, v in common.items() for new_status, number in v.items()
])
for (n, d), (nn, dd), (nnn, ddd) in zip(G.degree(), G.out_degree(), G.in_degree()):
    print(d, dd, ddd, n, nn, nnn)
nx.draw(G, with_labels=True)
plt.show()
