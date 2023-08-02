import os
from sys import argv
from collections.abc import Iterable
import zipfile

# Variable naming scheme
# a_xxx: absolute path
# r_xxx: path relative to 'root'
# p_xxx: path relative to 'parent'
# z_xxx: path inside zip file

def files(a_root: str, r_entries: Iterable[str]):
  r_files = list[str]()
  for r_entry in r_entries:
    a_entry = os.path.join(a_root, r_entry)
    if os.path.isdir(a_entry):
      for a_parent, _, p_files in os.walk(a_entry):
        for p_file in p_files:
          a_file = os.path.join(a_parent, p_file)
          r_file = os.path.relpath(a_file, a_root)
          r_files.append(r_file)
    elif os.path.isfile(a_entry):
      r_files.append(r_entry)
    else:
      raise ValueError(f"Entry does not exist: {r_entry}")
  return r_files

a_root = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
a_zip = os.path.join(os.path.dirname(__file__), "configurations.zip")

args = argv[1:]
config_json = True
options = True
while options and len(args) > 0:
  if args[0] == "--no-config-json":
    config_json = False
  elif args[0] == "--":
    options = False
  elif args[0].startswith("--"):
    raise ValueError(f"Unknown option {args[0]}")
  else:
    break
  args = args[1:]
if len(args) < 1:
  raise ValueError("Not enough arguments")

name = args[0]
if name == "":
  raise ValueError("Name must not be empty")
r_entries = args[1:]
if len(r_entries) == 0:
  r_entries = ["img"]
if config_json and not "config.json" in r_entries:
  r_entries.append("config.json")
#if len(r_entries) == 0: # unreachable
#  raise ValueError("Nothing to save")

r_entries_check = []
for r_entry in r_entries:
  if os.path.isabs(r_entry) or \
     os.path.normpath(r_entry) == os.curdir or \
     os.path.commonpath([r_entry, os.pardir]) != "":
    raise ValueError(f"Invalid entry: {r_entry}")

  r_entry_norm = os.path.normpath(r_entry)
  for r_existing_entry in r_entries_check:
    r_existing_entry_norm = os.path.normpath(r_existing_entry)
    r_common = os.path.commonpath([r_entry_norm, r_existing_entry_norm])
    if r_common in [r_entry_norm, r_existing_entry_norm]:
      raise ValueError(f"Duplicate or overlapping entries: {r_existing_entry}, {r_entry}")

  r_entries_check.append(r_entry)

with zipfile.ZipFile(a_zip, "a", zipfile.ZIP_DEFLATED) as zipf:
  if zipfile.Path(zipf, f"{name}/").exists():
    raise RuntimeError(f"Configuration '{name}' already exists")
  r_files = files(a_root, r_entries)
  for r_file in r_files:
    z_file = f"{name}/{r_file.replace(os.sep, '/')}"
    a_file = os.path.join(a_root, r_file)
    print(f"adding: {os.path.join(os.curdir, r_file)} --> {z_file}")
    zipf.write(a_file, z_file)
  print(f"Configuration successfully saved as '{name}'")
