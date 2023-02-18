# from osgeo import gdal
# import arcpy.management
from arcpy.sa import *
import pandas as pd
import arcpy

arcpy.env.workspace = "G:\\geodata\\VIIRS\\VIIRSdata"
"""
hdfname="GMODO-SVM12-SVM13-SVM15-SVM16_npp_d20200725_t0416261_e0422065_b45298_c20230130025703192209_nobc_ops.h5"

ds=gdal.Open("G:\\geodata\\VIIRS\\VIIRSdata\\"+hdfname) # load the hdf file by gdal
subdatasets = ds.GetSubDatasets() # get the list of the sub datasets

arcpy.ExtractSubDataset_management(hdfname,"M12.tif","1")
"""


# Read VIIRS data
M12=Raster(r"G:\geodata\VIIRS\test2\GMODO-SVM12-SVM13-SVM15-SVM16_npp_d20200725_t0416261_e0422065_b45298_c20230130025703192209_nobc_ops_MOD_Radiance.dat","0") #T3.75
M13=Raster(r"G:\geodata\VIIRS\test2\GMODO-SVM12-SVM13-SVM15-SVM16_npp_d20200725_t0416261_e0422065_b45298_c20230130025703192209_nobc_ops_MOD_Radiance.dat","1") #T40
M15=Raster(r"G:\geodata\VIIRS\test2\GMODO-SVM12-SVM13-SVM15-SVM16_npp_d20200725_t0416261_e0422065_b45298_c20230130025703192209_nobc_ops_MOD_Radiance.dat","2") #T11
M16=Raster(r"G:\geodata\VIIRS\test2\GMODO-SVM12-SVM13-SVM15-SVM16_npp_d20200725_t0416261_e0422065_b45298_c20230130025703192209_nobc_ops_MOD_Radiance.dat","3") #T12
VZA=Raster(r"G:\geodata\VIIRS\test2\VZA.tif") #θ
SZA=Raster(r"G:\geodata\VIIRS\test2\SZA.tif") #φ


landCover=Raster(r"G:\geodata\VIIRS\landCover\landcover2020.tif")

# Reclassify
df=pd.read_excel(r"Coefficients.xlsx",sheet_name="LST",index_col="IGBP_ID") # read the coefficient table
df.pop("Type") # delete the colmun in string
df=df*1000000
df=df.astype("int")
#
# for c in df.columns:
#     df[c]=df[c].astype("int")

coe_dict={}
for c in df.columns: # create the raster with each coefficient
    coe_list = [[0, "NODATA"]]
    for i in df.index:
        # print(df.a0[i])
        coe_list.append([i, df[c][i]])
    remap = RemapValue(coe_list)
    outReclassify = Reclassify(landCover, "Value", remap, "NODATA")  # Execute Reclassify
    outReclassify *= 0.000001
    coe_dict.update({c:outReclassify})
    print(c,"Min:",outReclassify.minimum)

# Calculate the LST
LST=coe_dict["a0"]+M15*coe_dict["a1"]+(M15-M16)*coe_dict["a2"]+(1/Cos(VZA)-1)*coe_dict["a3"]+M12*coe_dict["a4"]+M13*coe_dict["a5"]
+ M15*Cos(SZA)*coe_dict["a6"]+  M16*Cos(SZA)*coe_dict["a7"]+(M15-M16)**2*coe_dict["a8"]
print(LST)




# arcpy.ddd.Reclassify("landcover2020.tif", "Value", "0 1;1 2;2 3;3 4;4 5;5 6;6 7;7 8;8 9;9 10;10 11;11 12;12 13;13 14;14 15;15 16;16 17;17 18", r"G:\geodata\VIIRS\MapProject\MapProject.gdb\Reclass_land1", "DATA")