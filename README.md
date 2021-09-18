## Download Locations
- [Florida Department of Revenue](https://floridarevenue.com/property/Pages/DataPortal_RequestAssessmentRollGISData.aspx)
- [Flood Zones](https://www.fema.gov/national-flood-hazard-layer-nfhl#)
- [National Wetlands](https://www.fws.gov/wetlands/data/Data-Download.html)

### Topology
- [National Map](https://viewer.nationalmap.gov/basic/)

### Superfund/Brownfield
- [EPA](https://www.epa.gov/frs/geospatial-data-download-service)
- [Flordia](http://geodata.myflorida.com/datasets/FDACS::brownfield-sites-2019)

### Soil Data
- [NRCS](https://nrcs.app.box.com/v/soils)
- [Soil Web](https://gdg.sc.egov.usda.gov/GDGHome_DirectDownLoad.aspx)
- [Soil Web App](https://casoilresource.lawr.ucdavis.edu/soilweb-apps)

See also https://casoilresource.lawr.ucdavis.edu/gmap/

### Opportunity Zones
- [Resources](https://www.cdfifund.gov/Pages/Opportunity-Zones.aspx)

### Zoning
Zoning data is maintained at the city level for incorporated areas and county level for unincorporated ones.  Larger cities publish zoning maps. Some use Arcgis layers others publish pdf documents.  Each map is a separate site.  For example, in Brevard County Florida there are 17 different zoning authorities:
1. Cape Canaveral - no map [website](https://www.cityofcapecanaveral.org/)
2. Cocoa Beach - https://www.cityofcocoabeach.com/DocumentCenter/View/3271/Ord1614-Zoning-Map-Citywide-PDF?bidId=
3. Cocoa - https://cocoacity.maps.arcgis.com/home/webmap/viewer.html?webmap=531ff8bc709a4f08bfc9e732c76cebaa
4. Grant-Valkaria - no map [website](https://grantvalkaria.org/bc-planning-and-zoning)
5. Indialantic - https://www.indialantic.com/wp-content/uploads/zoning-map.pdf
6. India Harbour Beach - no map [website](https://www.indianharbourbeach.org/)
7. Malabar - no map [website](https://www.townofmalabar.org/planning-zoning-board)
8. Melbourne - https://mgis.maps.arcgis.com/apps/webappviewer/index.html?id=3f1f8b678a754f74ab7a58ba33c7911f
9. Melbourne Beach - https://www.melbournebeachfl.org/sites/melbournebeachfl/files/uploads/zoning_map.pdf
10. Melbourne Village - no map [website](https://melbournevillage.org/)
11. West Melbourne - https://www.westmelbourne.org/DocumentCenter/View/2918/Zoning?bidId= [landing page](https://www.westmelbourne.org/261/City-Maps)
11. Palm Bay - https://gis.palmbayflorida.org/portal/apps/webappviewer/index.html?id=c263a4dbd1834bc2a73b97f1bb88e2d5
12. Palm Shores - http://www.townofpalmshores.org/sites/palmshoresfl/files/uploads/zoning_map.pdf [landing page](http://www.townofpalmshores.org/planning-zoning-board/pages/planning-zoning-maps)
13. Rockledge - https://www.cityofrockledge.org/DocumentCenter/View/442/2014-Zoning-Map-PDF
14. Satellite Beach - http://www.satellitebeach.org/Departments/Zoning%20Map%20no%20CM%2012-14-17.pdf
15. Titusville - https://titusville.maps.arcgis.com/apps/webappviewer/index.html?id=993da359767b455fa2e98c82bcc6331e
16. Unincorporated Brevard County - http://www.arcgis.com/apps/webappviewer/index.html?id=8401fea35fda4415aa48f0dfe861ccdc&extent=-9060424.6779%2C3250925.5042%2C-8913665.5836%2C3321171.1332%2C102100 (https broken)

Shape files:

1. https://hub.arcgis.com/datasets/titusville::zoning
2. https://hub.arcgis.com/datasets/titusville::future-land-use
3. https://hub.arcgis.com/datasets/brevardbocc::zoning

### Example upload

Git Clone the [GDAL Docker Images repo](https://github.com/OSGeo/gdal/tree/master/gdal/docker) and build a local image or use a pre-built [image from DockerHub]( https://hub.docker.com/r/osgeo/gdal/tags?page=1&ordering=last_updated)

```
docker run --rm -v /home:/home osgeo/gdal:alpine-normal-latest ogrinfo \
 ES:https://elastic:1vqDKypyMc09s74KuREy9Af78b792fa42745d798050773a213c120.us-central1.gcp.cloud.es.io:9243

docker run --rm -v /home:/home osgeo/gdal:alpine-normal-latest ogr2ogr \
 -lco INDEX_NAME=wetlands -lco NOT_ANALYZED_FIELDS={ALL} -lco WRITE_MAPPING=./wetlands-mapping.json \
 ES:https://elastic:1vqDKypyMc09s74KuREy9ADM@f78b792fa42745d798050773a213c120.us-central1.gcp.cloud.es.io:9243 \
 FL_Wetlands.shp

docker run --rm -v /home:/home osgeo/gdal:alpine-normal-latest ogr2ogr \
  ES:https://elastic:1vqDKypyMc09s74KuREy9Af78b792fa42745d798050773a213c120.us-central1.gcp.cloud.es.io:9243 \
  FL_Wetlands.shp

docker run --rm -v $PWD:/home osgeo/gdal:alpine-normal-latest ogr2ogr \
   -lco INDEX_NAME=floodmap -lco NOT_ANALYZED_FIELDS={ALL} -lco WRITE_MAPPING=/home/floodmap-mapping.json -skipfailures \
   ES:https://elastic:1vqDKypyMc09s74KuREy9ADM@f78b792fa42745d798050773a213c120.us-central1.gcp.cloud.es.io:9243 \
 /home/S_FLD_HAZ_AR.shp

docker run --rm -v $PWD:/home osgeo/gdal:alpine-normal-latest ogr2ogr \
-lco INDEX_NAME=floodmap -lco OVERWRITE_INDEX=YES -lco MAPPING=/home/floodmap-mapping.json -skipfailures \
ES:https://elastic:1vqDKypyMc09s74KuREy9Af78b792fa42745d798050773a213c120.us-central1.gcp.cloud.es.io:9243 \
/home/S_FLD_HAZ_AR.shp

curl -X PUT https://elastic:1vqDKypyMc09s74KuREy9ADM@f78b792fa42745d798050773a213c120.us-central1.gcp.cloud.es.io:9243/floodmap \
-d @floodmap-mapping.json -H 'Content-Type: application/json'

docker run --rm -v /Users:/Users osgeo/gdal:alpine-normal-latest ogr2ogr -skipfailures \
ES:https://elastic:1vqDKypyMc09s74KuREy9Af78b792fa42745d798050773a213c120.us-central1.gcp.cloud.es.io:9243 \
$PWD/FL_Wetlands.shp

docker run --rm -v /Users:/Users osgeo/gdal:alpine-normal-latest ogr2ogr -skipfailures \
ES:https://elastic:1vqDKypyMc09s74KuREy9Af78b792fa42745d798050773a213c120.us-central1.gcp.cloud.es.io:9243 \
$PWD/gNATSGO_FL.gdb

docker run --rm -v /Users:/Users osgeo/gdal:alpine-normal-latest ogr2ogr -skipfailures \
ES:https://elastic:1vqDKypyMc09s74KuREy9Af78b792fa42745d798050773a213c120.us-central1.gcp.cloud.es.io:9243 \
$PWD/Brownfield_Sites_2019.shp

docker run --rm -v $PWD:/home osgeo/gdal:alpine-normal-latest ogr2ogr -skipfailures \
ES:https://elastic:1vqDKypyMc09s74KuREy9Af78b792fa42745d798050773a213c120.us-central1.gcp.cloud.es.io:9243 \
/home/S_FLD_HAZ_AR.shp
```
