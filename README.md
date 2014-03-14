test 004

data_portal
===========

python utilities to prepare data for posting in the King County Data Portal

shp2geojson.py - this the main piece of code that will do the translation and posting

dir_list.py - this is where i'm working on producing a list of shapefiles when given a directory string.

================
Installing gdal on Windows has been sketchy. Google says use http://www.gisinternals.com/sdk/

but gisinternals is non-responsive on 1/2/2014, found some evidence that others have had same problem over last 2 days.

Current attempt is as follows. Go to http://www.maptools.org/ms4w/index.phtml?page=downloads.html . 
Download the stable zip archive. Copy gdaldata, gdaplugins, and tools/gdal-ogr from ms4w in the zip archive 
to c:\Program Files\gdal directory. Add C:\Program Files\gdal\gdal-ogr to the PATH system variable. Create new 
system variables as follows: GDAL_DATA=\ms4w\gdaldata & GDAL_DRIVER_PATH=\ms4w\gdalplugins. From zip archive 
ms4w/Apache/cgi-bin/ copy *.dll to c:\program files\gdal\gdal-ogr. 

