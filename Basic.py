import folium.map
import streamlit as st
import pandas as pd
import folium 
from streamlit_folium import st_folium
from streamlit_folium import folium_static
from folium import plugins
import geopandas
import osmnx as ox
import pydeck as pdk

city = "Waterloo"
place_name = ""

st.set_page_config( page_title=None,
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None,)


# color = st.color_picker("Pick A Color", "#00f900")
# st.write("The current color is", color)
st.title("🚗🚲 :blue[Waterloo Parking Finder]")

# Banner using Markdown
# st.markdown("""
#      <meta name="viewport" content="width=device-width, initial-scale=1.0">
#      <span style=“background-color: #daf2f7">
#             <style>
           
#               .banner {
#             background-color:  #daf2f7;
#             text-align: center;
#             font-size: 30px;
#             padding: 20px;
#             color: #6a4687;}        
#     </style>   
#     <div class="banner">
#         🚗🚲 Waterloo Parking Finder
#     </div>
#             <hr style='border: 1px solid black;'>
# """, unsafe_allow_html=True)


st.markdown("""
:blue[Welcome! This app helps you find **car and bicycle parking** spots in the City of Waterloo using open data.
Use the filters on the sidebar and explore the interactive map below. Easily locate car and bicycle parking spots across the City of Waterloo. Find your current location, use measurement
            tool to measure your distance from the parking space]
""")

st.info("🧭 Tip: Click on any map marker to view parking details.")


view = st.radio(" :blue[Set Map View 📍] ",
        ["Light Mode", "Satellite View","Dark Mode"],horizontal=True)

#Roads_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/Roads/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

waterloo_boundary_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/CityBoundary/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

RegionOfWaterloo_url = "https://services1.arcgis.com/qAo1OsXi67t7XgmS/arcgis/rest/services/Municipal_Boundary/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

gdf_park_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/Parks/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

gdf_trails_pathways_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/Trails_and_Pathways/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

SportField_Diamond_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/SportsFieldsDiamonds/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

Schools_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/Schools/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

Points_Interest_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/PointsOfInterest/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

City_Operated_Parking_url = "https://services.arcgis.com/ZpeBVw5o1kjit7LT/arcgis/rest/services/ParkingLots/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

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
                zoom_control=True, control_scale=True, key="waterloomap")#, disable_3d = True, min_zoom=0, max_zoom=30)
 
if view == "Light Mode":
    m = folium.Map(location=[43.462400, -80.520811], tiles="CartoDB Positron", zoom_start=13,
                zoom_control=True, control_scale=True, key="waterloomap")#, disable_3d = True, min_zoom=0, max_zoom=30)

if view == "Dark Mode":
    m = folium.Map(location=[43.462400, -80.520811], tiles="CartoDB Dark_Matter", zoom_start=13,
                zoom_control=True, control_scale=True, key="waterloomap")#, disable_3d = True, min_zoom=0, max_zoom=30)
#adding location control

    
 #Adding waterloo square location marker

def Add_CityData():
    
    folium.GeoJson(read_gdf(RegionOfWaterloo_url), overlay=True,
                style_function=lambda feature: {'color': "#b9ea09",
        'weight': 1.5,'fillOpacity': 0.0}).add_to(m)
    
m.add_child(folium.plugins.LocateControl())
m.add_child(folium.plugins.Fullscreen())
m.add_child(folium.plugins.MeasureControl())



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


def Clearall_Checkbx():
    
        # if st.session_state["prk"] == True:
        #     st.session_state["prk"] = False
        #     parks = False
       # if st.session_state["trl"] == True:
       #      st.session_state["trl"] = False

        # if st.session_state["sptsfld"] == True:
        #     st.session_state["sptsfld"] = False

        # if st.session_state["schl"] == True:
        #     st.session_state["schl"] = False

        # if st.session_state["poi"] == True:
        #     st.session_state["poi"] = False
        
        # if st.session_state["ionstp"] == True:
        #     st.session_state["ionstp"] = False
        #     parks = False
        if st.session_state["prklots"] == True:
            st.session_state["prklots"] = False

        if st.session_state["bicprk"] == True:
            st.session_state["bicprk"] = False

        # if st.session_state["libry"] == True:
        #     st.session_state["libry"] = False

        #if st.session_state["hsptl"] == True:
        #    st.session_state["hsptl"] = False
        
       # if st.session_state["busstp"] == True:
       #     st.session_state["busstp"] = False

        # if st.session_state["spmkt"] == True:
        #     st.session_state["spmkt"] = False

        #if st.session_state["evchstns"] == True:
        #    st.session_state["evchstns"] = False

        
        #if st.session_state["otherplcs"] == True:
        #    st.session_state["otherplcs"] = False
        

def ClearAll_buttonClick():
    if st.session_state["clrall"]:
        Clearall_Checkbx()


with st.sidebar:
    
    st.markdown("###  :blue[Select to Search]")
    with st.form(key= "waterlooma", enter_to_submit=True):                    
        
        parks = False#st.checkbox(":blue[Parks]", key="prk", disabled=True)
        trails = False #st.checkbox(":blue[Trails]", key="trl")
        sportField = False#st.checkbox(":blue[Sports Field]",  key="sptsfld")
        schools = False#st.checkbox(":blue[Schools]",  key="schl")
        poi = False#st.checkbox(":blue[Points of Interest]",  key="poi")
        ion = False#st.checkbox(":blue[ION Stops]",  key="ionstp")
        parkingLots = st.checkbox(":blue[Parking Lots]",  key="prklots")
        
        bicycleParking = st.checkbox(":blue[Bicycle Parking]",  key="bicprk")

        library = False#st.checkbox(":blue[Library]",  key="libry")
        hospitals = False#st.checkbox(":blue[Health Care & Pharmacy]",  key="hsptl")
        bus_Stop = False #st.checkbox(":blue[Bus Stops]",  key="busstp")        
        supermarkets_malls = False#st.checkbox(":blue[Supermarkets & Malls]",  key="spmkt")       
        evCharging = False #st.checkbox(":blue[EV Charging stations]",  key="evchstns")
        st.form_submit_button(":red[Search 🔎]", use_container_width=True)#Submit buton for the form

    st.button(":blue[Clear All Selection 🧹]", key="clrall", on_click=ClearAll_buttonClick, use_container_width=True)

   

    st.write("🗺️ :blue[How to Use the Map]")
    st.write(" :blue[Zoom & Pan: Navigate around Waterloo, Ontario, Canada using your mouse or trackpad — zoom in/out and drag the map to explore different areas.]")
    st.write(" :blue[Parking Icons: Car parking spots are marked in pink rectangular space bordered with purple color.]")
    st.write(" :blue[Bicycle Parking Icons: Bicycle parking spots are marked in green icon.]")
    st.write(" :blue[Click on Markers: Select a marker to view details like parking type, address, or capacity (if available)]")

    st.write(" :blue[Filter Options: Use the sidebar to toggle between car and bicycle parking. You can find out the distance to any parking lot from your " \
    "current location.]")
    st.write(" :blue[Clear All Selection: Smash this button to clear the map off all the previous selections]")
    st.write(" :blue[Mobile Friendly: The app is responsive — use it on the go to find nearby parking!]")
   

           
if view == "Satellite View":
    tile = folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        #tiles = '<iframe src="https://www.google.com/maps/d/embed?mid=1-BmsGpk0VJqNE7xMBnQUa7QU_SYwokc&ehbc=2E312F" width="640" height="480"></iframe>',
        attr = 'Esri',
        name = 'Esri Satellite',
        overlay = False,
        control = True
       ).add_to(m)          


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
                style_function=lambda feature: {'color': 'green',
        'weight': 2,  'dashArray': '3,3'}).add_to(m)

if schools == True:
    fields = ["NAME", "TYPE", "URL"]
    tooltip = ["NAME", "TYPE"]
    text = "hi"
    popup, tooltip = GeneratePopup_ToolTip(fields, tooltip)
    folium.GeoJson(read_gdf(Schools_url), overlay=True, 
                   marker=folium.Marker(icon=folium.Icon(icon='flag',color= 'orange', prefix = "glyphicon")), popup=popup, 
                   zoom_on_click=True, tooltip=tooltip).add_to(m)  

if poi == True:#Place of Interest (poi)
    fields = ["FACILITY","OWNER", "TYPE"]
    tooltip = ["FACILITY","OWNER", "TYPE"]
    popup, tooltip = GeneratePopup_ToolTip(fields,tooltip)

    gdf_poi = read_gdf(Points_Interest_url)

    for row in gdf_poi.itertuples():
        gdf_poi = gdf_poi.drop(gdf_poi[(gdf_poi['TYPE'] == 'Library') | (gdf_poi['TYPE'] == 'Fire Hall') | 
                                       (gdf_poi['TYPE'] == 'Ambulance Station') |  (gdf_poi['TYPE'] == 'Police Station')].index)
        

    folium.GeoJson(gdf_poi,zoom_on_click=True,overlay=True, 
                   marker=folium.Marker(icon=folium.Icon(icon='asterisk',color="darkblue", prefix = "glyphicon")), popup=popup, tooltip=tooltip).add_to(m)  

if parkingLots == True:

    fields = ["access"]
    tooltip = ["access"]

    
    popup, tooltip = GeneratePopup_ToolTip(fields, tooltip)

    # List key-value pairs for tags
    tags = {'amenity': True, 'amenity': ['parking']}   

    #access and capacity colum
    
    parking = ox.features_from_place("Waterloo, Ontario", tags)
    parking = parking.fillna('Data not available')
    #parking = read_gdf(City_Operated_Parking_url)

    
    folium.GeoJson(parking, overlay=True, popup=popup, tooltip=tooltip,zoom_on_click=True,style_function=lambda feature: {'color': 'purple',
        'weight': 1, 'fillColor': 'pink', 'fillOpacity': 0.8}, ).add_to(m)  
    
    
if ion == True:
    fields = ["StopName","StopLocation","StopStatus","StopDirection"]
    tooltip = ["StopName"]
    popup, tooltip = GeneratePopup_ToolTip(fields,tooltip)
    folium.GeoJson(read_gdf(ION_Stops_url), overlay=True, 
                   marker=folium.Marker(icon=folium.Icon(icon='circle',prefix='fa fa-train',color="lightgreen")), 
                   popup=popup, tooltip=tooltip).add_to(m) 


if bicycleParking == True:
    fields = [ "TYPE", "OWNED_BY", "DESCR", "ADDRESS", "CAPACITY",]
    tooltip = ["DESCR", "ADDRESS", "CAPACITY"]
    popup, tooltip = GeneratePopup_ToolTip(fields,tooltip)
    
   
    marker_cluster = folium.plugins.MarkerCluster().add_to(m)

    folium.GeoJson(read_gdf(bicycleParking_url), overlay=True,popup=popup, 
                   tooltip=tooltip, marker=folium.Marker(icon=folium.Icon(color="green", prefix="fa", icon="bicycle"))).add_to(marker_cluster)
    
    # folium.GeoJson(read_gdf(bicycleParking_url), overlay=True, control=True, 
    #                marker=folium.Marker(icon=folium.Icon(icon='bicycle',prefix='fa', 
    #                                                      color="green")), popup=popup, tooltip=tooltip).add_to(m) 
    

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
                                                         color="beige"))).add_to(m)

if bus_Stop == True:

    tooltip = ["Street","CrossStreet", "Municipality"]
    fields = ["Street","CrossStreet", "Municipality", "EasyGo"]

    popup, tooltip = GeneratePopup_ToolTip(fields, tooltip)

       
    ########Creating Marker Cluster for GRT Bus stop for Region Of Waterloo####################

    # Create a MarkerCluster object
    marker_cluster = folium.plugins.MarkerCluster().add_to(m)

    # Example of custom icons    
    
    folium.GeoJson(read_gdf(GRT_Bus_Stop_url), overlay=True,popup=popup, 
                   tooltip=tooltip, marker=folium.Marker(icon=folium.Icon(prefix="fa fa-bus", icon="bus", color="darkpurple"))).add_to(marker_cluster)
    
    ########Creating Marker Cluster for GRT Bus Routes for Region Of Waterloo####################
                   
    folium.GeoJson(read_gdf(GRT_Bus_Route_url), overlay=True, zoom_on_click=True,
                style_function=lambda feature: {'color': ' #f7b10b',
        'weight': 1.5}).add_to(m)

    
if hospitals == True:
    fields = ["LANDMARK", "CIVIC_NO", "STREET"]
    tooltip = ["LANDMARK", "CIVIC_NO", "STREET"]
    popup, tooltip = GeneratePopup_ToolTip(fields,tooltip)

    # List key-value pairs for tags
    tags = {'amenity': True, 'amenity': ['pharmacy','drugstore', 'chemist','clinic']}   

    pharmacy = ox.features_from_place(place_name, tags)
    pharmacy = pharmacy.fillna('Data not available') #filling null values in the data frame with the specfied value

    folium.GeoJson(read_gdf(Hospitals_url), overlay=True, 
                   marker=folium.Marker(icon=folium.Icon(icon='plus',color="darkred", prefix = "glyphicon")), 
                   popup=popup, tooltip=tooltip).add_to(m)
    
    fields = ["name", "opening_hours", "website"]
    tooltip = ["name", "opening_hours"]
    popup, tooltip = GeneratePopup_ToolTip(fields,tooltip)
    
    folium.GeoJson(pharmacy, popup=popup, tooltip=tooltip,marker=folium.Marker(icon=folium.Icon(icon='plus',color="orange", prefix = "glyphicon"))).add_to(m)   

if supermarkets_malls == True:    

    # List key-value pairs for tags
    tags = {'shop': True, 'shop': ['supermarket', 'malls']}   

    buildings = ox.features_from_place(place_name, tags)
    buildings = buildings.fillna('Data not available')
    #buildings.head()
    #st.write(buildings)
    folium.GeoJson(buildings, marker=folium.Marker(icon=folium.Icon(icon='info-sign',
                                                         color="pink"))).add_to(m)

if evCharging == True:    
    fields = ["brand", "access", "opening_hours"]
    tooltip = ["opening_hours"]
    popup, tooltip = GeneratePopup_ToolTip(fields,tooltip)

    # List key-value pairs for tags
    #amenity=cinema
    tags = {'amenity': True, 'amenity': ['charging_station']}   

    evstations = ox.features_from_place(place_name, tags)
    evstations = evstations.fillna('Data not available') #filling null values in the data frame with the specfied value
    folium.GeoJson(evstations, tooltip=tooltip,popup= popup, marker=folium.CircleMarker(radius=10, stroke=True, color='blue',fillOpacity=2.0, fillColor='green')).add_to(m)



view_state = pdk.ViewState(
    latitude=40, longitude=-117, controller=True, zoom=2.4, pitch=30
)



#Adding textbox for user to enter the name of place

#st.text_input("Enter the name of a place", place_name)

def Display_Place_Parking():
    
    if(place_name) :
        st.write(place_name)
        fields = ["access"]
        tooltip = ["access"]
        st.write(place_name)
        popup, tooltip = GeneratePopup_ToolTip(fields, tooltip)

        # List key-value pairs for tags
        tags = {'amenity': True, 'amenity': ['parking']}   

        #access and capacity colum        
        parking = ox.features_from_place(place_name, tags)
        parking = parking.fillna('Data not available')
        #parking = read_gdf(City_Operated_Parking_url)

        
        folium.GeoJson(parking, overlay=True, popup=popup, tooltip=tooltip,zoom_on_click=True,style_function=lambda feature: {'color': 'purple',
            'weight': 1, 'fillColor': 'pink', 'fillOpacity': 0.8}, ).add_to(m)  
    
#st.button("Go", on_click=Display_Place_Parking(), key="Gosearch")


#Adding to the main map

folium_static(m,width = 1000, height=500)

st.markdown("#### ℹ️ :blue[About This App]")
st.markdown(""" :blue[
This app helps users find car and bicycle parking in the City of Waterloo using open data sources.
Built with ❤️ using Python, Streamlit, OpenStreetMap, and Waterloo Region Open Data.
]""")
st.markdown("#### 📬 :blue[Feedback or Suggestions?]")
st.markdown(" :blue[Feel free to reach out on [LinkedIn](https://www.linkedin.com/in/alefiya-sj-a553a1220/) or contribute on [GitHub](https://github.com/adungrawala/WebApp).]")

st.markdown(" :blue[© 2025 Alefiya SJ. This is a community tool and not affiliated with the City of Waterloo, Ontario, Canada.]")