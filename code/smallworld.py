from graph_tool.all import *
from random import *
from pylab import *  # for plotting


# Create a small world network using the Watts-Strogatz method.
# The algorithm creates a K-connected ring, with from N nodes, and then 
# rewires each edge with probability b to a random other node.
# N = Number of nodes to creates.
# K = Mean degree of the graph.
# b = Probability for each edge to be rewired. 
def watts_strogatz(N,K,b):
  g = Graph(directed = True)
  nodes = g.add_vertex(N)
  n_change = 0
  
  print "Watts-Strogatz:"
  print "Number of nodes: ", N
  print "Number of edges: ", K*N
  print "Rewiring chance: ", b
  
  # Connect the nodes into a ring
  for i in range(0, len(nodes)):
    for j in range(1, K+1):
      g.add_edge(g.vertex(i), g.vertex((i+j)%len(nodes)))
  
  
  # Rewire phase. We will walk through the nodes, then through the edges of 
  # that node. 
  # If random() is smaller then the given b, we rewire the edge. Rules:
  # 1. Dont rewire to self
  # 2. Dont duplicate an already existing connection           
  print "count:", g.num_edges()
  
  for i in range(0, len(nodes)):
    to_be_added = []
    to_be_removed = []
    
    for e in g.vertex(i).out_edges():
      
      if random() < b:
	r = range(0,len(nodes))
	r.remove(i)
	n_change +=1
	
	# Outward edges
	for oe in g.vertex(i).out_edges():
	  if r.count(g.vertex_index[oe.target()]) > 0:
	    r.remove(g.vertex_index[oe.target()])
	
	# Inward edges
	for ie in g.vertex(i).in_edges():
	  if r.count(g.vertex_index[ie.source()]) > 0:
	    r.remove(g.vertex_index[ie.source()])
	    
	# Already picked this round
	for ap in to_be_added:
	  if r.count(g.vertex_index[ap]) > 0:
	    r.remove(g.vertex_index[ap])
	
	# Randomly pick one of the possible vertices to rewire to.
	pick = choice(r)
	
	# Add the edges that are to be added and removed to lists. To be 
	# processed after all the edges of the vertex have been handled.
	to_be_added.append(g.vertex(choice(r)))
	to_be_removed.append(e)

    # Remove the obsolete edges, and add the new ones. This is the actual
    # rewiring.
    for o in to_be_removed:
      g.remove_edge(o)
      
    for o in to_be_added:
      new = g.add_edge(g.vertex(i), o)
      
      
      
  print "Edges rewired: ",n_change
      
  g.set_directed(False)
  return g

  
def draw_to_pdf(g):

  #graph_draw(g, vprops={"label": g.vertex_index}, output="ring.pdf")
  graph_draw(g, size=(15,30), penwidth=0.2,
  output="../graphs/watts-10000-4-0.2.pdf")
  
  

#draw_to_pdf(watts_strogatz(1000,3,0.20))

def save(g):
  g.save("graph.xml.gz")

 
def plot(g):
# now we have a graph!
# let's calculate its in-degree distribution and plot it to a file
  tot_hist = vertex_hist(g, "total")

  figure(figsize=(4, 3))
  errorbar(tot_hist[1][:-1], tot_hist[0], fmt="o", yerr=sqrt(tot_hist[0]),
           label="tot")
  gca().set_yscale("log")
  gca().set_xscale("log")
  gca().set_ylim(1e-1, 1e5)
  gca().set_xlim(0.8, 1e3)
  subplots_adjust(left=0.2, bottom=0.2)
  xlabel("$k_{tot}$")
  ylabel("$NP(k_{tot})$")
  savefig("random-deg-hist10.pdf")

g = watts_strogatz(10000, 4, 0.2)
draw_to_pdf(g)
save(g)
#plot(g) 
