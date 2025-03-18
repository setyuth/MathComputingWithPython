import pandas as pd
import os
import matplotlib.pyplot as plt
import geopandas as gpd

# Define the folder and file path
covidfolder = 'data_external/covid19'
csv_file = '03-27-2020.csv'
file_path = os.path.join(covidfolder, csv_file)

# Print for debugging
print(f"Looking for file at: {file_path}")

# Verify the file exists
if not os.path.isfile(file_path):
    print(f"Error: File {file_path} not found")
    exit()

# Try to read the CSV file
print(f"Attempting to read file: {file_path}")
try:
    c = pd.read_csv(file_path)
    print("File loaded successfully. First 5 rows:")
    # print(c.head())

    # make a geometry object from Lat, Long
    geo = gpd.points_from_xy(c['Long_'], c['Lat'])
    # give the geometry to geopandas together with c
    gc = gpd.GeoDataFrame(c, geometry=geo)
    print(gc.head())

    # Load the world map from a local shapefile
    world_shapefile = r'D:\PYTHON-PROJECTS\MathComputingWithPython\data_external\naturalearth\ne_110m_admin_0_countries.shp'
    if not os.path.isfile(world_shapefile):
        print(f"Error: Shapefile {world_shapefile} not found. Please download it from Natural Earth.")
        exit()

    world = gpd.read_file(world_shapefile)
    print("\nWorld map loaded. Plotting...")
    # world.plot()
    base = world.plot(alpha=0.3)
    msz = 500 * gc['Confirmed'] / gc['Confirmed'].max()
    gc.plot(ax=base, column='Confirmed', markersize=msz, alpha=0.7)
    plt.show()  # Display the plot
except pd.errors.EmptyDataError:
    print(f"Error: File {file_path} is empty")
except Exception as e:
    print(f"An unexpected error occurred: {e}")