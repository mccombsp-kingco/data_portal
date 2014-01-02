import os, subprocess, time


def pythonFileList(sourceDir):
    # make a list of shape files in provided directory
    fileList = os.listdir(sourceDir)
    shapeList = []
    for f in fileList:
        print "filename ", f
        parts = f.split('.')
        print "second part ", parts[1]
        if parts[1].lower() == 'shp' and len(parts) == 2:
            print "Found One!!"
            shapeList.append(f)
    return shapeList
   

sourceDir = "/Users/paulmccombs/kccode/KC_Data/natres_SHP/natres/"

print pythonFileList(sourceDir)