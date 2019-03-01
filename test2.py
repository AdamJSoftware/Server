import subprocess

address = os.getcwd() + "\MAC.ps1"
subprocess.Popen(["powershell.exe", address], stdout=sys.stdout)