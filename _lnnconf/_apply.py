import os
from sys import argv
import zipfile

# Variable naming scheme
# a_xxx: absolute path
# r_xxx: path relative to 'root'
# p_xxx: path relative to 'parent'
# z_xxx: path inside zip file

a_root = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
a_zip = os.path.join(os.path.dirname(__file__), 'configurations.zip')

args = argv[1:]
options = True
while options and len(args) > 0:
  if args[0] == "--":
    options = False
  elif args[0].startswith("--"):
    raise ValueError(f"Unknown option {args[0]}")
  else:
    break
  args = args[1:]
if len(args) < 1:
  raise ValueError("Not enough arguments")
if len(args) > 1:
  raise ValueError("Too many arguments")
name = args[0]
if name == "":
  raise ValueError("Name must not be empty")

with zipfile.ZipFile(a_zip) as zipf:
  if not zipfile.Path(zipf, f"{name}/").exists():
    raise ValueError(f"Configuration '{name}' does not exist")

  for a_parent, _, p_files in os.walk(a_root):
    if os.path.samefile(a_parent, a_root): continue
    r_parent = os.path.relpath(a_parent, a_root)
    z_parent = f"{name}/{r_parent.replace(os.sep, '/')}"
    if zipfile.Path(zipf, f"{z_parent}/").exists():
      for p_file in p_files:
        a_file = os.path.join(a_parent, p_file)
        r_file = os.path.relpath(a_file, a_root)
        print(f"deleting: {os.path.join('.', r_file)}")
        os.remove(a_file)

  for z_file in zipf.namelist():
    if not z_file.startswith(f"{name}/"): continue
    if not zipfile.Path(zipf, z_file).is_file(): continue
    r_file = os.path.relpath(z_file, name)
    a_file = os.path.join(a_root, r_file)
    print(f"extracting: {z_file} --> {os.path.join(os.curdir, r_file)}")
    os.makedirs(os.path.dirname(a_file), exist_ok=True)
    with open(a_file, "wb") as file:
      file.write(zipf.read(z_file))

print(f"Applied configuration '{name}'")
