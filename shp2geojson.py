"""
python shp2geojson.py <input directory path> <output directory path> {push to github?: github}
github argument requires being run from a functional git repository environment.
"""

import sys, os, subprocess, time, dir_list

# identify a source directory of shapefiles
#sourceDir = "/Users/paulmccombs/kccode/KC_Data/natres_SHP/natres/"

def shp2geojson(sourceDir, outputDir, github=0):
    """This is the main function of the script. It gets a list of shape files converts them to geoJSON and optionally posts them to github"""
    # make a list of shape files
    # INSERT a test to verify this is a directory and ends with a slash of some kind.
    sourceList = dir_list.shpFileList(sourceDir)

    # run the through the list of shape files
    for shapeFile in sourceList:

        # reproject
        # INSERT a test for expected projection print a warning if not expected state plane.
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
        jsonFileName = fileNameList[0]+".geoJSON"
        fulljsonFilePath = outputDir+jsonFileName
        print "output geoJSON path: " , fulljsonFilePath
        convertString = "ogr2ogr -f geoJSON %s %s"% (fulljsonFilePath, newName)
        os.system(convertString)
        if github:
            push_to_github(fulljsonFilePath, jsonFileName)
        
def push_to_github(fulljsonFilePath, jsonFileName):
    """Used to post geoJSON files up to github. This requires a functional git hub environment on your computer."""
    # Use suprocess module to push revised data to github.
    # This will choke horribly if geoJSON is over 100MB and you're trying to load to a free github account. Don't know if that changes with paid
    # account.
    # INSERT test for 100MB limit being exceeded.
    # CHANGE using code sample in commments below to make this run from a directory other than a functional git hub repository. Will require adding
    # a git repository directory as an agrument.
    # Note: changed from copy to cp and del to rm so it would run on OSX.
    # TEST in git bash to see if rm and cp are functional.
    # CONSIDER: testing for os environment and using commands as appropriate.
    os.system("cp %s .\\"% fulljsonFilePath)
    subprocess.call(['git', 'add', jsonFileName])
    subprocess.call(['git', 'commit', '-m', '"Data Upload: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + '"'])
    subprocess.call(['git', 'push'])
    os.system("rm %s"% jsonFileName)

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
        