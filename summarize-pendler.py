import json

f = open('pendler.json', 'r')
kreise = f.read()
f.close()
geojson = json.loads(kreise)

for f in geojson['features']:
    f['properties']['poptotal']  = f['properties']['einpendler']['svb']['anzahl']
    f['properties']['popmale']   = f['properties']['einpendler']['svb']['maenner']
    f['properties']['popfemale'] = f['properties']['einpendler']['svb']['frauen']

    f['properties']['pendintotal']  = f['properties']['einpendler']['gesamt']['anzahl']
    f['properties']['pendinmale']   = f['properties']['einpendler']['gesamt']['maenner']
    f['properties']['pendinfemale'] = f['properties']['einpendler']['gesamt']['frauen']

    f['properties']['pendouttotal']  = f['properties']['auspendler']['gesamt']['anzahl']
    f['properties']['pendoutmale']   = f['properties']['auspendler']['gesamt']['maenner']
    f['properties']['pendoutfemale'] = f['properties']['auspendler']['gesamt']['frauen']

    f['properties'].pop('einpendler', None)
    f['properties'].pop('auspendler', None)

f = open('pendler-summary.json', 'w')
f.write(json.dumps(geojson))
f.close()
