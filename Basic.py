import folium.plugins
import streamlit as st
import pandas as pd
import folium 
from streamlit_folium import st_folium
from folium import plugins
import geopandas


city = "Waterloo"

st.set_page_config( page_title=None,
    page_icon=None,
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None,)


# color = st.color_picker("Pick A Color", "#00f900")
# st.write("The current color is", color)

# Banner using Markdown
st.markdown("""
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <span style=“background-color: #daf2f7">
            <style>
           
              .banner {
            background-color:  #daf2f7;
            text-align: center;
            font-size: 30px;
            padding: 20px;
            color: #6a4687;}        
    </style>   
    <div class="banner">
        Welcome to Waterloo!
    </div>
            <hr style='border: 1px solid black;'>
""", unsafe_allow_html=True)



#Roads_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/Roads/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

waterloo_boundary_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/CityBoundary/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

RegionOfWaterloo_url = "https://services1.arcgis.com/qAo1OsXi67t7XgmS/arcgis/rest/services/Municipal_Boundary/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

gdf_park_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/Parks/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

gdf_trails_pathways_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/Trails_and_Pathways/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

SportField_Diamond_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/SportsFieldsDiamonds/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

Schools_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/Schools/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

Points_Interest_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/PointsOfInterest/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

Parking_Spots_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/ParkingLots/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

ION_Stops_url = "https://utility.arcgis.com/usrsvcs/servers/f063d1fb147847f796ce8c024e117419/rest/services/OpenData/OpenData/MapServer/5/query?outFields=*&where=1%3D1&f=geojson"

Hospitals_url = "https://services1.arcgis.com/qAo1OsXi67t7XgmS/arcgis/rest/services/Hospitals/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

bicycleParking_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/BicycleParking/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

libraries_url = "https://utility.arcgis.com/usrsvcs/servers/e20e47591d41407e95f85d73e9b90322/rest/services/OpenData/OpenData/MapServer/0/query?outFields=*&where=1%3D1&f=geojson"

GRT_Bus_Stop_url = "https://utility.arcgis.com/usrsvcs/servers/52c4134809a94f85b31a2e9553de1358/rest/services/OpenData/OpenData/MapServer/3/query?outFields=*&where=1%3D1&f=geojson"

GRT_Bus_Route_url = "https://utility.arcgis.com/usrsvcs/servers/16e0ab66dadf4044a5be144e9d88effb/rest/services/OpenData/OpenData/MapServer/4/query?outFields=*&where=1%3D1&f=geojson" 

@st.cache_data
def read_gdf(gdf_url):
    gdf = geopandas.read_file(gdf_url)
    return gdf


m = folium.Map(location=[43.462400, -80.520811], tiles="CartoDB Positron", zoom_start=13,
                zoom_control=True, control_scale=True, key="waterloomap", disable_3d = True, min_zoom=0, max_zoom=30)
 

 #Adding waterloo square location marker
def Add_CityData():
    
    # folium.GeoJson(read_gdf(waterloo_boundary_url), overlay=True, zoom_on_click=True,
    #             style_function=lambda feature: {'color': '#b91563',
    #     'weight': 1.5,'fillOpacity': 0.0}).add_to(m)
    
    
    folium.GeoJson(read_gdf(RegionOfWaterloo_url), overlay=True, zoom_on_click=True,
                style_function=lambda feature: {'color': '#4f096d',
        'weight': 1.5,'fillOpacity': 0.0}).add_to(m)
    
#adding location control
folium.plugins.LocateControl().add_to(m)
folium.plugins.Fullscreen().add_to(m)

# adding park data to popup#
def GeneratePopup_ToolTip(fields, tooltip):
     
    #adding popup values
    popup = folium.GeoJsonPopup(
    fields= fields,
    localize=True,
    labels=True,
    max_width= 900,
    style="background-color: violet;",
    )
    
    #adding tooltip
    tooltip = folium.GeoJsonTooltip(
    fields=tooltip,
    localize=True,
    sticky=False,
    labels=True,
    max_width=900,
 )
    return popup, tooltip

Add_CityData() #Calling the function to add roads and city boundary

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #daf2f7;
        opacity: 1.0,
        contrast: 1.2
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header(":violet[Explore Waterloo]")
   
       
    with st.form(key= "waterlooma", enter_to_submit=True):     
               
        
        parks = st.checkbox(":violet[Parks]", key="prk")
        trails = st.checkbox(":violet[Trails]")
        sportField = st.checkbox(":violet[Sports Field]")
        schools = st.checkbox(":violet[Schools]")
        poi = st.checkbox(":violet[Points of Interest]")
        ion = st.checkbox(":violet[ION Stops]")
        parkingLots = st.checkbox(":violet[Parking Lots]")
        
        bicycleParking = st.checkbox(":violet[Bicycle Parking]")
        library = st.checkbox(":violet[Library]")
        hospitals = st.checkbox(":violet[Hospitals]")
        bus_Stop = st.checkbox(":violet[Bus Stops - Region of Waterloo]")
        st.form_submit_button(":violet[Submit]", use_container_width=False)#Submit buton for the form
        
           
           


if parks == True:
    fields = ["PARK_NAME", "ADDRESS", "PARK_TYPE", "PLAYGROUND", "TENNIS_CRT", "DIAMOND", "FIELDS", "BASKETBALL", "CRICKET", "RINKS", "TOBOGGAN", "WASHROOM"]
    tooltip = ["PARK_NAME", "ADDRESS"]
    popup, tooltip = GeneratePopup_ToolTip(fields, tooltip)
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
                style_function=lambda feature: {'color': 'red',
        'weight': 2,  'dashArray': '3,3'}).add_to(m)

if schools == True:
    fields = ["NAME", "TYPE", "URL"]
    tooltip = ["NAME", "TYPE"]
    popup, tooltip = GeneratePopup_ToolTip(fields, tooltip)
    folium.GeoJson(read_gdf(Schools_url), overlay=True, 
                   marker=folium.Marker(icon=folium.Icon(icon='home',color="orange", prefix = "glyphicon",)), popup=popup, zoom_on_click=True, tooltip=tooltip).add_to(m)  

if poi == True:#Place of Interest (poi)
    fields = ["FACILITY","OWNER", "TYPE"]
    tooltip = ["FACILITY","OWNER", "TYPE"]
    popup, tooltip = GeneratePopup_ToolTip(fields,tooltip)

    gdf_poi = read_gdf(Points_Interest_url)

    for row in gdf_poi.itertuples():
        gdf_poi = gdf_poi.drop(gdf_poi[(gdf_poi['TYPE'] == 'Library') | (gdf_poi['TYPE'] == 'Fire Hall') | 
                                       (gdf_poi['TYPE'] == 'Ambulance Station') |  (gdf_poi['TYPE'] == 'Police Station')].index)
        

    folium.GeoJson(gdf_poi,zoom_on_click=True,overlay=True, 
                   marker=folium.Marker(icon=folium.Icon(icon='asterisk',color="darkblue")), popup=popup, tooltip=tooltip).add_to(m)  

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
    folium.GeoJson(read_gdf(ION_Stops_url), overlay=True, 
                   marker=folium.Marker(icon=folium.Icon(icon='train',prefix='fa fa-train',color="lightgreen")), 
                   popup=popup, tooltip=tooltip).add_to(m) 



#adding final map to streamlit
if bicycleParking == True:
    fields = [ "TYPE", "OWNED_BY", "DESCR", "ADDRESS", "CAPACITY",]
    tooltip = ["DESCR", "ADDRESS", "CAPACITY"]
    popup, tooltip = GeneratePopup_ToolTip(fields,tooltip)
    
    folium.GeoJson(read_gdf(bicycleParking_url), overlay=True, control=True, 
                   marker=folium.Marker(icon=folium.Icon(icon='bicycle',prefix='fa', 
                                                         color="green")), popup=popup, tooltip=tooltip).add_to(m) 
    

if library == True:
    fields = ["Name","Address","Phone", "Website"]
    tooltip = ["Name","Address"]
    popup, tooltip = GeneratePopup_ToolTip(fields,tooltip)

    lib_gdf = read_gdf(libraries_url)
    #going through each row and dropping the frame with library other than 'Waterloo'
    for index,row in lib_gdf.iterrows(): # Looping over all points
       i = lib_gdf[(lib_gdf.Municipality != city)].index 
       lib_gdf = geopandas.GeoDataFrame.drop(lib_gdf,index=i)

    folium.GeoJson(lib_gdf, overlay=True,popup=popup, tooltip=tooltip, 
                   marker=folium.Marker(icon=folium.Icon(icon='book',prefix='fa fa-book',
                                                         color="black"))).add_to(m)

if bus_Stop == True:

    tooltip = ["Street","CrossStreet", "Municipality"]
    fields = ["Street","CrossStreet", "Municipality", "EasyGo"]

    popup, tooltip = GeneratePopup_ToolTip(fields, tooltip)

       
    ########Creating Marker Cluster for GRT Bus stop for Region Of Waterloo####################

    # Create a MarkerCluster object
    marker_cluster = folium.plugins.MarkerCluster().add_to(m)

    # Example of custom icons
    custom_icon = folium.Icon(prefix='fa fa-bus', icon='bus', color='darkpurple')
    
    folium.GeoJson(read_gdf(GRT_Bus_Stop_url), overlay=True,popup=popup, 
                   tooltip=tooltip, marker=folium.Marker(icon=custom_icon)).add_to(marker_cluster)
    
    ########Creating Marker Cluster for GRT Bus Routes for Region Of Waterloo####################
                   
    folium.GeoJson(read_gdf(GRT_Bus_Route_url), overlay=True, zoom_on_click=True,
                style_function=lambda feature: {'color': ' #f7b10b',
        'weight': 1.5}).add_to(m)

    
   
if hospitals == True:
    fields = ["LANDMARK", "CIVIC_NO", "STREET"]
    tooltip = ["LANDMARK", "CIVIC_NO", "STREET"]
    popup, tooltip = GeneratePopup_ToolTip(fields,tooltip)
    folium.GeoJson(read_gdf(Hospitals_url), overlay=True, 
                   marker=folium.Marker(icon=folium.Icon(icon='home',color="darkred")), 
                   popup=popup, tooltip=tooltip).add_to(m) 
   
#Adding to the main map
st_folium(m,width = 1000, height=500)




