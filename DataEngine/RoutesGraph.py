import networkx as nx
from geojson import Feature, FeatureCollection, MultiLineString, dumps, Point


class RoutesGraph:
	Graph = None

	def __init__(self):
		self.Graph = nx.Graph()
	
	def addEdge(self, src, dst, src_name, dst_name, src_type, dst_type):
		if (self.Graph.has_edge(src, dst)):
			self.Graph.edges[src, dst]['weight'] +=1
		
		else:
			self.Graph.add_edge(src, dst, weight = 1)
			self.Graph.nodes[src]['labels'] = src_name + " " + src_type;
			self.Graph.nodes[dst]['labels'] = dst_name + " " + dst_type;
		
	def writeToGeojson(self, filepath):
		features = []
		
		for u, v, d in self.Graph.edges(data=True):
			
			f = Feature(geometry=MultiLineString(
                		[[u, v]]), properties={"weight": d['weight']})

			features.append(f)
			
		for i, d in self.Graph.nodes(data=True):
			f = Feature(geometry=Point(i), properties={"name": d['labels']})
			
			features.append(f)

		routes = FeatureCollection(features)
		fd = open(filepath, "w")
		fd.write(dumps(routes, sort_keys=True))
		fd.close()


