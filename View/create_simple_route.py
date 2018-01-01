from geojson import Feature, FeatureCollection, MultiLineString, dumps
from openpyxl import load_workbook

wb = load_workbook(filename='miejscowosci.xlsx', read_only=True);
ws = wb['Arkusz1'];

cities = ['Kraków', 'Zakopane', 'Nowy Sącz', 'Tarnów'];
weights = ["1000", "200", "30"];
cities_coordinates = ["", "", "", ""];


for row in ws.rows:
	for i in range(0, len( cities)):
		if ((row[1].value == cities[i]) and (row[2].value == 'miasto')):
			high = row[14].value;
			length = row[15].value;
			
			high_converted = int(high[0:2]) + (float(high[3:5]) / 60) + (float(high[6:8])/3600);
			length_converted = int(length[0:2]) + (float(length[3:5]) / 60) + (float(length[6:8])/3600);
			
			cities_coordinates[i] = ((length_converted, high_converted));


features = [];
for i in range(0, len(cities_coordinates) - 1):
	f = Feature(geometry=MultiLineString(
		[[cities_coordinates[i], cities_coordinates[i + 1]]]), 
		properties={"weight": weights[i]});
		
	features.append(f);

	
my_featureS = FeatureCollection(features); 
	
f = open("lines.json", "w");
f.write(dumps(my_featureS, sort_keys=True));
f.close();
