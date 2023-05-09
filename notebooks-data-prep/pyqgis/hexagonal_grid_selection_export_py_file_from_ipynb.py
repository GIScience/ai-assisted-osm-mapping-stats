#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os



# In[2]:


os.chdir("..") # return to the main directory
home_wd = os.getcwd()
home_wd


# In[3]:


state_dic = {
    0: "India",
    1: "Vietnam",
    2: "Tanzania",
    3: "Kenya",
    4: "Nigeria"
}


# In[4]:


# user input definition

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


# In[5]:


in_grid = os.path.join(home_wd, r"shp\origin_downloaded_layers\heigit_hexagrid.shp")
in_states = os.path.join(home_wd, r"shp\origin_downloaded_layers\ne_10m_admin_0_sovereignty.shp")
out_grid_geojson = os.path.join(home_wd, f"geojson-hexagrid-states\\{state_dic[user_data_spec]}", "")

temp_shp = os.path.join(home_wd,r"shp\temporary-shp", "")


# In[6]:


out_grid_geojson


# In[7]:


# get the data types

field_info = arcpy.Describe(in_grid).fields

for field in field_info:
    print(f"{field.name}: {field.type}")




field = arcpy.AddFieldDelimiters(in_states, "NAME_EN")
selection = "{field} = '{val}'".format(field=field, val=state_dic[user_data_spec])
sel_state = arcpy.management.SelectLayerByAttribute(in_states, "NEW_SELECTION", 
                                        selection)


# In[12]:


sel_state_grids = arcpy.management.SelectLayerByLocation(in_grid,
                                                        "INTERSECT",
                                                        sel_state ,
                                                        None,
                                                        "NEW_SELECTION")


# In[13]:


count = 0
with arcpy.da.SearchCursor(sel_state_grids, ['id_int']) as cursor:
    for row in cursor:
        count+=1
count


# In[14]:



# In[17]:


with arcpy.da.SearchCursor(sel_state_grids, ["id_int", "SHAPE@"]) as cur:
    for row in cur:
        arcpy.conversion.FeaturesToJSON(row[1],
        f"{out_grid_geojson}{row[0]}_{state_dic[user_data_spec]}.geojson",
        geoJSON=True)
