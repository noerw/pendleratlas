# Pendleratlas Scraper

Die Bundesagentur fuer Arbeit stellt die Pendlerstatistik von 2016 als
interaktive Karte auf ihrer [Website][Pendleratlas] bereit.

Diese Statistik bietet die detailliertesten Informationen zu Pendlern auf Bundesebene welche ich finden konnte:
Es werden kreisuebergreifende Ein- / Auspendler fuer jeden Kreis, gegliedert nach Pendler-Ziel sowie Geschlecht geliefert.
Ebenfalls ist die Wohnpopulation und Gesamt-Pendlermenge jedes Kreises angegeben.
Anders als in den [Veroeffentlichungen von DeStatis][Destatis] werden hier also auch die exakten Ziel-Kreise der Pendler, sowie exakte Angaben gemacht.

Daten auf Gemeinde-Ebene mit zusaetzlichen Attributen (Beschaeftigungsart, Wirtschaftsbereich) wie im [Pendleratlas-NRW][PendleratlasNRW] liegen leider nicht vor.

## PendlerDaten API
Um selbst mit den Daten *arbeiten* zu koennen kann es nuetzlich sein, sie nicht nur auf einer Karte zu betrachten.
Diese python Skripte laden die Pendlerstatistik automatisiert herunter und exportiert sie als GeoJSON bzw Shapefile.
Die zugehoerige API liegt unter `https://statistik.arbeitsagentur.de/PendlerDaten?` ([Beispiel][PendlerBsp]).

[Pendleratlas]: https://statistik.arbeitsagentur.de/Navigation/Statistik/Statistische-Analysen/Interaktive-Visualisierung/Pendleratlas/Pendleratlas-Nav.html
[Destatis]: https://www-genesis.destatis.de/gis/genView?SRC=4&TABLE=254-39-4
[PendleratlasNRW]: https://www.pendleratlas.nrw.de/

[PendlerBsp]: https://statistik.arbeitsagentur.de/PendlerData\?type\=ein\&year_month\=201606\&regionInd\=05754\&view\=renderPendler

> **Disclaimer**: Dieses Projekt ist in keiner Weise mit destatis oder der Arbeitsagentur verbunden. Ich garantiere und hafte fuer nichts bezueglich der hier bereitgestellten Daten und Skripte. Es wurden ausschliesslich oeffentlich zugaengliche APIs dokumentiert.

### IDs der Kreise
Die API referenziert die Kreise ueber IDs welche von einem ESRI ArcGIS MapServer (?) unter
`http://geois.arbeitsagentur.de/arcgis/rest/services/Gebietsstrukturen/MapServer/3` liegen.

Dieses Layer laesst sich als GeoJSON mitsamt Kreis IDs, Geometrien und Namen mit folgendem Befehl beziehen:

```bash
wget "http://geois.arbeitsagentur.de/arcgis/rest/services/Gebietsstrukturen/MapServer/3/query?f=geojson&where=valid_from <= CURRENT_DATE AND valid_to >= CURRENT_DATE&returnGeometry=true&spatialRel=esriSpatialRelIntersects&outFields=ID,region,OBJECTID,parentID&outSR=4326" -O kreise.json

# oder 
python fetch-kreise.py > kreise.json
```

> Es stellt sich heraus, dass die von der PendlerDaten API erwarteten Kreis IDs aus dem Attribut `RS` der [Verwaltungsgrenzen (`vg250_krs`) des Geodatenzentrums][Verwaltungsgrenzen] sind. Falls also die exakte Geometrie der Kreise benoetigt wird, kann man das sicherlich auch diesen Datensatz als Grundlage wahlen.

[Verwaltungsgrenzen]: https://www.geodatenzentrum.de/geodaten/gdz_rahmen.gdz_div?gdz_spr=deu&gdz_akt_zeile=5&gdz_anz_zeile=1&gdz_unt_zeile=14&gdz_user_id=0

### Pendlerdaten
Das Skript `fetch-pendler.py` erwartet die Gemeindegrenzen `kreise.json` im selben Ordner, und fragt die API der Arbeitsagentur fuer jeden Kreis ab.
Dies dauert ne ganze Weile, da die API langsam und instabil ist. Fehlgeschlagene Requests werden wiederholt bis alles da ist.
Das Skript augmentiert das zuvor bezogene `kreise.json` und speichert als `pendler.json`

Es werden die Attribute `einpendler` und `auspendler` in den Properties jedes Features angelegt.
Diese sehen dann wie folgt aus:

```js
"properties": {
  "ID": "05910",
  "region": "Hömmelebömmele",

  // einpendler je kreis ID
  "einpendler": {
    "05913": {
      "frauen": 1838,
      "anzahl": 4573,
      "maenner": 2735
    },
    "05911": {
      "frauen": 1265,
      "anzahl": 3220,
      "maenner": 1955
    },

    // .... alle anderen kreise

    // gesamt pendler
    "gesamt": {
      "frauen": 19865,
      "anzahl": 52456,
      "maenner": 32591
    },
    // wohnbevoelkerung des kreises
    "svb": {
      "frauen": 95155,
      "anzahl": 211028,
      "maenner": 115873
    }
  },

  "einpendler": { ... }
}
```

### Shapefile
Eine Zusammenfassung der Daten (Pendlergesamtaufkommmen pro Kreis) als Shapefile laesst sich folgendermassen generieren:

```bash
python summarize-pendler.py
ogr2ogr pendler.shp pendler-summary.json
```

# Lizenz
- Code: public domain
- pendler.shp, pendler.json, kreise.json: © GeoBasis-DE / BKG 2016 (Daten verändert)
- Pendlerdaten: unbekannt
