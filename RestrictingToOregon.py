import pandas as pd
import os
import matplotlib.pyplot as plt
import geopandas as gpd
import urllib.request
import shutil

# Define paths
download_folder = 'data_external/map of oregon'
covid_file = r'D:\PYTHON-PROJECTS\MathComputingWithPython\data_external\covid19\03-27-2020.csv'

# Load COVID-19 data
try:
    co = pd.read_csv(covid_file)
    print("COVID-19 data loaded successfully. First 5 rows:")
    print(co.head())
    print("\nColumns in COVID-19 data:", co.columns.tolist())
except Exception as e:
    print(f"Error loading COVID-19 file: {e}")
    exit()

# Download and process US counties shapefile
try:
    # URL of the US counties map data
    census_url = 'https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_county_500k.zip'

    # Create download folder if it doesn’t exist
    if not os.path.isdir(download_folder):
        os.makedirs(download_folder)
    us_county_file = os.path.join(download_folder, 'cb_2018_us_county_500k.zip')

    # Download if the file doesn’t already exist
    if not os.path.isfile(us_county_file):
        print(f"Downloading US counties shapefile from {census_url}...")
        with urllib.request.urlopen(census_url) as response, open(us_county_file, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        print("Download complete.")

    # Read the shapefile
    us_counties = gpd.read_file(f"zip://{us_county_file}")
    print("US counties data loaded. First 5 rows:")
    print(us_counties.head())

    # Filter for Oregon (STATEFP = '41')
    ore = us_counties[us_counties['STATEFP'] == '41']

    # Convert GEOID to int64 and rename to FIPS
    ore = ore.astype({'GEOID': 'int64'}).rename(columns={'GEOID': 'FIPS'})

    # Handle non-finite values in FIPS column of COVID data
    print("\nChecking for non-finite values in 'FIPS' column...")
    print(co['FIPS'].isna().sum(), "missing values in 'FIPS'")

    # Filter out rows with NaN in FIPS and convert to int64
    co = co.dropna(subset=['FIPS'])  # Drop rows where FIPS is NaN
    co = co.astype({'FIPS': 'int64'})  # Now safe to convert

    # Merge Oregon counties with COVID data
    orco = pd.merge(ore, co.iloc[:, :-1], on='FIPS')
    print("\nMerged Oregon data. First 5 rows:")
    print(orco.head())

    # Plot coloring counties by number of confirmed cases
    fig, ax = plt.subplots(figsize=(12, 8))
    orco.plot(ax=ax, column='Confirmed', legend=True,
              legend_kwds={'label': '# confirmed cases', 'orientation': 'horizontal'})

    # Label the counties
    for x, y, county in zip(orco['Long_'], orco['Lat'], orco['NAME']):
        ax.text(x, y, county, color='grey')

    ax.set_title('Confirmed COVID-19 cases in Oregon as of 03-27-2020')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    plt.show()

except pd.errors.EmptyDataError:
    print(f"Error: File {us_county_file} or {covid_file} is empty")
except Exception as e:
    print(f"An unexpected error occurred: {e}")