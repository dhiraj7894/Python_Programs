import os
import os.path
import shutil
import fnmatch
RootDir1 = r'/home/makerghat/Desktop/GIS/'
TargetFolder = r'/home/makerghat/Desktop/GIS_2'
for root, dirs, files in os.walk((os.path.normpath(RootDir1)), topdown=False):
        for name in files:
            if name.endswith('.zip'):
                print("Found")
                SourceFolder = os.path.join(root,name)
                shutil.move(SourceFolder, TargetFolder)
