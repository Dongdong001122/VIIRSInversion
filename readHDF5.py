import  os
from osgeo import gdal

## List input raster files
os.chdir(r"G:\geodata\VIIRS\VIIRSdata")
rasterFiles = os.listdir(os.getcwd())
print(rasterFiles)

## Open HDF file
hdflayer = gdal.Open(rasterFiles[0], gdal.GA_ReadOnly)

# Open raster layer
rlayer = gdal.Open(hdflayer.GetSubDatasets()[0][0], gdal.GA_ReadOnly)

# Define output raster and warp-reproject
outputName = '_test.tiff'
outputRaster = '..\\outputRaster'+ outputName
gdal.Warp(outputRaster,rlayer,dstSRS='EPSG:4326')

# Add output raster to canvas
# iface.addRasterLayer(outputRaster, outputName)