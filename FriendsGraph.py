import networkx as nx
import matplotlib.pyplot as plt
from helperFunctions import *




def drawFriendsGraph(main_puuid, connections):
    
    G = nx.Graph()
    plt.rcParams["font.family"] = "Yu Gothic"
    
    
    #starting user
    G.add_node(main_puuid)
    max_width = (connections[0])[1]
    
    #print(connections)
    print (f"max width: {max_width}")
    
    #connectioins to all other people
    for player_puuid, games_together in connections:
        if player_puuid == main_puuid:
            continue
        G.add_edge(main_puuid, player_puuid, weight = games_together)
        
    #positioning
    pos = nx.spring_layout(G, seed=42)
    
    #edge width
    edge_widths = [
        min(G[u][v]["weight"], 5)
        for u, v in G.edges()
    ]
    
    #node size
    node_sizes = []

    for node in G.nodes():
        if node == main_puuid:
            node_sizes.append(1200)
        else:
            weight = G[main_puuid][node]["weight"]
            size = 300 + weight * 50
            
            if size > 1000:
                size = 1000      
                
            node_sizes.append(size)

    #labels
    labels = {}
    
    for node in G.nodes():
        labels[node] = getAccount(node)
            
    
    nx.draw(
        G,
        pos,
        with_labels=False,
        node_size=node_sizes,
        width=edge_widths
    )
    
    nx.draw_networkx_labels(
        G,
        pos,
        labels=labels,
        font_size=8,
        font_family="Yu Gothic"
    )
            
    plt.show()
            
    