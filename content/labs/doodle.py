#%%
import osgeo.ogr
import math
import os
#%%
os.chdir('content/labs/data/python_geospatial_development_westra')
os.listdir()
#%%
shapefile = osgeo.ogr.Open("tl_2009_us_state.shp")
numLayers = shapefile.GetLayerCount()

print("Shapefile contains %d layers" % numLayers)
print()

for layerNum in range(numLayers):
    layer = shapefile.GetLayer(layerNum)
    spatialRef = layer.GetSpatialRef().ExportToProj4()
    numFeatures = layer.GetFeatureCount()
    print("Layer %d has spatial reference %s" % (layerNum, spatialRef))
    print("Layer %d has %d features:" % (layerNum, numFeatures))
    print()

    for featureNum in range(numFeatures):
        feature = layer.GetFeature(featureNum)
        featureName = feature.GetField("NAME")
        print("Feature %d has name %s" % (featureNum, featureName))
#%%
shapefile = osgeo.ogr.Open("tl_2009_us_state.shp")
layer = shapefile.GetLayer(0)
feature = layer.GetFeature(2)

print("Feature 2 has the following attributes:")
print()

attributes = feature.items()

for key,value in attributes.items():
    print("  %s = %s" % (key, value))
    print()

geometry = feature.GetGeometryRef()
geometryName = geometry.GetGeometryName()

print("Feature's geometry data consists of a %s" % geometryName)
#%%


def analyze_geometry(geometry, indent=0):
    s = ["  " * indent, geometry.GetGeometryName()]
    if geometry.GetPointCount() > 0:
        s.append(" with %d data points" % geometry.GetPointCount())
    if geometry.GetGeometryCount() > 0:
        s.append(" containing:")

    print("".join(s))

    for i in range(geometry.GetGeometryCount()):
        analyze_geometry(geometry.GetGeometryRef(i), indent+1)


shapefile = osgeo.ogr.Open("tl_2009_us_state.shp")
layer = shapefile.GetLayer(0)
feature = layer.GetFeature(53)
print("Feature", feature.GetField("NAME"), "is represented by a")
geometry = feature.GetGeometryRef()

analyze_geometry(geometry)
#%%


def find_points(geometry, results):
    for i in range(geometry.GetPointCount()):
        x, y, z = geometry.GetPoint(i)
        if results['north'] is None or results['north'][1] < y:
            results['north'] = (x, y)
        if results['south'] is None or results['south'][1] > y:
            results['south'] = (x, y)

    for i in range(geometry.GetGeometryCount()):
        find_points(geometry.GetGeometryRef(i), results)


shapefile = osgeo.ogr.Open("tl_2009_us_state.shp")
layer = shapefile.GetLayer(0)
feature = layer.GetFeature(53)
geometry = feature.GetGeometryRef()

results = {'north': None,
           'south': None}

find_points(geometry, results)

print("Northernmost point is (%0.4f, %0.4f)" % results['north'])
print("Southernmost point is (%0.4f, %0.4f)" % results['south'])
#%%
lat1 = 42.0095
long1 = -122.3782

lat2 = 32.5288
long2 = -117.2049

rLat1 = math.radians(lat1)
rLong1 = math.radians(long1)
rLat2 = math.radians(lat2)
rLong2 = math.radians(long2)

dLat = rLat2 - rLat1
dLong = rLong2 - rLong1
a = math.sin(dLat/2)**2 + math.cos(rLat1) * math.cos(rLat2) \
                        * math.sin(dLong/2)**2
c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
distance = 6371 * c

print("Great circle distance is %0.0f kilometers" % distance)