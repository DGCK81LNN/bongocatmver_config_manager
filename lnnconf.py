#!/usr/bin/env python
import os
import re
import zipfile
from collections.abc import Iterable
from sys import argv
from textwrap import dedent
from time import sleep
from traceback import print_exc

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

print(__file__)

a_root = os.path.normpath(os.path.dirname(__file__))
a_zip = os.path.join(os.path.dirname(__file__), 'lnnconf_configurations.zip')
a_tmp = os.path.join(os.path.dirname(__file__), 'lnnconf_temp.zip')
shell_mode = False

def cmdSave(*args: str):
  """
  save [options...] [--] <name> [entry...]
  Save a new configuration.

  Aliases: s, add

  Parameters:
    name    Name of the new configuration.
            Must not be the same as an existing saved configuration.
    entry   Names of files and directories to include.
            Defaults to 'img'.
            All specified entries must exist.
            'config.json' is implicitly included unless --no-config-json is
            specified. To include only 'config.json' and not 'img', pass
            'config.json'.
  Options:
    --no-config-json  Do not include config.json in the saved configuration.

  Example:
    save myconfig img/standard Resources config.json
  """
  argl = list(args)
  config_json = True
  options = True
  while options and len(argl) > 0:
    if argl[0] == "--":
      options = False
    elif argl[0] == "--no-config-json":
      config_json = False
    elif argl[0] == "--help":
      return cmdHelp("save")
    elif argl[0].startswith("--"):
      raise ValueError(f"Unknown option {argl[0]}")
    else:
      break
    argl.pop(0)
  if len(argl) < 1:
    raise ValueError("Not enough arguments")

  name = argl[0]
  if name == "":
    raise ValueError("Name must not be empty")
  r_entries = argl[1:]
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

def cmdList(*args: str):
  """
  list
  List saved configurations.

  Aliases: l, ls
  """
  if (len(args) > 0):
    if args[0] == "--help":
      return cmdHelp("list")
    raise ValueError("Too many arguments")
  with zipfile.ZipFile(a_zip) as zipf:
    names = [path.name for path in zipfile.Path(zipf).iterdir()]
    names.sort()
    print("\n".join(names))

def cmdApply(*args: str):
  """
  apply <name>
  Apply a configuration.
  This may delete some of the existing files on disk.

  Alias: a, load
  """
  argl = list(args)
  options = True
  while options and len(argl) > 0:
    if argl[0] == "--":
      options = False
    elif argl[0] == "--help":
      return cmdHelp("apply")
    elif argl[0].startswith("--"):
      raise ValueError(f"Unknown option {argl[0]}")
    else:
      break
    argl.pop(0)
  if len(argl) < 1:
    raise ValueError("Not enough arguments")
  if len(argl) > 1:
    raise ValueError("Too many arguments")
  name = argl[0]
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

def cmdDelete(*args: str):
  """
  delete <name...>
  Delete saved configuration(s).

  Aliases: d, del, rm
  """
  argl = list(args)
  options = True
  while options and len(argl) > 0:
    if argl[0] == "--":
      options = False
    elif argl[0] == "--help":
      return cmdHelp("delete")
    elif argl[0].startswith("--"):
      raise ValueError(f"Unknown option {argl[0]}")
    else:
      break
    argl.pop(0)
  if len(argl) < 1:
    raise ValueError("Not enough arguments")
  for name in argl:
    if name == "":
      raise ValueError("Name must not be empty")

  with zipfile.ZipFile(a_zip, 'r') as zipf:
    for name in argl:
      if not zipfile.Path(zipf, f"{name}/").exists():
        raise RuntimeError(f"Configuration '{name}' does not exist")

    with zipfile.ZipFile(a_tmp, 'w', zipfile.ZIP_DEFLATED) as tmpf:
      for z_file in zipf.namelist():
        if not zipfile.Path(zipf, z_file).is_file(): continue
        if any(map(lambda name: z_file.startswith(f"{name}/"), argl)):
          print(f"deleting: {z_file}")
        else:
          tmpf.writestr(z_file, zipf.read(z_file))
  os.replace(a_tmp, a_zip)

  print(f"""Deleted configuration{'s' if len(argl) > 1 else ''} {", ".join(f"'{name}'" for name in argl)}""")

def cmdHelp(*args: str):
  """
  help [command]
  Show help.

  Aliases: h, ?
  """
  if len(args) > 0 and args[0] == "--help":
    return cmdHelp("help")
  elif len(args) > 1:
    raise ValueError("Too many arguments")
  elif len(args) == 0:
    overviews = [
      "save <name> [entry...]    Save a new configuration",
      "list                      List saved configurations",
      "apply <name>              Apply a configuration",
      "delete <name...>          Delete saved configuration(s)",
      "help [command]            Show help",
    ]
    if shell_mode:
      overviews.append(
        "exit                      Exit lnnconf shell"
      )
    if not shell_mode:
      print(f"Usage: {os.path.basename(__file__)} <command> [args...]\n")
    print("Commands:\n" + "\n".join(overviews))
  else:
    command = args[0]
    if command in commands:
      print(dedent(commands[command].__doc__).strip("\n"))
    else:
      raise ValueError(f"Unknown command '{command}'")

def cmdExit(*args: str):
  """
  exit
  Exit lnnconf shell.

  Aliases: q, quit
  """
  global shell_mode
  if len(args) > 0 and args[0] == "--help":
    return cmdHelp("exit")
  if shell_mode:
    shell_mode = False
  else:
    raise RuntimeError("Not in shell mode")

commands = {
  "save": cmdSave,
  "s": cmdSave,
  "add": cmdSave,
  "list": cmdList,
  "l": cmdList,
  "ls": cmdList,
  "apply": cmdApply,
  "a": cmdApply,
  "load": cmdApply,
  "delete": cmdDelete,
  "d": cmdDelete,
  "del": cmdDelete,
  "rm": cmdDelete,
  "help": cmdHelp,
  "h": cmdHelp,
  "?": cmdHelp,
  "exit": cmdExit,
  "quit": cmdExit,
  "q": cmdExit,
  #"echo": print,
}

args = argv[1:]
options = True
while options and len(args) > 0:
  if args[0] == "--":
    options = False
  elif args[0] == "--help" or args[0] == "-h":
    cmdHelp(*args[1:])
    exit()
  elif args[0].startswith("--"):
    raise ValueError(f"Unknown option {args[0]}")
  else:
    break
  args.pop(0)

def run_command(*args: str):
  command = args[0]
  if command in commands:
    commands[command](*args[1:])
  else:
    raise ValueError(f"Unknown command '{command}'")

if len(args) == 0:
  print()
  print(dedent("""
  Welcome to lnnconf shell!
  Type 'help' to show available commands
  Type 'exit' to quit
  """).strip("\n"))
  shell_mode = True
  while shell_mode:
    print()
    try:
      cmd = input("lnnconf shell> ")
      args = list(map(
        lambda m: re.sub(
          '(["\'])(\\\\?.)*?\\1|["\'].*',
          lambda m: eval(m[0]),
          m[0]
        ),
        re.finditer('(?:(["\'])(\\\\?.)*?\\1|\\S)+', cmd)
      ))
      if (len(args) > 0):
        run_command(*args)
    except EOFError:
      break
    except KeyboardInterrupt:
      pass
    except:
      print_exc()
  print("bye")
  sleep(1/3)
else:
  run_command(*args)
