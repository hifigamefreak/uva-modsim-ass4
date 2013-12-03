from graph_tool.all import *
from random import *
import smallworld

def create_network():
  g = smallworld.watts_strogatz(50, 2, 0.0)
  
  vprop_state = g.new_vertex_property("int")
  vprop_new_state = g.new_vertex_property("int")
  
  g.vertex_properties["state"] = vprop_state
  g.vertex_properties["new_state"] = vprop_new_state
  
  # Assign states to all the vertices. A state consists of 2 integers.
  # First integer is the state, 3=Susceptible, 0=infected, 1=recovered, 2=dead.
  # This strange order of states has to do with the way graph_tool assigns 
  # colors. Could be done more elegantly, but this is no priority
  # The second integer is the time the state has been unchanged. Used to 
  # determine if people become resistant. 
  for v in g.vertices():
    g.vertex_properties["state"][v] = 3
  
  return g
   
  
def SIR_process(g, steps, Pinf, Pdeath, Precover, verbose, export):
  
  if export:
    SIR_draw(g)
 
  if verbose:
    print "Start: ", SIR_status(g)
    
  for i in range(0,steps):
    SIR_step(g, Pinf, Pdeath, Precover)
    
    if export:
      SIR_draw(g, i+1)
      
    if verbose:
      print i+1,": " , SIR_status(g)
  
  
def SIR_infect_random(g, n_inf): 
  
  r = range(0, g.num_vertices())
  s = sample(r, n_inf)
  print "Infecting ", n_inf, " vertices."
  for i in s:
    g.vertex_properties["state"][g.vertex(i)] = 0
  print "Infected: ", s
  
  
def SIR_resistant_random(g, n_inf): 
  
  r = range(0, g.num_vertices())
  s = sample(r, n_inf)
  print "Making resistant ", n_inf, " vertices."
  for i in s:
    g.vertex_properties["state"][g.vertex(i)] = 1
  print "Resistant: ", s
  
  
  
def SIR_step(g, Pinf, Pdeath, Precover):
  
  for v in g.vertices():
    g.vertex_properties["new_state"][v] = g.vertex_properties["state"][v]
  
  # Calculate all the state changes
  for v in g.vertices():
    for w in v.out_neighbours():
      if (g.vertex_properties["state"][v] == 3 and g.vertex_properties["state"][w] == 0 and random() < Pinf):
	g.vertex_properties["new_state"][v] = 0
	
    if (g.vertex_properties["state"][v] == 0):
      if (random() < Pdeath):
	g.vertex_properties["new_state"][v] = 2
      elif (random() < Precover):
	g.vertex_properties["new_state"][v] = 1

  # Commit all the state changes
  for v in g.vertices():
    g.vertex_properties["state"][v] = g.vertex_properties["new_state"][v]
    

    
def SIR_status(g):
  
  status = [0]*4
  
  for v in g.vertices():
    status[g.vertex_properties["state"][v]] += 1
    
  return status
  
def SIR_draw(g, i=0): 
  state = g.vertex_properties["state"]
  graph_draw(g, layout="twopi",pin=False, vnorm=True, vsize=0.4, size=(15,15), penwidth=1.0, vcolor=state, output=str(i)+"SIR.pdf")
  
n = create_network()
print SIR_status(n)
SIR_infect_random(n, 1)
SIR_resistant_random(n, 2)
print SIR_status(n)
SIR_process(n, 10, 0.3, 0.05, 0.05, True, True)
