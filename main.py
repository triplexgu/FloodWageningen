"""
# Geoscripting
# Exercise 10
# Flooding risk Wageningen
# Starter
# Group: able panther of judgment
# 25/10/2022
"""
# Load required packages and our functions file
import os
import functions_exc10 as funcs

# Create data and output folders
if not os.path.exists('data'):
    os.makedirs('data')
if not os.path.exists('output'):
    os.makedirs('output')

# Extract the Wageningen Municipality geometry from OSM
placeGDF = funcs.geocodePlacenameToGDF('Wageningen, Netherlands', '28992')

# Task 1
# Extract extent from the placeGDF geometry and store in variable bbox
bbox=list(placeGDF.total_bounds)

# Download AHN3 data with 5 meter resolution for the area of interest
dtm=funcs.ahn3_5m_forStudyArea(bbox,'data/AHN3_5m_DTM.tif')

# Task 2
# Create and apply function calcFloodMap(dtm, waterheight, outputfilename) that reclassifies a given DTM to flooded
# and dry areas with given waterheight of 10 meters.
flood=funcs.calcFloodMap(dtm, 10, 'data/AHN3_5m_Flood.tif')


# Task 3
# Calculate some statistics about the hypothetical flood:
#    maxWaterDepth (m) : maximum water depth occurring within study area
#    averageWaterDepth (m) : average water depth occurring
#    percWaterCoverage (%) : part of the study area that is flooded
# Note: These statistics are for the whole raster, no need to clip to the municipality boundaries first!
# Tip: see https://note.nkmk.me/en/python-numpy-count/

# Using numpy
import numpy as np

# Transfer the raster to nparray
flood_data = flood.read()

# Use numpy method to calculate the statistics
# maxDepth = (rs.zonal_stats(placeGDF, flood, stats='max'))[0]
maxWaterDepth = np.nanmax(flood_data)
averageWaterDepth = np.nanmean(flood_data)
percWaterCoverage = np.count_nonzero(flood_data>0)/flood_data.size*100

# Plot a (either static or dynamic) floodmap with the water depth in meters including the geometry outline
# of Wageningen municipality (placeGDF)

# Using Matplotlib
import matplotlib.pyplot as plt
# Create one plot with figure size 10 by 10
fig, ax = plt.subplots(figsize=(10, 10), dpi=200)

# imshow() is the main raster plotting method in Matplotlib
# Again, ensure an equal scale in the x and y direction
floodplot = ax.imshow(flood_data[0], cmap='YlGnBu', extent=bbox, aspect='equal')

# Title (do not do this for a scientific report, use a caption instead)
ax.set_title("Flood Map - Wageningen", fontsize=14)

# Add a legend (colourbar) with label
cbar = fig.colorbar(floodplot , fraction=0.035, pad=0.01)
cbar.ax.get_yaxis().labelpad = 15
cbar.ax.set_ylabel('Water depth (m)', rotation=90)

# Hide the axes
ax.set_axis_off()
plt.show()

# Bonus: Calculate how much of the roads is within the flooded zone
# Tips:
#    https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.geometries.geometries_from_place
#    https://pythonhosted.org/rasterstats/

