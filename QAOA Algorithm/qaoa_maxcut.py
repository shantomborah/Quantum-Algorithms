import networkx as nx
import matplotlib.pyplot as plt

from networkx.drawing.layout import spring_layout
from qaoa_components import QAOA


# Build input graph
V = list(range(7))
E = [(0, 5), (0, 2), (1, 2), (1, 3), (2, 5), (2, 6), (3, 5), (3, 4), (4, 5), (4, 6)]
G = nx.Graph()
G.add_nodes_from(V)
G.add_edges_from(E)

# Draw input graph
fig = plt.figure(figsize=(10, 5))
fig.suptitle('Max Cut')
plt.subplot(121)
ax = plt.gca()
ax.set_title('Input Graph')
pos = spring_layout(G)
nx.draw(G, with_labels=True, node_color='lightgreen', edge_color='lightblue',
        style='solid', width=2, ax=ax, pos=pos, font_size=8, font_weight='bold')

# Generate QAOA clauses
clauses = []
for i in range(len(E)):
    edge = E[i]
    clause = ['X'] * len(V)
    clause[edge[0]] = '0'
    clause[edge[1]] = '1'
    clauses.append("".join(clause))
    clause = ['X'] * len(V)
    clause[edge[0]] = '1'
    clause[edge[1]] = '0'
    clauses.append("".join(clause))

# Execute QAOA
qaoa = QAOA(clauses, 6)
z = qaoa.sample(vis=True)
print('Sampled Output: ' + str(z))
print('Optimized Cost: ' + str(qaoa.cost(z)))

# Extract colormap
color_map = []
for i in range(len(V)):
    if z[i] == '0':
        color_map.append('blue')
    else:
        color_map.append('red')

# Extract cuts
cuts = []
for e in E:
    if z[e[0]] == z[e[1]]:
        cuts.append('solid')
    else:
        cuts.append('dashed')

# Draw output graph
plt.figure(fig.number)
plt.subplot(122)
ax = plt.gca()
ax.set_title('Output Graph')
nx.draw(G, with_labels=True, node_color=color_map, edge_color='green',
        style=cuts, width=2, ax=ax, pos=pos, font_size=8, font_weight='bold')
plt.show()
