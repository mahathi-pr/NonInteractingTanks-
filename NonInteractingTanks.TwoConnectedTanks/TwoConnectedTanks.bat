@echo off
SET PATH=;C:/Users/G Mahathi/Desktop/NonInteractingTanks/bin/;%PATH%;
SET ERRORLEVEL=
CALL "%CD%/TwoConnectedTanks.exe" %*
SET RESULT=%ERRORLEVEL%

EXIT /b %RESULT%
