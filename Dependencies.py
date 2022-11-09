def runShellCommand(command):
    import subprocess
    return subprocess.check_output(command, shell=True).decode("utf-8").split("\n")

def displayGpuInformation():
    gpu_info = runShellCommand("nvidia-smi")
    gpu_info = '\n'.join(gpu_info)
    if gpu_info.find('failed') >= 0:
        print('Not connected to a GPU')
    else:
        print(gpu_info)

def mountDrive():
    print("Mounting Google Drive...")
    from google.colab import drive
    drive.mount('/content/gdrive')
    runShellCommand("ln -s /content/gdrive/My\ Drive/ /mydrive")

def setupTensorflowModels():
    print("Cloning Tensorflow models from https://github.com/tensorflow/models.git...")
    runShellCommand("git clone --q https://github.com/tensorflow/models.git")
    print("Building Tensorflow models...")
    runShellCommand("cd models/research && protoc object_detection/protos/*.proto --python_out=.")
    runShellCommand("cd models/research && cp object_detection/packages/tf2/setup.py .")
    print("Installing Tensorflow models...")
    runShellCommand("cd models/research && python -m pip --q install .")

def correctOpencvVersion(desiredOpencvVersion):
    print("Correcting OpenCV versions to use version " + desiredOpencvVersion)
    opencvVersions = runShellCommand("pip list|grep opencv")
    for opencvSubLibraryVersion in opencvVersions:
        if desiredOpencvVersion not in opencvSubLibraryVersion:
            libraryName = opencvSubLibraryVersion.split(" ")[0]
            if libraryName != "": 
                print("Correcting library version for " + libraryName)
                runShellCommand("pip uninstall " + str(libraryName) + " --y")
                runShellCommand("pip install " + str(libraryName) + "==" + str(desiredOpencvVersion))

def prepareDependencies():
    import os
    import glob
    import xml.etree.ElementTree as ET
    import pandas as pd
    import tensorflow as tf
    import subprocess
    print("Tensorflow version: " + tf.__version__)

    displayGpuInformation()
    mountDrive()
    setupTensorflowModels()
    correctOpencvVersion("4.1.2.30")
