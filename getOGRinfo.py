import subprocess

#########
# INSERT a test for expected projection print a warning if not expected state plane.
# look for results of eg. ogrinfo -so intrmpaa.shp intrmpaa
#
shapefile = '\\\\gisdw\kclib\plibrary2\planning\shapes\polygon\uac.shp'
shapefile = 'uac.shp'
layer = 'uac'

print 'ogrinfo -so ' + shapefile + ' ' + layer


p = subprocess.Popen('ogrinfo -so ' + shapefile + ' ' + layer, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# output is the result of the ogrinfo command. Test for the string 'NAD_1983_HARN_StatePlane_Washington_North_FIPS_4601_Feet'
output = p.communicate()
part = output[0]
if 'PROJCS' in part:
    if '"NAD_1983_HARN_StatePlane_Washington_North_FIPS_4601_Feet"' in part:
        print 'Passed projection test'
    # The following section should parse what the PROJCS is and state it
    else:
        print 'Projection for ' + shapefile + ' is not expected'
else:
    print 'Projection for ' + shapefile + ' is not defined'
            
     
    
### Result ####
# Had to open data source read-only.
# INFO: Open of `sfw_baldeaglebuf.shp'
    # using driver `ESRI Shapefile' successful.

# Layer name: sfw_baldeaglebuf
# Geometry: Polygon
# Feature Count: 140
# Extent: (1219834.108000, 64233.067000) - (1506083.741000, 279098.859000)
# Layer SRS WKT:
# PROJCS["NAD_1983_HARN_StatePlane_Washington_North_FIPS_4601_Feet",
    # GEOGCS["GCS_North_American_1983_HARN",
        # DATUM["NAD83_High_Accuracy_Reference_Network",
            # SPHEROID["GRS_1980",6378137.0,298.257222101]],
        # PRIMEM["Greenwich",0.0],
        # UNIT["Degree",0.0174532925199433]],
    # PROJECTION["Lambert_Conformal_Conic_2SP"],
    # PARAMETER["False_Easting",1640416.666666667],
    # PARAMETER["False_Northing",0.0],
    # PARAMETER["Central_Meridian",-120.8333333333333],
    # PARAMETER["Standard_Parallel_1",47.5],
    # PARAMETER["Standard_Parallel_2",48.73333333333333],
    # PARAMETER["Latitude_Of_Origin",47.0],
    # UNIT["Foot_US",0.3048006096012192]]
# BUFFER_FEA: String (254.0)
# MGTZONE_CO: Integer (5.0)
# MGTZONE_DE: String (254.0)
# SHAPE_area: Real (19.11)
# SHAPE_len: Real (19.11)

# ERROR 4: Unable to open sfw_baldeaglebuf.shp or sfw_baldeaglebuf.SHP.
### End Result ###
########


def getInfo():
    return "Does Nothing"
