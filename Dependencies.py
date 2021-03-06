def prepareDependencies():
    import os
    import glob
    import xml.etree.ElementTree as ET
    import pandas as pd
    import tensorflow as tf
    print(tf.__version__)

    # Check GPU version
    gpu_info = !nvidia-smi
    gpu_info = '\n'.join(gpu_info)
    if gpu_info.find('failed') >= 0:
        print('Not connected to a GPU')
    else:
        print(gpu_info)

    # Mount Drive
    from google.colab import drive
    drive.mount('/content/gdrive')
    !ln -s /content/gdrive/My\ Drive/ /mydrive

    # Setup Tensorflow
    !git clone --q https://github.com/tensorflow/models.git
    %cd models/research
    !protoc object_detection/protos/*.proto --python_out=.
    !cp object_detection/packages/tf2/setup.py .
    !python -m pip --q install .

    # Correct opencv version
    import os
    desiredOpencvVersion = "4.1.2.30"
    opencvVersions = !pip list|grep opencv
    for opencvSubLibraryVersion in opencvVersions:
        if desiredOpencvVersion not in opencvSubLibraryVersion:
            libraryName = opencvSubLibraryVersion.split(" ")[0]
            !pip uninstall $libraryName --y
            !pip install $libraryName==$desiredOpencvVersion