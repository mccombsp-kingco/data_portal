"""
python shp2geojson.py <input directory path> <output directory path> {push to github?: github}
"""

import sys, os, subprocess, time, dir_list

# identify a source directory of shapefiles
#sourceDir = "/Users/paulmccombs/kccode/KC_Data/natres_SHP/natres/"

def shp2geojson(sourceDir, outputDir, github=0):
    """This is the main function of the script. It gets a list of shape files converts them to geoJSON and optionally posts them to github"""
    # test for expected projection print a warning if not expected state plane.
    # to be implemented later

    # make a list of shape files
    sourceList = dir_list.shpFileList(sourceDir)

    # identify an output directory
    #outputDir = "./" # current directory

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
    if github:
        push_to_github(outputDir, jsonFileName)
        
def push_to_github(outputDir, jsonFileName): #Note I probably broke this when I modularized the script. Not sure if it will work with the directories as is -pm
    """Used to post geoJSON files up to github. This requires a functional git hub environment on your computer."""
    # Use suprocess module to push revised data to github.
    # Need to set both the --git-dir and --work-tree
    # http://stackoverflow.com/questions/1386291/git-git-dir-not-working-as-expected
    subprocess.call(['git','--git-dir', './.git',
                     '--work-tree', './.git',
                     'add', jsonFileName])
    subprocess.call(['git', '--git-dir', './.git',
                     '--work-tree', './.git',
                     'commit', '-m', '"Data Upload: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + '"'])
    subprocess.call(['git', '--git-dir', './.git', '--work-tree', './.git', 'push'])

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
                    shp2geojson(sys.argv[1], sys.argv[2])
            if len(sys.argv) > 3:
                print "Will put geoJSON files in %s"% sys.argv[2]
                if sys.argv[3].lower() == "github":
                    print "Will attempt to post geoJSON files to github"
                    shp2geojson(sys.argv[1], sys.argv[2], "github")

        else: print __doc__

    except:
        print __doc__
        raise
        