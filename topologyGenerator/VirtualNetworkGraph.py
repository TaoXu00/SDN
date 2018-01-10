import sys
import argparse
import random

CONNECTED=True    # Flag used to tell if graph is connected
KEEP_CHECKING=True # Flag used in functions: check_if_connected() and search_neighbors()

class Vertex:
  def __init__(self, node, node_weight):
    self.id = node
    self.node_weight = node_weight
    self.adjacent = {}

  def __str__(self):
    return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

  def add_neighbor(self, neighbor, weight=1):
    self.adjacent[neighbor] = weight

  def get_connections(self):
    return self.adjacent.keys()

  def get_id(self):
    return self.id

  def get_edge_weight(self, neighbor):
    return self.adjacent[neighbor]

  def get_node_weight(self):
    return self.node_weight

class Graph():
  def __init__(self):
    self.vert_dict = {}
    self.num_vertices = 0
    self.num_nodes = 0
    self.topology = ""
    self.alpha = 0  # int of range = 0-100
    self.node_min = 0
    self.node_max = 0
    self.link_min = 0
    self.link_max = 0

  def __iter__(self):
    return iter(self.vert_dict.values())

  def add_vertex(self, node, node_weight):
    self.num_vertices = self.num_vertices + 1
    new_vertex = Vertex(node, node_weight)
    self.vert_dict[node] = new_vertex
    #print "node= " + str(node) + " new_vertex= " + str(new_vertex)
    return new_vertex
  
  def remove_vertex(self, node):
    if node in self.vert_dict:
      return self.vert_dict.pop(node)
    else:
      return None

  def remove_vertices(self):
    self.vert_dict = {}

  def get_vertex(self, n):
    if n in self.vert_dict:
      return self.vert_dict[n]
    else:
      return None

  def get_vertices(self):
    return self.vert_dict.keys() 

  def add_edge(self, src, dest, weight = 0):
    if src not in self.vert_dict:
      self.add_vertex(src)
    if dest not in self.vert_dict:
      self.add_vertex(dest)

    self.vert_dict[src].add_neighbor(self.vert_dict[dest], weight)
    ### If directed graph, uncomment below... """
    #self.vert_dict[dest].add_neighbor(self.vert_dict[src], weight)

  def set_num_nodes(self, n):
    self.num_nodes = n

  def get_num_nodes(self):
    return self.num_nodes

  def set_topology(self, topo):
    self.topology = topo

  def get_topology(self):
    return self.topology

  def set_alpha(self, a):
    self.alpha = a

  def get_alpha(self):
    return self.alpha

  def set_node_min(self, n):
    self.node_min = n

  def get_node_min(self):
    return self.node_min

  def set_node_max(self, n):
    self.node_max = n

  def get_node_max(self):
    return self.node_max

  def set_link_min(self, n):
    self.link_min = n

  def get_link_min(self):
    return self.link_min

  def set_link_max(self, n):
    self.link_max = n

  def get_link_max(self):
    return self.link_max

### END classes ###

### make full (mesh) connected graph
def make_full(g):
  for node in g:
    for other_node in g:
      link_weight = int(random.uniform(g.get_link_min(), g.get_link_max()))
      if (other_node == node):
	continue
      else:
        g.add_edge(node.get_id(), other_node.get_id(), link_weight)  

def biased_coin_flip(g):
  alpha = g.get_alpha()
  coin_bias = random.uniform(1,100)
  if (coin_bias <= alpha):
    return 1 # Head
  return 0 # Tail
 
def print_graph(g):
  for node in g:
    for neighbor in node.get_connections():
      nodeid = node.get_id()
      neighborid = neighbor.get_id()
      print '%3d %3d %4d' % ( nodeid, neighborid, node.get_edge_weight(neighbor))

  for node in g:
    print node.get_node_weight(),
  
  print ""

  """ Debug: Shows current node and adjacent node(s)
  for node in g:
    print 'g.vert_dict[%s]=%s' %(node.get_id(), g.vert_dict[node.get_id()])

  print g.get_vertices()
  for node in g:
    print len(node.adjacent.keys()),
  print ""
  """

### writes graph out to file w/ filename: <topology>.out
def save_graph(g):
  f = open(g.get_topology()+'.out', 'w')
  for node in g:
    for neighbor in node.get_connections():
      nodeid = node.get_id()
      neighborid = neighbor.get_id()
      #f.writelines('%3d %3d %4d\n' % ( nodeid, neighborid, node.get_edge_weight(neighbor)))
      f.writelines('%3d %3d\n' % ( nodeid, neighborid))

  for node in g:
    f.write(str(node.get_node_weight())+ " " )

  f.write("\n")

  f.flush()
  f.close()
 
# Part of quazi-DFS
def search_neighbors(node, unvisited, visited):
  global CONNECTED
  global KEEP_CHECKING
  if KEEP_CHECKING:
    if node in unvisited:
      unvisited.remove(node) 
      visited.append(node)
      if node.get_connections():
        for neighbor in node.get_connections():
          search_neighbors(neighbor, unvisited, visited)
      elif ((len(unvisited)+1)>1): # Are we on the end node?
        KEEP_CHECKING = False
        CONNECTED = False 

"""
Performs quazi-DFS tree traversal with help from search_neighbors()
Keeps 2 lists: unvisited (filed with all nodes) and visited (empty list)
unvisited: has nodes removed as they're visited; also used to get neighbors
  of node and traverses them recursively.           
visited: as nodes are visited they get added here. Used as to break
  out of while loop by checking (# of nodes visited = # of total nodes)
KEEP_CHECKING: another check to know when to stop. Needed due to sloppiness
  of quazi-DFS implementation.
CONNECTED: "Is graph connected?"    
"""
def check_if_connected(g):
  global CONNECTED
  global KEEP_CHECKING
  KEEP_CHECKING=True
  visited = []
  unvisited = [node for node in g] 
  num_vertices = len(g.get_vertices())
  while (KEEP_CHECKING and (unvisited or (len(visited) != num_vertices))):
    node = unvisited[0]  
    search_neighbors(node, unvisited, visited)

  if not unvisited:
    CONNECTED=True
  else:
    CONNECTED=False
  return
    
def add_nodes_and_node_weights(g):
  for i in range(g.get_num_nodes()):
    node_weight = int(random.uniform(g.get_node_min(), g.get_node_max()))
    g.add_vertex(i, node_weight)
  return


""" Generates edges based on biased coin flip:
    If heads: add edge
    else: do not add edge
  Iterates over each possible pair of nodes.
  If alpha = 1, result is full graph.
  If alpha = 0, result is graph with no links. """
def generate_random_graph(g):
  for node in g:
    for other_node in g:
      if (other_node == node):
        continue
      else:
        heads = biased_coin_flip(g) 
        if heads:
          link_weight = int(random.uniform(g.get_link_min(), g.get_link_max()))
          g.add_edge(node.get_id(), other_node.get_id(), link_weight)  

### END functions ###

if __name__ == '__main__':
  topology = ""
  alpha = 0
  link_max = 0

  # Parse and check command line arguments...
  parser = argparse.ArgumentParser(prog=sys.argv[0], usage="python %(prog)s <configfile>")
  parser.add_argument('filename')
  try:
    args = parser.parse_args()
  except IOError:
    parser.print_help()
    sys.exit(2)
    
  try:
    f = open(args.filename)
  except IOError:
    print "Cannot open config file! Aborting..."
    sys.exit()

  g = Graph()

  num_nodes = 0
  topology = ""
  alpha = 0
  node_min = node_max=0
  link_min = link_max=0
  attempts = 1
  
  # Parse file line by line...
  for line in f:
    lhs, rhs = line.split(":")
    lhs = lhs.lower()
    #print lhs, rhs
    if (lhs == "nodes"):
      num_nodes = int(rhs)
      g.set_num_nodes(num_nodes)
    elif (lhs == "topology"):
      topology = str(rhs).strip().lower()
      #g.set_topology(str(rhs).strip().lower())  # removes leading and ending whitespace; makes lowercase
      g.set_topology(topology)
    elif ((lhs == "alpha") and (g.get_topology() == "random")):
      alpha = int(float(rhs)*100)
      g.set_alpha(alpha)
      #print g.get_topology() + " " + str(alpha) + " " + str(g.get_alpha())
      if ( (g.get_alpha() < 0) or (g.get_alpha() > 100) ):
        print "Invalid range for alpha! Must be a decimal from 0.0-1.0"
        sys.exit()
    elif (lhs == "node-min"):
      node_min = int(rhs)
      g.set_node_min(node_min)
      #g.set_node_min(int(rhs))
    elif (lhs == "node-max"):
      node_max = int(rhs)
      g.set_node_max(node_max)
      #g.set_node_max(int(rhs))
    elif (lhs == "link-min"):
      link_min = int(rhs)
      g.set_link_min(link_min)
      #g.set_link_min(int(rhs))
    elif (lhs == "link-max"):
      link_max = int(rhs)
      g.set_link_max(link_max)
      #g.set_link_max(int(rhs))
    else:
      continue

  f.close()
  
  """ Debug...
  print "nodes: " + str(g.get_num_nodes()) 
  print "topology: " + g.get_topology()
  print "alpha: " + str(g.get_alpha())
  print "link_max: " + str(g.get_link_max())
  """
  add_nodes_and_node_weights(g)

  if (g.get_topology() == "linear"):
    for i in range(0, g.get_num_nodes()-1):
      link_weight = int(random.uniform(g.get_link_min(), g.get_link_max()))
      g.add_edge(i,i+1,link_weight)
  elif (g.get_topology() == "full"):
    make_full(g)
  elif (g.get_topology() == "star"):
    hub_node = 0 
    for i in range(1, g.get_num_nodes()):    
      link_weight = int(random.uniform(g.get_link_min(), g.get_link_max()))
      g.add_edge(hub_node, i, link_weight)
  elif (g.get_topology() == "random"):
    if (g.get_alpha() == 100):
      make_full(g)  
    elif (g.get_alpha() == 0):
      """ Make no connections """
      pass
    else:
      # Random edges based on alpha
      generate_random_graph(g) 
      check_if_connected(g) 
      #attempts = 1
      # Keep trying to generate a connected graph...
      while not CONNECTED:  
        #print attempts, g.get_alpha(),
        #print CONNECTED
        attempts = attempts + 1
        del g
        g = Graph() # Start fresh....
        g.set_num_nodes(num_nodes) 
        g.set_topology(topology)
        g.set_alpha(alpha)
        g.set_node_min(node_min)
        g.set_node_max(node_max)
        g.set_link_min(link_min)
        g.set_link_max(link_max)
        add_nodes_and_node_weights(g)
        generate_random_graph(g)
        check_if_connected(g)

  # Write graph to file...
  save_graph(g)

# Debug....
  #print_graph(g) 
  #check_if_connected(g)
  #print attempts, g.get_alpha()
  #print CONNECTED
