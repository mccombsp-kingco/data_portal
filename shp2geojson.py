"""
python shp2geojson.py <input directory path> <output directory path> {push to github?: github}
github argument requires being run from a functional git repository environment.
"""

import sys, os, subprocess, time, dir_list, getOGRinfo

# identify a source directory of shapefiles
#sourceDir = "/Users/paulmccombs/kccode/KC_Data/natres_SHP/natres/"
def fixDirname(dirName):
	if dirName[-1] <> os.sep:
	    dirName = dirName + os.sep
	return dirName

def shp2geojson(oldShapePath, jsonPath):
    """Converts input shape file to a geoJSON file which is reprojected to web mercator.
    Returns a list containing text objects with information discovered durring the conversion"""
    
    returnList = []
    
    ####
    # Reproject Needed?
    ####
    # INSERT a test for expected projection print a warning if not expected state plane.
    # look for results of eg. ogrinfo -so intrmpaa.shp intrmpaa
    # returnList.append(getOGRinfo.getInfo())
    ####

    # reprojectString = "ogr2ogr -t_srs EPSG:4326 %s %s"% (newShapePath, oldShapePath)
    # returnList.append(reprojectString)
    # os.system(reprojectString)
 
    ####
    # This convert string specifies format and projection all together.
    convertString = "ogr2ogr -f geoJSON -t_srs EPSG:4326 %s %s"% (jsonPath, oldShapePath)
    returnList.append(convertString)
    os.system(convertString)
  
def wholeDirLoop (sourceDir, outputDir, github=0):
    """This looks into a directory and creates a list of shape files, which is then looped through to 
    convert each shape file to a  geoJSON reprojected to web mercator, and optionally posts them to github"""
    # make a list of shape files
    sourceDir = fixDirname(sourceDir)
    outputDir = fixDirname(outputDir)

    sourceList = dir_list.shpFileList(sourceDir)


    # run the through the list of shape files
    for shapeFile in sourceList:

        ####
        # Process the directory names and the shape file name to pass to the conversion function (shp2geojson)
        #newShapePath = "%sproj_%s"% (outputDir, shapeFile) # New shape file full path
        oldShapePath = "%s%s"% (sourceDir, shapeFile)      # Old shape file full path
        fileNameList = shapeFile.split('.') # This is problematic if there are multiple '.'s in the shape file name
        jsonFileName = fileNameList[0]+".geojson"
        jsonPath = outputDir+jsonFileName     # New geoJSON file full path

        statusList = shp2geojson(oldShapePath, jsonPath)
        print statusList
        
        ####
        # Test for need to push to github and call push_to_github if needed.
        if github:
            push_to_github(jsonPath, jsonFileName)
        
def push_to_github(fulljsonFilePath, jsonFileName):
    """Used to post geoJSON files up to github. This requires a functional git hub environment on your computer."""
    # Use suprocess module to push revised data to github.
    # INSERT test for 100MB limit being exceeded.
    # CHANGE using code sample in commments below to make this run from a directory other than a functional git hub repository. Will require adding
    # a git repository directory as an agrument.
    # TEST in git bash to see if rm and cp are functional.
    # CONSIDER: testing for os environment and using commands as appropriate.

    # This will choke horribly if geoJSON is over 100MB and you're trying to load to a free github account. Will not draw a map with a specific 27MB
    # file that was tested. Setting the limit to 10MB at present. -pm Don't know if that changes with paid account. Testing to prevent that outcome.
    jsonInfo = os.stat(fulljsonFilePath)
    if jsonInfo.st_size > 10000000:
        print "%s is larger than 10MB and will not be loaded to github due to size restrictions."% fulljsonFilePath
    
    # git push happens here
    else:
        if os.name == 'nt':
            os.system("copy %s .\\"% fulljsonFilePath)
        else: # this hasn't been tested. Should add a test for each other system that we use and a final else that says "too bad."
            os.system("cp %s .\\"% fulljsonFilePath)
            
        subprocess.call(['git', 'add', jsonFileName])
        subprocess.call(['git', 'commit', '-m', '"Data Upload: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + '"'])
        subprocess.call(['git', 'push'])
    #Cleaning up after posting caused problems sychronizing with github: os.system("rm %s"% jsonFileName)

    # This was the code sample from stack overflow that Peter Keum found. It was working but only when everything was in the same directory.
    # It wasn't working for me and I messed arrond with it, I finaly decided to copy my files into the current working directory. Ended up
    # stripping out a lot of the complications as they weren't relevant in that context. But keeping here for future repairs.
    # # Use suprocess module to push revised data to github.
    # # Need to set both the --git-dir and --work-tree
    # # http://stackoverflow.com/questions/1386291/git-git-dir-not-working-as-expected
    # subprocess.call(['git','--git-dir', outputDir + '/.git',
                     # '--work-tree', outputDir,
                     # 'add', jsonFileName])
    # subprocess.call(['git', '--git-dir', outputDir + '/.git',
                     # '--work-tree', outputDir,
                     # 'commit', '-m', '"Data Upload: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + '"'])
    # subprocess.call(['git', '--git-dir', outputDir + '/.git',
    #                '--work-tree', outputDir,'push'])
                     
if __name__ == '__main__':
    try:
        for arg in sys.argv:
            print "Argument: %s"% arg
        if len(sys.argv) > 1:
            print "Looking for shape files in %s"% sys.argv[1]
            if len (sys.argv) == 3:
                    print "Will not attempt to post geoJSON files to github"
                    wholeDirLoop(sys.argv[1], sys.argv[2])
            if len(sys.argv) > 3:
                print "Will put geoJSON files in %s"% sys.argv[2]
                if sys.argv[3].lower() == "github":
                    print "Will attempt to post geoJSON files to github"
                    wholeDirLoop(sys.argv[1], sys.argv[2], "github")

        else: print __doc__

    except:
        print __doc__
        raise
        
