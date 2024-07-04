"""
# Geoscripting
# Exercise 10
# Flooding risk Wageningen
# Starter
# Group: able panther of judgment
# 25/10/2022
"""


def calcFloodMap(dtm, waterheight, outputfilename):
    """Function that takes a DEM and water height as input, both with same height
    reference. Output is a raster specifying whether a cell is flooded, and if so the water depth."""
    # Load necessary package
    import rasterio
    import numpy as np
    # Read the input raster (dem)
    dtm_data = dtm.read()

    # Filter out buildings and water bodies
    dtm_data[dtm_data == dtm.nodata] = waterheight

    # Compute surface level relative to water level
    Surface_level=dtm_data-waterheight

    # Set all cells where the value is higher than zero to None (these are not flooded)
    Surface_level[Surface_level>0]=np.nan

    # Invert values in all flooded cells to get water height
    Flood_hgt = 0-Surface_level

    # Write the raster to a file    
    kwargs = dtm.meta 
    with rasterio.open(outputfilename, 'w', **kwargs) as file:
        file.write(Flood_hgt.astype(rasterio.float32))
        
    # Return the flood raster
    flood = rasterio.open(outputfilename, driver="GTiff")
    return flood


def geocodePlacenameToGDF(placename='Wageningen, Netherlands', epsg_code='28992'):
    """This function uses the OSMNX package to extract a geometry
    representing the placename provided as input and transforms to
    the required projection (EPSG code)."""
    # Load necessary package
    import osmnx as ox

    # Retrieve the GDF
    placeGDF = ox.geocoder.geocode_to_gdf(placename)

    # Check first whether there is any output to return
    if len(placeGDF) == 1:
        # Project GDFs to the required projection
        try:
            placeGDF = placeGDF.to_crs('EPSG:' + epsg_code)
        except:
            print("Given EPSG-code doesn't exist")
        else:
            return placeGDF
    else:
        print(
            "We're sorry, but the given placename is not found within OpenStreetMap. Check for typos or try another placename")


def ahn3_5m_forStudyArea(extent, outputfilename):
    """This function extracts for given extent (bbox) the AHN3 based Digital
    Terrain Model (DTM) with 5 meter resolution and saves as geotiff.
    bbox should be a list of bounding coordinates: [xmin, ymin, xmax, ymax]."""
    # Load necessary packages
    from owslib.wcs import WebCoverageService
    import rasterio

    # Specify the AHN3 wcs-url
    wcs = WebCoverageService('http://geodata.nationaalgeoregister.nl/ahn3/wcs?service=WCS', version='1.0.0')

    # Download and save DTM
    response = wcs.getCoverage(identifier='ahn3_5m_dtm', bbox=extent, format='GEOTIFF_FLOAT32',
                               crs='urn:ogc:def:crs:EPSG::28992', resx=5, resy=5)

    with open(outputfilename, 'wb') as file:
        file.write(response.read())

    # Load DTM
    dtm = rasterio.open(outputfilename, driver="GTiff")

    return dtm
