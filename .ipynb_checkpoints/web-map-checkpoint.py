import folium
import pandas

# we use Pandas to import data from CSV and set variables for coordinates and elevation of each volcano
data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

# this function simply assigns a colour keyword based on elevation
def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

# this sets the default centre and zoom of the map
map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles="Mapbox Bright")

# this tells the folium module what it is looking for
fgv = folium.FeatureGroup(name="Volcanoes")

# we can go through each volcano and assign a circle marker, coloured based on the elevation
for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius = 6, popup=str(el)+" m",
    fill_color=color_producer(el), fill=True,  color = 'grey', fill_opacity=0.7))

# in this case we creating a new feature group for the population of each country
fgp = folium.FeatureGroup(name="Population")

# the json file that we have includes both polygons for each country, as well as population data
# we can then assign each country's polygon a colour based on it's population
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

# finally, we simply add the feature groups as layers to the map
map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("Map1.html")
