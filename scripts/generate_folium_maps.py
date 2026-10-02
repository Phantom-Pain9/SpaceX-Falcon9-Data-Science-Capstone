import folium
from folium.plugins import MarkerCluster
import pandas as pd
import subprocess
import os
import math
import time

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_dir, 'data', 'spacex_launch_geo.csv')
fig_dir = os.path.join(base_dir, 'figures')
html_dir = os.path.join(base_dir, 'scripts')

df = pd.read_csv(data_path)

# ==========================================
# MAP 1: Launch Site Markers
# ==========================================
site_map = folium.Map(location=[28.562302, -80.577356], zoom_start=5)

for _, row in df[['Launch Site', 'Lat', 'Long']].drop_duplicates().iterrows():
    circle = folium.Circle(
        [row['Lat'], row['Long']],
        radius=1000,
        color='#d35400',
        fill=True
    ).add_child(folium.Popup(row['Launch Site']))
    
    marker = folium.map.Marker(
        [row['Lat'], row['Long']],
        icon=folium.DivIcon(
            icon_size=(20, 20),
            icon_anchor=(0, 0),
            html=f'<div style="font-size: 13; font-weight: bold; color:#d35400;">{row["Launch Site"]}</div>'
        )
    )
    site_map.add_child(circle)
    site_map.add_child(marker)

map1_path = os.path.join(html_dir, 'folium_map1.html')
site_map.save(map1_path)

# ==========================================
# MAP 2: MarkerCluster with Success / Failure
# ==========================================
cluster_map = folium.Map(location=[28.562302, -80.577356], zoom_start=5)
marker_cluster = MarkerCluster().add_to(cluster_map)

for _, row in df.iterrows():
    color = 'green' if row['class'] == 1 else 'red'
    marker = folium.Marker(
        location=[row['Lat'], row['Long']],
        icon=folium.Icon(color='white', icon_color=color),
        popup=f"Site: {row['Launch Site']}<br>Outcome: {'Success' if row['class']==1 else 'Failure'}"
    )
    marker_cluster.add_child(marker)

map2_path = os.path.join(html_dir, 'folium_map2.html')
cluster_map.save(map2_path)

# ==========================================
# MAP 3: Distance & Proximity Analysis (KSC LC-39A / CCAFS SLC-40)
# ==========================================
# Cape Canaveral coordinates
prox_map = folium.Map(location=[28.563197, -80.576820], zoom_start=14)

launch_coord = [28.563197, -80.576820]
coastline_coord = [28.56367, -80.568]
highway_coord = [28.56372, -80.57085]
railway_coord = [28.57205, -80.58525]
city_coord = [28.612219, -80.807556] # Titusville

def haversine(c1, c2):
    lat1, lon1 = c1
    lat2, lon2 = c2
    R = 6371.0 # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

proximities = [
    ("Coastline", coastline_coord, "#3498db"),
    ("Highway", highway_coord, "#e67e22"),
    ("Railway", railway_coord, "#9b59b6"),
    ("City (Titusville)", city_coord, "#e74c3c")
]

# Launch site marker
folium.Marker(
    launch_coord,
    icon=folium.Icon(color='blue', icon='rocket', prefix='fa'),
    popup="CCAFS SLC-40"
).add_to(prox_map)

for name, coord, color in proximities:
    dist = haversine(launch_coord, coord)
    folium.Marker(
        coord,
        icon=folium.DivIcon(
            icon_size=(20, 20),
            icon_anchor=(0, 0),
            html=f'<div style="font-size: 12pt; font-weight: bold; color: {color}; background-color: white; border: 1px solid black; padding: 2px 4px; border-radius: 4px;">{name}: {dist:.2f} KM</div>'
        )
    ).add_to(prox_map)
    
    folium.PolyLine(
        [launch_coord, coord],
        color=color,
        weight=2.5,
        opacity=0.8
    ).add_to(prox_map)

map3_path = os.path.join(html_dir, 'folium_map3.html')
prox_map.save(map3_path)
print("Folium HTML maps saved.")

# Screenshot using Google Chrome
chrome_bin = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
for idx, (mpath, img_name) in enumerate([
    (map1_path, '12_folium_launch_sites.png'),
    (map2_path, '13_folium_marker_clusters.png'),
    (map3_path, '14_folium_distance_analysis.png')
]):
    out_img = os.path.join(fig_dir, img_name)
    cmd = [
        chrome_bin,
        '--headless',
        '--disable-gpu',
        '--hide-scrollbars',
        '--window-size=1200,750',
        f'--screenshot={out_img}',
        f'file://{mpath}'
    ]
    print(f"Capturing screenshot for {img_name}...")
    subprocess.run(cmd, check=True)
    print(f"Captured {img_name}")

print("Folium map capture complete!")
