def runShellCommand(command):
    import subprocess
    return subprocess.check_output(command, shell=True).decode("utf-8").split("\n")

def prepareDependencies():
    import os
    import glob
    import xml.etree.ElementTree as ET
    import pandas as pd
    import tensorflow as tf
    import subprocess
    print(tf.__version__)

    # Check GPU version
    gpu_info = runShellCommand("nvidia-smi")
    gpu_info = '\n'.join(gpu_info)
    if gpu_info.find('failed') >= 0:
        print('Not connected to a GPU')
    else:
        print(gpu_info)

    # Mount Drive
    from google.colab import drive
    drive.mount('/content/gdrive')
    runShellCommand("ln -s /content/gdrive/My\ Drive/ /mydrive")

    # Setup Tensorflow
    runShellCommand("git clone --q https://github.com/tensorflow/models.git")
    runShellCommand("cd models/research")
    runShellCommand("protoc object_detection/protos/*.proto --python_out=.")
    runShellCommand("cp object_detection/packages/tf2/setup.py .")
    runShellCommand("python -m pip --q install .")

    # Correct opencv version
    import os
    desiredOpencvVersion = "4.1.2.30"
    opencvVersions = runShellCommand("pip list|grep opencv")
    for opencvSubLibraryVersion in opencvVersions:
        if desiredOpencvVersion not in opencvSubLibraryVersion:
            libraryName = opencvSubLibraryVersion.split(" ")[0]
            runShellCommand("pip uninstall $libraryName --y")
            runShellCommand("pip install $libraryName==$desiredOpencvVersion")
