@echo off
rem Rebuilds the server after code changes. Stop the game server first.
set "JAVA_HOME=%~dp0Tools\java21"
set "PATH=%JAVA_HOME%\bin;%PATH%"
cd /d "%~dp0Server"
call mvnw.cmd clean package -Dmaven.test.skip
pause
