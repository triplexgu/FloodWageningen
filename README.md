# Flooding Risk Wageningen

## Requirements
- Task 1: Apply the `geocodePlacenameToGDF()` function to the municipality of Wageningen. Extract the bounding box values from the resulting `placeGDF` and save these to a variable `bbox`. You will need these for the next step; as input for the function `ahn3_5m_forStudyArea()`. Apply the function `ahn3_5m_forStudyArea()` to the extent given by `bbox` and save the results into variable `dtm`.

- Task 2: Fill in and apply the function `calcFloodMap()`, which has already been given with some structure, but without the functional code. It is a function that, given (1) a DTM, (2) water height, and (3) an output filename, writes **and** returns a simple water depth map (unit is meters water depth). No need for complex flood models for now, simply assume that locations below the given water height will be flooded. Note that water bodies and buildings have a value of 0 in the AHN3. Refer to the Python Raster Tutorial for help with `rasterio`.

- Task 3: Calculate the following statistics derived from the floodmap for a 10 meter case: `maxWaterDepth` (m) `averageWaterDepth` (m) and `percWaterCoverage` (%). Additionally, plot a (static or dynamic) map with the water depth in meters. Include the geometry outline of the municipality of Wageningen. During all three tasks, pay attention to the documentation and structure of your Python scripts.

## Extra (only attempt if you finished and tested the above without errors)
Calculate how much of the roads is within the flooded zone and save it to a variable `percWetRoads` (the length (m) of (partly) flooded roads divided by total length of all roads)). Extract the roads from osm.
