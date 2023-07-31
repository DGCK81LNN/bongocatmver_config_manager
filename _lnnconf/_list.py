import os
from sys import argv
import zipfile

if len(argv) > 1: raise ValueError("Too many arguments")
a_zip = os.path.join(os.path.dirname(__file__), 'configurations.zip')

with zipfile.ZipFile(a_zip) as zipf:
  names = [path.name for path in zipfile.Path(zipf).iterdir()]
  names.sort()
  print("\n".join(names))
