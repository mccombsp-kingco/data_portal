import os, subprocess, time


def pythonFileList(sourceDir):
    # identify a source directory of shapefiles

    # test for expected projection print a warning if not expected state plane

    # make a list of shape files
    sourceList = ["agrpddst.shp",]


    for (dirpath, dirnames, filenames) in walk(mypath):
        f.extend(filenames)
        break

sourceDir = "/Users/paulmccombs/kccode/KC_Data/natres_SHP/natres/"

print pythonFileList(sourceDir)