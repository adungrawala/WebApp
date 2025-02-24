import streamlit as st
import pandas as pd
import folium 
from streamlit_folium import st_folium
from folium import plugins
import geopandas
import leafmap.foliumap as leafmap

if "center" not in st.session_state:
    layout = "wide"
else:
    layout = "centered" if st.session_state.center else "wide"

st.set_page_config(layout=layout)

st.checkbox(
    "Viewing on a mobile?", key="center", value=st.session_state.get("center", False)
)

st.header("City of Waterloo")

   
   
Roads_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/Roads/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

waterloo_boundary_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/CityBoundary/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

gdf_park_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/Parks/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

gdf_trails_pathways_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/Trails_and_Pathways/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

SportField_Diamond_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/SportsFieldsDiamonds/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

Schools_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/Schools/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

Points_Interest_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/PointsOfInterest/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

Parking_Spots_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/ParkingLots/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

ION_Stops_url = "https://utility.arcgis.com/usrsvcs/servers/f063d1fb147847f796ce8c024e117419/rest/services/OpenData/OpenData/MapServer/5/query?outFields=*&where=1%3D1&f=geojson"


@st.cache_data
def read_gdf(gdf_url):
    
    gdf = geopandas.read_file(gdf_url)
    return gdf

basemap = st.selectbox("Select the basemap of your choice", ("openstreetmap","CartoDB Positron","Cartodb dark_matter"), placeholder="Select the basemap")
m = folium.Map(location=[43.462400, -80.520811], tiles=basemap, zoom_start=13, zoom_control=True, control_scale=True, key="waterloomap")

 #Adding waterloo square location marker

def Add_CityData():
    
    if(basemap != "Cartodb dark_matter"):

        folium.GeoJson(read_gdf(waterloo_boundary_url), overlay=True, style_function=lambda feature: {'color': 'black', 
            'weight': 2,  'fillOpacity': 0.1, 'border': 1}).add_to(m)
        
        folium.GeoJson(read_gdf(Roads_url), overlay=True, style_function=lambda feature: {'color': 'black',
            'weight': 1}).add_to(m)
    else:
        folium.GeoJson(read_gdf(waterloo_boundary_url), overlay=True, style_function=lambda feature: {'color': 'yellow', 
            'weight': 2,  'fillOpacity': 0.1, 'border': 1}).add_to(m)
        folium.GeoJson(read_gdf(Roads_url), overlay=True, style_function=lambda feature: {'color': 'yellow',
            'weight': 1}).add_to(m)
    
    folium.Marker(
    location=[43.462400, -80.520811],
    popup="City of Waterloo",
    tooltip="Waterloo, Ontario",
    ).add_to(m)   

#adding location control
folium.plugins.LocateControl().add_to(m)



# adding park data to popup#
def GeneratePopup_ToolTip(fields, tooltip):
     
    #adding popup values
    popup = folium.GeoJsonPopup(
    fields= fields,
    localize=True,
    labels=True,
    style="background-color: yellow;",
    )
    
    #adding tooltip
    tooltip = folium.GeoJsonTooltip(
    fields=tooltip,
    localize=True,
    sticky=False,
    labels=True,
    max_width=800,
 )
    return popup, tooltip


st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #e4efcd;
        opacity: o.5
    }
</style>
""", unsafe_allow_html=True)

Add_CityData()

with st.sidebar:
    color = st.color_picker("Pick A Color", "#00f900")
    st.write("The current color is", color)
    st.write("Explore Waterloo")
    with st.form(key= "waterlooma"):       
        parks = st.checkbox(":blue[Parks]", False)
        trails = st.checkbox(":blue[Trails]")
        sportField = st.checkbox(":blue[Sports Field]")
        schools = st.checkbox(":blue[Schools]")
        poi = st.checkbox(":blue[Points of Interest]")
        ion = st.checkbox(":blue[ION Stops]")
        parkingLots = st.checkbox(":blue[Parking Lots]")
  
        st.form_submit_button("Submit")

##ff000010;

if parks == True:
    fields = ["PARK_NAME", "ADDRESS", "PARK_TYPE", "PLAYGROUND", "TENNIS_CRT", "DIAMOND", "FIELDS", "BASKETBALL", "CRICKET", "RINKS", "TOBOGGAN", "WASHROOM"]
    tooltip = ["PARK_NAME", "ADDRESS"]
    popup, tooltip = GeneratePopup_ToolTip(fields, tooltip)
    #read_gdf(gdf_park_url)
    folium.GeoJson(read_gdf(gdf_park_url), overlay=True,popup=popup, zoom_on_click=True, tooltip=tooltip, style_function=lambda feature: {'color': 'green',
        'weight': 2, 'fillColor': 'green'}).add_to(m)
    

if sportField == True:
    fields = ["LAYER","LIGHTS","PARKING","SCH_PRK", "MAX_BASE","MAX_PITCH","DUGOUTS","WASHROOMS","PLAYGRND"]
    tooltip = ["LAYER"]
    popup, tooltip = GeneratePopup_ToolTip(fields, tooltip)
    folium.GeoJson(read_gdf(SportField_Diamond_url), overlay=True,popup=popup, zoom_on_click=True, tooltip=tooltip, style_function=lambda feature: {'color': 'green',
        'weight': 1, 'fillColor': 'brown', 'fillOpacity': 0.5}).add_to(m)
        

if trails == True:
    fields = ["TRAIL_NAME", "PATH_TYPE", "SURFACE"]
    tooltip = ["TRAIL_NAME", "PATH_TYPE", "SURFACE"]
    popup, tooltip = GeneratePopup_ToolTip(fields, tooltip)
    
    folium.GeoJson(read_gdf(gdf_trails_pathways_url), overlay=True,popup=popup, zoom_on_click=True, tooltip=tooltip,
                style_function=lambda feature: {'color': '#b10dbd',
        'weight': 3,  'dashArray': '4,4'}).add_to(m)

if schools == True:
    fields = ["NAME", "TYPE", "URL"]
    tooltip = ["NAME", "TYPE"]
    popup, tooltip = GeneratePopup_ToolTip(fields, tooltip)
    folium.GeoJson(read_gdf(Schools_url), overlay=True, marker=folium.Marker(icon=folium.Icon(icon='star',color="orange")), popup=popup, zoom_on_click=True, tooltip=tooltip).add_to(m)  

if poi == True:
    fields = ["FACILITY","OWNER", "TYPE"]
    tooltip = ["FACILITY","OWNER", "TYPE"]
    popup, tooltip = GeneratePopup_ToolTip(fields,tooltip)
    folium.GeoJson(read_gdf(Points_Interest_url),zoom_on_click=True,overlay=True, marker=folium.Marker(icon=folium.Icon(icon='star',color="purple")), popup=popup, tooltip=tooltip).add_to(m)  

if parkingLots == True:
    fields = ["NAME","ADDRESS","PERMIT_HRS","ACCESSIBLE", "MOTORCYCLE","DESCR","RESERVED","CAPACITY","TWOH_FREE","HOURLY"]
    tooltip = ["NAME","DESCR"]
    popup, tooltip = GeneratePopup_ToolTip(fields, tooltip)
    folium.GeoJson(read_gdf(Parking_Spots_url), overlay=True, popup=popup ,tooltip=tooltip,zoom_on_click=True,style_function=lambda feature: {'color': 'turquoise',
        'weight': 1, 'fillColor': 'red', 'fillOpacity': 0.5} ).add_to(m)  

if ion == True:
    fields = ["StopName","StopLocation","StopStatus","StopDirection"]
    tooltip = ["StopName"]
    popup, tooltip = GeneratePopup_ToolTip(fields,tooltip)
    folium.GeoJson(read_gdf(ION_Stops_url), overlay=True, marker=folium.Marker(icon=folium.Icon(icon='star',color="blue")), popup=popup, tooltip=tooltip).add_to(m) 

#adding final map to streamlit
#ith st.form(key="waterloomap"):

st_folium(m,width = 1000, height=725)



