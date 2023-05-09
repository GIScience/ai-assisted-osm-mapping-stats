from qgis.core import *
from qgis.processing import *

names = [layer.name() for layer in QgsProject.instance().mapLayers().values()]
names

# Get the active layer list
project = QgsProject.instance()
layers = project.mapLayers().values()
states = project.mapLayersByName('ne_10m_admin_0_sovereignty')[0]
grid = project.mapLayersByName('isea_grid_with_buildings (1) — isea_grid_2023')[0]

states.selectByExpression('"NAME_EN" IN(\'India\', \'Vietnam\', \'Tanzania\', \'Kenya\', \'Nigeria\')')

processing.run("native:selectbylocation", 
{'INPUT':'C:/Users/milan/Desktop/isea_grid_with_buildings (1).gpkg|layername=isea_grid_2023',
'PREDICATE':[0],
'INTERSECT':QgsProcessingFeatureSourceDefinition('C:/Users/milan/OneDrive - MUNI/VŠ/PhD/Zahraniční stáž/Work/HeiGIT_notebooks/analysis/ai-assisted-osm-mapping-stats/shp/origin_downloaded_layers/ne_10m_admin_0_sovereignty.shp',
selectedFeaturesOnly=True, 
featureLimit=-1,
geometryCheck=QgsFeatureRequest.GeometryAbortOnInvalid),
'METHOD':0})

