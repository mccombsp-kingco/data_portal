import subprocess, time

subprocess.call(['git', 'add', 'README.md'])
subprocess.call(['git', 'commit', '-m', '"Push Test: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + '"'])
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
                 
