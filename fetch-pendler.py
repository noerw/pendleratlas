import sys
import json
import requests

pendlerUrl = 'https://statistik.arbeitsagentur.de/PendlerData'
pendlerParams = { 'year_month' : '201706', 'view' : 'renderPendler' }

f = open('kreise.json', 'r')
kreise = f.read()
f.close()
geojson = json.loads(kreise)

while not all('auspendler' in f['properties'] for f in geojson['features']):
    for i in range(len(geojson['features'])):
        f = geojson['features'][i];

        if 'auspendler' in f['properties']:
            continue
        else:
            print 'fetching', f['properties']['ID'], i

        pendlerParams['regionInd'] = f['properties']['ID']

        try:
            pendlerParams['type'] = 'ein'
            r = requests.get(pendlerUrl, params=pendlerParams)
            f['properties']['einpendler'] = json.loads(r.text)

            pendlerParams['type'] = 'aus'
            r = requests.get(pendlerUrl, params=pendlerParams)
            f['properties']['auspendler'] = json.loads(r.text)

        except KeyboardInterrupt:
            sys.exit(1)
        except:
            print 'errored at', i
            continue

f = open('pendler.json', 'w')
f.write(json.dumps(geojson))
f.close()
