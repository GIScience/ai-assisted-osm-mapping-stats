import os
from qgis.core import (
    QgsVectorLayer,
    QgsProject,
    QgsExpression,
    QgsExpressionContext,
    QgsFeatureRequest,
    QgsGeometry,
    QgsFeature,
)


# Set the project home directory
os.chdir("..")
home_wd = os.getcwd()

state_dic = {
    0: "India",
    1: "Vietnam",
    2: "Tanzania",
    3: "Kenya",
    4: "Nigeria",
}

while True:
    try:
        user_data_spec = int(input("Which grid data do you want to split?\
                            Enter a number:\
                            0 for India,\
                            1 for Vietnam,\
                            2 for Tanzania,\
                            3 for Kenya,\
                            4 for Nigeria,\
                                :"
                                ))
    except ValueError:
        print("Please enter a number.")
        continue
    if user_data_spec not in range(len(state_dic)):
        print(f"Please enter one of these numbers: {state_dic.keys()}.")
        continue
    break
user_data_spec = 2
# Define the input and output files
in_grid = os.path.join(home_wd, "shp", "origin_downloaded_layers", "heigit_hexagrid.shp")
in_states = os.path.join(home_wd, "shp", "origin_downloaded_layers", "ne_10m_admin_0_sovereignty.shp")
out_grid_geojson = os.path.join(home_wd, "geojson-hexagrid-states", state_dic[user_data_spec])

project = QgsProject.instance()

# Create a QGIS vector layer from the input grid file
grid_layer = QgsVectorLayer(in_grid, "Grid", "ogr")
if not grid_layer.isValid():
    print("Grid layer not valid!")
    exit()

# Create a QGIS vector layer from the input states file
state_layer = QgsVectorLayer(in_states, "States", "ogr")
if not state_layer.isValid():
    print("State layer not valid!")
    exit()

project.addMapLayer(grid_layer)
project.addMapLayer(state_layer)

# Define the state to be processed
state_name = state_dic[user_data_spec]

# Create an expression to select the desired state
exp_context = QgsExpressionContext()
exp_context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(state_layer))
exp_context.appendScopes(QgsExpressionContextUtils.projectScopes())
exp_context.setVariable("state_name", state_name)
state_exp = QgsExpression('NAME_EN = \'' + state_name + '\'')
state_exp.prepare(exp_context)

# Select the state features based on the expression
state_layer.selectByExpression(state_exp)

# Create an empty list to store the selected grid features
selected_features = []

# Iterate through the selected state features and select the corresponding grid features
for state_feat in state_layer.selectedFeatures():
    state_geom = state_feat.geometry()
    grid_request = QgsFeatureRequest().setFilterRect(state_geom.boundingBox())
    for grid_feat in grid_layer.getFeatures(grid_request):
        if grid_feat.geometry().intersects(state_geom):
            selected_features.append(grid_feat)

# Iterate through the selected grid features and export them to GeoJSON files
for grid_feat in selected_features:
    grid_geom = grid_feat.geometry()
    grid_id = grid_feat["id_int"]
    out_file = os.path.join(out_grid_geojson, f"{grid_id}_{state_name}.geojson")
    with open(out_file, "w") as f:
        f.write(grid_geom.asJson())