@echo off
powershell %~dp0\lnnconf.ps1 apply %*
@ping 127.0.0.1 -n 2 > nul
