#########################################################################
# Shapefile to WKT Conversion
# Author: Aaron Taveras
# Date Created: 2/17/2022
# Debugging must done using Python 3x.
#########################################################################

import sys #include system specific parameters and functions
import os #include os library

import arcpy, string #include ArcGIS Python library
from arcpy import env #include ArcGIS Python Environment module
from arcpy.sa import* #include ArcGIS Spatial Analyst module

#########################################################################
## Create folder for intermediate processing files
#########################################################################

cf=r"C:/Temp/Temp_GIS_Files" #follow this path to locate processing files
if not os.path.exists(cf):
    os.makedirs(cf)

#########################################################################
## Mini function to send the print messages to the right output
## Input: Message-string to be printed
#########################################################################

def MyPrint(Message):
    if (RunningInArcPro): arcpy.AddMessage(Message)
    else: print(Message)

#########################################################################
## Determine if we are running within ArcPro (as a tool) or not
#########################################################################

RunningInArcPro=False #assume we are not running as a tool in ArcPro

if (len(sys.argv))>1: #if parameters are present, run in ArcPro as a tool
    RunningInArcPro=True

#########################################################################
## Set input paths
#########################################################################

inputSHP=r"C:\Users\aTaveras\Desktop\Peavine_Property\Peavine_Property.shp" #default input path (enter shapefile path here)

#########################################################################
# Set output paths
#########################################################################

output="C:/Users/aTaveras/Desktop/WKT_Conversion.txt" #default output path

#########################################################################
# If running in a tool, get the parameters from the Arc Tool GUI
#########################################################################

if (RunningInArcPro): #if running in a tool, get the parameters from the Arc Tool GUI
    inputSHP=arcpy.GetParameterAsText(0) #sets parameter for Shapefile input in ArcPro
    output=arcpy.GetParameterAsText(1) #sets parameter for WKT ouput in ArcPro

#########################################################################
# Prints all parameters for debugging
#########################################################################

MyPrint("inputSHP: "+inputSHP)
MyPrint("ouput: "+output)

#########################################################################
## Run the script repeatedly without deleting the intermediate files
#########################################################################

arcpy.env.overwriteOutput=True

#########################################################################
## Pre-processing
#########################################################################

MyPrint("#-----Begining Pre-Processing-----#") #prints message to ArcPro dialog that processing has begun

try:
    dfc = arcpy.management.Dissolve(inputSHP, "C:\Temp\Temp_GIS_Files\wkt_temp.shp", "", "", "MULTI_PART", "") #create multipart feature
    sr = arcpy.SpatialReference('WGS 1984 Web Mercator (Auxiliary Sphere)') #output WKT in WGS 1984 Web Mercator (Auxiliary Sphere)

    MyPrint(arcpy.GetMessages()) #prints ArcPro dialog processing messages
    MyPrint("#-----Pre-Processing Completed Successfully-----#") #prints message to ArcPro dialog

except:
    MyPrint(arcpy.GetMessages()) #prints ArcPro dialog processing messages
    MyPrint("#-----Failed-----#") #prints message to ArcPro dialog

#########################################################################
## File conversion
#########################################################################

MyPrint("#-----Begining Conversion-----#") #prints message to ArcPro dialog that processing has begun

try:
    cursor = arcpy.da.SearchCursor(dfc, ["SHAPE@WKT"], spatial_reference=sr) #convert to WKT projected on the fly and print
    for row in cursor:
        print(row[0])

    MyPrint("#-----Conversion Completed Successfully-----#") #prints message to ArcPro dialog

except:
    MyPrint("#-----Failed-----#") #prints message to ArcPro dialog

#########################################################################
## Save result to file
#########################################################################

MyPrint("#-----Saving Result to File-----#") #prints message to ArcPro dialog that processing has begun

try:
    with open(output, "w") as outputWKT:
        print(row[0], file=outputWKT)

    del row
    del cursor

    MyPrint("#-----Result was Saved Successfully-----#") #prints message to ArcPro dialog

except:
    MyPrint("#-----Failed-----#") #prints message to ArcPro dialog
