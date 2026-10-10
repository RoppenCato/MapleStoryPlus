@echo off
rem Close the game server window first, then run this to shut the database down cleanly.
"%~dp0Tools\mysql\bin\mysqladmin" --defaults-file="%~dp0Settings\mysql.ini" shutdown
echo Database stopped.
pause
