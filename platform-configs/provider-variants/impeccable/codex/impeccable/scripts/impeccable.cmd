@echo off
setlocal
rem Local library adaptation: explicit approved engine only; never download or install.
if defined IMPECCABLE_LIBRARY_LAUNCH goto recursive
if not defined IMPECCABLE_BIN goto unavailable
if not "%IMPECCABLE_BIN:~1,2%"==":\" if not "%IMPECCABLE_BIN:~0,2%"=="\\" goto unavailable
if not exist "%IMPECCABLE_BIN%" goto unavailable
if /I "%~1"=="install" goto management
if /I "%~1"=="update" goto management
if /I "%~1"=="hooks" goto management
if /I "%~1"=="pin" goto management
set "IMPECCABLE_SKILL_DIR=%~dp0.."
set "IMPECCABLE_SELF=%~f0"
set "IMPECCABLE_LIBRARY_LAUNCH=1"
"%IMPECCABLE_BIN%" %*
exit /b %errorlevel%
:unavailable
echo impeccable: set IMPECCABLE_BIN to an approved absolute engine path; no download attempted; use manual context fallback otherwise 1>&2
exit /b 127
:recursive
echo impeccable: recursive launcher refused 1>&2
exit /b 126
:management
echo impeccable: installation, updates, hooks and shortcut management are outside this library launcher 1>&2
exit /b 126
