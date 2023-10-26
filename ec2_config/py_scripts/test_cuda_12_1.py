"""
This is to be run on the ec2 instance with that has cuda 12.1
"""

try:
    import cupy
    print("cupy can be imported")
except:
    print("cupy could not be imported")

from numba.cuda import is_available as numba_works
from torch.cuda import is_available as torch_works

if numba_works():
    print("Numba cuda works")
else:
    print("Numba does not work")

if torch_works():
    print("torch cuda works")
else:
    print("torch does not work")
