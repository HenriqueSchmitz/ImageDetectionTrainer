def runShellCommand(command):
    import subprocess
    return subprocess.check_output(command, shell=True).decode("utf-8").split("\n")