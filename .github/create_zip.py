from zipfile import ZipFile
import os
import shutil

os.chdir("..")
zip = ZipFile('windows.zip', 'w')

for folderName, subfolders, filenames in os.walk("lang"):
           for filename in filenames:
               if filter(filename):
                   filePath = os.path.join(folderName, filename)
                   zip.write(filePath)
shutil.move("./dist/AudiosToTwitter.exe", "./AudiosToTwitter.exe")
zip.write("AudiosToTwitter.exe")
