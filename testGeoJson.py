# %%
import geopandas as gpd
import pandas as pd

geo_file = gpd.read_file("/Users/gustavnystedt/Downloads/CTYUA_Dec_2015_FCB_in_England_and_Wales_2022_-2260055219064148630.geojson")
# %%
mapping_csv = pd.read_csv("/Users/gustavnystedt/Downloads/Local_Authority_District_to_Region_(December_2022)_Lookup_in_England.csv")

# %%
mapped_yeye = pd.merge(geo_file, mapping_csv, how="inner", left_on='ctyua15cd', right_on='LAD22CD')
# %%
import geoplot
import geoplot.crs as gcrs
# %%
geoplot.polyplot(geo_file, projection=gcrs.AlbersEqualArea(), edgecolor='darkgrey', facecolor='lightgrey', linewidth=.3,
    figsize=(12, 8))
# %%
test = geo_file.to_crs(epsg=4326)
# %%
geoplot.polyplot(test, projection=gcrs.AlbersEqualArea(), edgecolor='darkgrey', facecolor='lightgrey', linewidth=.3,
    figsize=(12, 8))
# %%
test.to_csv('test_geofile.csv')
# %%
