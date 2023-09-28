@echo off
python %~dp0\lnnconf.py apply -- %*
if errorlevel 1 (
  pause
  exit /b %ERRORLEVEL%
) else (
  @ping 127.0.0.1 -n 2 > nul
)
