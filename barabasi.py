#! /usr/bin/env python

# We probably will need some things from several places
import sys, os
from pylab import *  # for plotting
from numpy.random import *  # for random sampling
seed(42)

# We need to import the graph_tool module itself
from graph_tool.all import *

# let's construct a scale-free network. It is
# a directed network, with preferential attachment. The algorithm below is
# very naive, and a bit slow, but quite simple.

# We start with an empty, directed graph
g = Graph()

# We want also to keep the age information for each vertex and edge. For that
# let's create some property maps
v_age = g.new_vertex_property("int")
e_age = g.new_edge_property("int")

# The final size of the network
N = 10

# We have to start with one vertex
v = g.add_vertex()
v_age[v] = 0

# we will keep a list of the vertices. The number of times a vertex is in this
# list will give the probability of it being selected.
vlist = [v]

# let's now add the new edges and vertices
for i in xrange(1, N):
    # create our new vertex
    v = g.add_vertex()
    v_age[v] = i

    # we need to sample a new vertex to be the target, based on its in-degree +
    # 1. For that, we simply randomly sample it from vlist.
    i = randint(0, len(vlist))
    target = vlist[i]

    # add edge
    e = g.add_edge(v, target)
    e_age[e] = i

    # put v and target in the list
    vlist.append(target)
    vlist.append(v)

# now we have a graph!
# let's calculate its total-degree distribution and plot it to a file
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
savefig("scale-free-deg-hist10.pdf")

# let's do a random walk on the graph and print the age of the vertices we find,
# just for fun.
v = g.vertex(randint(0, g.num_vertices()))
while True:
    print "vertex:", v, "in-degree:", v.in_degree(), "out-degree:",\
          v.out_degree(), "age:", v_age[v]

    if v.out_degree() == 0:
        print "Nowhere else to go... We found the main hub!"
        break

    n_list = []
    for w in v.out_neighbours():
        n_list.append(w)
    v = n_list[randint(0, len(n_list))]

# let's save our graph for posterity. We want to save the age properties as
# well... To do this, they must become "internal" properties:
g.vertex_properties["age"] = v_age
g.edge_properties["age"] = e_age

# now we can save it
#g.save("graph.xml.gz")

# now we can draw it
#g = load_graph("graph.xml.gz")
#age = g.vertex_properties["age"]
#graph_draw(g, size=(15,15), vcolor=age, output="graph.pdf")

