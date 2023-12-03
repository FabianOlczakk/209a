import json
import networkx as nx
import matplotlib.pyplot as plt

# Load JSON data from a file
with open('aut_x44.json') as f:
    data = json.load(f)

def extract_json_keys(data):
    """
    Recursively extract keys from a nested JSON structure.
    Args:
        data (dict): JSON data
    Returns:
        list: List of lists containing the extracted keys
    """
    extracted_keys = []

    for key, value in data.items():
        temp = [key]
        for k in value.keys():
            temp.append(k)
        
        extracted_keys.append(temp)
        extracted_keys += extract_json_keys(value)
    
    return extracted_keys

# Extract keys from the JSON data
extracted_data = extract_json_keys(data)

# Remove lists smaller than 3
extracted_data = [x for x in extracted_data if len(x) >= 3]

# Remove first 3 characters from keys with length greater than 2
for i in range(len(extracted_data)):
    if len(extracted_data[i][0]) > 2:
        extracted_data[i][0] = extracted_data[i][0][3:]

def bubble_sort_signals(data):
    """
    Sort the data based on the second element of each sublist using bubble sort.
    Args:
        data (list): List of lists
    Returns:
        list: Sorted list of lists
    """
    sorted_data = []

    for i in data:
        sublist = i[1:]
        n = len(sublist)

        for k in range(n):
            for j in range(0, n-k-1):
                if sublist[j][1] > sublist[j+1][1]:
                    sublist[j], sublist[j+1] = sublist[j+1], sublist[j]
        
        sorted_data.append([i[0]] + sublist)

    return sorted_data

# Sort the extracted data
sorted_data = bubble_sort_signals(extracted_data)

# Convert list of lists to list of tuples
sorted_data = [tuple(x) for x in sorted_data]

# Remove duplicates
sorted_data = list(set(sorted_data))

# Add index to each tuple
for i in range(len(sorted_data)):
    sorted_data[i] = (i,) + sorted_data[i]

# Print the data
for i in sorted_data:
    print(i)

# Create a new graph
G = nx.DiGraph()
edge_labels = {}

# Add nodes
for i in sorted_data:
    G.add_node(f'q{i[0]}({i[1]})')
  
# Add edges
for i in sorted_data:
    for l in range(1, len(i)):
        edges = []
        for k in sorted_data:
            if k[1] == str(i[l][3:5]): 
                edges.append(f'q{k[0]}({k[1]})')

        for k in edges:
            edge = (f'q{i[0]}({i[1]})', k)
            if edge in edge_labels:
                G.add_edge(*edge, label=f'{edge_labels[edge]}, z{i[l][1]}')
            else:
                G.add_edge(*edge, label=f'z{i[l][1]}')
            edge_labels[edge] = f'z{i[l][1]}'

# Draw the graph with node labels
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, arrows=True)
edge_labels = nx.get_edge_attributes(G, 'label')

# Draw edge labels for all edges except self-loops
for edge, label in edge_labels.items():
    if edge[0] != edge[1]:  # not a self-loop
        label_pos = nx.draw_networkx_edge_labels(G, pos, edge_labels={edge: label})

# Manually add edge labels for self-loops
for node, coords in pos.items():
    if G.has_edge(node, node):  # is a self-loop
        x, y = coords
        dx, dy = 0.1, 0.1  # adjust these values to move the label
        plt.text(x + dx, y + dy, edge_labels[(node, node)], fontsize=10)

# Display the graph
plt.show()