from .Shell import runShellCommand

def prepareTraining(baseModel, modelSource, projectFolder):
    downloadBaseModel(baseModel, modelSource, projectFolder)
    configurePipeline(baseModel, projectFolder)

def downloadBaseModel(baseModel, modelSource, projectFolder):
    print("Downloading Base Model...")
    compressedBaseModel = baseModel + ".tar.gz"
    modelDownloadUrl = modelSource + compressedBaseModel
    dataFolderPath = buildDataFolderPath(projectFolder)
    runShellCommand("cd " + dataFolderPath + " wget " + modelDownloadUrl)
    runShellCommand("cd " + dataFolderPath + "tar -xzvf  " + compressedBaseModel)

def configurePipeline(baseModel, projectFolder):
    print("Configuring Pipeline")
    dataFolderPath = buildDataFolderPath(projectFolder)
    modelConfigExamplePath = dataFolderPath + "/content/models/research/object_detection/configs/tf2/" + baseModel + ".config"
    runShellCommand("cp " + modelConfigExamplePath + " " + dataFolderPath)

def buildDataFolderPath(projectFolder):
    return "/mydrive/" + projectFolder + "/data/"