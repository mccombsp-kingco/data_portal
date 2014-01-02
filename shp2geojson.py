import os, subprocess, time

# identify a source directory of shapefiles
sourceDir = "/Users/paulmccombs/kccode/KC_Data/natres_SHP/natres/"

# test for expected projection print a warning if not expected state plane

# make a list of shape files
sourceList = ["agrpddst.shp",]

# identify an output directory
outputDir = "./" # current directory

# run the through the list of shape files
for shapeFile in sourceList:
    # reproject
    newName = "%sproj_%s"% (outputDir,shapeFile)
    print "sourceDir: ", sourceDir
    print "shapeFile: ", shapeFile
    oldName = "%s%s"% (sourceDir, shapeFile)
    print "oldName: ", oldName
    reprojectString = "ogr2ogr -t_srs EPSG:4326 %s %s"% (newName, oldName)
    print reprojectString
    os.system(reprojectString) 
    # convert to geoJSON
    fileNameList = shapeFile.split('.')
    jsonFileName = outputDir+fileNameList[0]+".geoJSON"
    print "jsonFileName: " , jsonFileName
    convertString = "ogr2ogr -f geoJSON %s %s"% (jsonFileName, newName)
    os.system(convertString)

# Use suprocess module to push revised data to github.
# Need to set both the --git-dir and --work-tree
# http://stackoverflow.com/questions/1386291/git-git-dir-not-working-as-expected
subprocess.call(['git','--git-dir', outputDir + '/.git',
                 '--work-tree', outputDir,
                 'add', jsonFileName])
subprocess.call(['git', '--git-dir', outputDir + '/.git',
                 '--work-tree', outputDir,
                 'commit', '-m', '"Data Upload: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + '"'])
subprocess.call(['git', '--git-dir', outputDir + '/.git',
                 '--work-tree', outputDir,'push'])