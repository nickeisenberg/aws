import subprocess 
import os

p = subprocess.run(
    "pip show pip | awk '/Location/ {print $2}'", 
    shell=True,
    capture_output=True,
    text=True
)

path = p.stdout.strip()

os.path.join(path, 'pyaws')
