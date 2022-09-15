# The work was performed by Zadorozhnaya Yuliya Andreevna, group 217

 Building a control network in an SDN network

# Dependencies
The application requires Python 3.6 or higher.
Standard libraries are used.

# Launch
Data format:

1) -t <topology file name> - from the TopologyZoo library in GraphML format.

2) Additional parameters k1 and k2.

An example of starting the program:

```
>>> python3 ./main.py -t tests/AttMpls.graphml -k1 3 -k2 22
Parsed arguments:
destination_node_id = 22
file_name = tests/AttMpls.graphml
source_node_id = 3
Parsed 25 nodes
Parsed 114 edges
Parsed graph: G(25 nodes, 114 edges)
Written topology to file tests/AttMpls.graphml_topo.csv
Written routes to file tests/AttMpls.graphml_routes.csv
Visualization available at file tests/AttMpls.graphml_demo.html
```

The program generates two csv files and an HTML file with graph visualization:

1) CSV file with description of network communication channels in ascending order of id of nodes.

2) CSV file describing the spanning tree.
The direct path is marked in black, the backup path is marked in red.

# Graph visualization
![alt text](image/graph.png "www.topology-zoo.org, ATT North America")
