from RoutesGraph import RoutesGraph
from openpyxl import load_workbook

Rg = RoutesGraph()
wb = load_workbook(filename='miejscowosci.xlsx', read_only=True);
ws = wb['Arkusz1'];

routes = [ 	['Kraków', 'Zakopane', 'Nowy Sącz', 'Tarnów'],
	  	['Kraków', 'Zakopane'],
		['Kraków', 'Zakopane'],
		['Kraków', 'Zakopane'],
		['Kraków', 'Zakopane'],
		['Kraków', 'Zakopane'],
]

cords = []

for route in routes:
	cords.append([])
	for place in route:
		for row in ws:
			if ((row[1].value == place) and (row[2].value == 'miasto')):
				high = row[14].value;
				length = row[15].value;
				
				high_converted = int(high[0:2]) + (float(high[3:5]) / 60) + (float(high[6:8])/3600);
				length_converted = int(length[0:2]) + (float(length[3:5]) / 60) + (float(length[6:8])/3600);

				cords[-1].append((length_converted, high_converted))


for route in cords:
	for i in range(0, len(route) - 1):
		Rg.addEdge(route[i], route[i + 1])


Rg.writeToGeojson("lines.json")
