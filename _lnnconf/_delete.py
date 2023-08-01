import os
from sys import argv
import zipfile

a_zip = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'configurations.zip')
a_tmp = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'temp.zip')

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
for name in args:
  if name == "":
    raise ValueError("Name must not be empty")

with zipfile.ZipFile(a_zip, 'r') as zipf:
  for name in args:
    if not zipfile.Path(zipf, f"{name}/").exists():
      raise RuntimeError(f"Configuration '{name}' does not exist")

  with zipfile.ZipFile(a_tmp, 'w', zipfile.ZIP_DEFLATED) as tmpf:
    for z_file in zipf.namelist():
      if not zipfile.Path(zipf, z_file).is_file(): continue
      if any(map(lambda name: z_file.startswith(f"{name}/"), args)):
        print(f"deleting: {z_file}")
      else:
        tmpf.writestr(z_file, zipf.read(z_file))
os.replace(a_tmp, a_zip)

print(f"""Deleted configuration{'s' if len(args) > 1 else ''} {", ".join(f"'{name}'" for name in args)}""")
