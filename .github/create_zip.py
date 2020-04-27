from zipfile import ZipFile
import os
import shutil

zip = ZipFile('windows.zip', 'w')

for folderName, subfolders, filenames in os.walk("lang"):
    for filename in filenames:
        filePath = os.path.join(folderName, filename)
        zip.write(filePath)
        print("Adding " + str(filePath))
shutil.move("./dist/AudiosToTwitter.exe", "./AudiosToTwitter.exe")
print("Adding .exe")
zip.write("AudiosToTwitter.exe")
