$LNNCONFDIR = Join-Path (Split-Path $MyInvocation.MyCommand.Path) "_lnnconf"

$cmd = $args[0]
$cmdargs = $args | Select-Object -Skip 1

if (-not $cmd -or $cmd -eq "--help" -or $cmd -eq "help" -or $cmd -eq "/?") {
  $me = [System.IO.Path]::GetFileNameWithoutExtension($MyInvocation.MyCommand.Path)
  Write-Host @"
Usage: $me <command> [args...]

Commands:
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
      $me save myconfig img/standard Resources config.json

  list
    List saved configurations.

    Aliases: l, ls

  apply <name>
    Apply a configuration.
    This may delete some of the existing files on disk.

    Alias: a, load

  delete <name...>
    Delete saved configuration(s).

    Example:
      $me delete config1 config2

    Aliases: d, del, rm
"@
  exit
}

if     ($cmd -eq "s" -or $cmd -eq "add") { $cmd = "save" }
elseif ($cmd -eq "l" -or $cmd -eq "ls") { $cmd = "list" }
elseif ($cmd -eq "a" -or $cmd -eq "load") { $cmd = "apply" }
elseif ($cmd -eq "d" -or $cmd -eq "del" -or $cmd -eq "rm")  { $cmd = "delete" }

if (Test-Path (Join-Path $LNNCONFDIR "_$cmd.py")) {
  python (Join-Path $LNNCONFDIR "_$cmd.py") $cmdargs
  exit $LASTEXITCODE
} else {
  Write-Host "Unknown command '$cmd'"
  exit 2
}
