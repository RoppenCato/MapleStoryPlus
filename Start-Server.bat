@echo off
title MapleStoryPlus Server
set "ROOT=%~dp0"
set "MYSQL=%ROOT%Tools\mysql\bin"
set "MYINI=%ROOT%Settings\mysql.ini"

"%MYSQL%\mysqladmin" --defaults-file="%MYINI%" ping >nul 2>&1
if not errorlevel 1 goto server

echo Starting database...
start "MapleStoryPlus Database" /min "%MYSQL%\mysqld" --defaults-file="%MYINI%" --console
:waitdb
ping -n 2 127.0.0.1 >nul
"%MYSQL%\mysqladmin" --defaults-file="%MYINI%" ping >nul 2>&1
if errorlevel 1 goto waitdb

:server
echo Starting game server...
cd /d "%ROOT%Server"
"%ROOT%Tools\java21\bin\java" -Xmx3g -Dwz-path=wz -Dconfig-path=..\Settings\config.yaml -jar target\Cosmic.jar
pause
