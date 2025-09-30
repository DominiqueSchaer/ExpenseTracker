@echo off
set msg=%1
if "%msg%"=="" set msg=Update from VS Code

git add .
git commit -m "%msg%"
for /f "delims=" %%i in ('git branch --show-current') do set BRANCH=%%i
git push -u origin %BRANCH%
