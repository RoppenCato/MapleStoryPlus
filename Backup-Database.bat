@echo off
rem Saves a copy of the game database (accounts, characters, items) to the Backups folder.
rem The database must be running. Safe to run while the game server is up.
set "ROOT=%~dp0"
if not exist "%ROOT%Backups" mkdir "%ROOT%Backups"
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HHmm"') do set "STAMP=%%i"
set "OUT=%ROOT%Backups\cosmic_%STAMP%.sql"
"%ROOT%Tools\mysql\bin\mysqldump" --defaults-file="%ROOT%Settings\mysql.ini" --single-transaction --routines --databases cosmic --result-file="%OUT%"
if errorlevel 1 (echo Backup FAILED.) else (echo Saved %OUT%)
if not defined NOPAUSE pause
