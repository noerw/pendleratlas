import requests

kreiseUrl = 'http://geois.arbeitsagentur.de/arcgis/rest/services/Gebietsstrukturen/MapServer/3/query'
kreiseParams = {
        'f' : 'geojson',
        'returnGeometry' : 'true',
        'spatialRel' : 'esriSpatialRelIntersects',
        'outSR' : '4326',
        'outFields' : 'ID,region',
        'where' : 'valid_from <= CURRENT_DATE AND valid_to >= CURRENT_DATE'
        }

r = requests.get(kreiseUrl, params=kreiseParams)

print(r.text)
