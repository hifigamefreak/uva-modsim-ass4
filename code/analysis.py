from graph_tool.all import *
import sys, os

g = load_graph("graph.xml.gz")

print "Clustering coefficient: ", global_clustering(g)
print "Diameter:" , distance_histogram(g)[1][-2]
print "Average degree (total):", vertex_average(g, "total")[0]
print "Max degree (total):", vertex_hist(g, "total")[1][-2]

