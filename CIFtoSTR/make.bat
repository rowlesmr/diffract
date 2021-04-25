
set filename=ciftostr
set dest=R:\XRDSF-ROWLEM-SE05479\Rowles\programs\
set git=C:\Users\184277j\Documents\GitHub\diffraction\CIFtoSTR\
set src=%~dp0

REM Set up the current working directory files
del %filename%.pyz


REM get the current date and time for the version number
for /f %%i in ('date /t') do set mydate=%%i
for /f %%i in ('time /t') do set mytime=%%i
echo datetime = "%mydate% %mytime%h" > citationdate.py


REM Make the python archive - zip lets you exclude locations
zip %filename%.pyz *.* -r -x make.bat testcifs* __pycache__* build* cache* %filename%.exe


REM REM create the archive
REM cd ..
REM python -m zipapp %filename% --compress
REM copy %filename%.pyz %filename%\
REM cd %filename%


REM make the exe file and clean up
pyinstaller  --onefile __main__.py --name %filename%
del %dest%%filename%.exe
del %git%%filename%.exe
del %filename%.exe
cd dist
copy %filename%.exe %git%
copy %filename%.exe %dest%
copy %filename%.exe ..
cd ..
rmdir /Q /S build
rmdir /Q /S dist
rmdir /Q /S __pycache__
del %filename%.spec




REM setup and complete the remote directory
del %dest%%filename%.pyz
copy %filename%.pyz %dest%


REM Copy the relevant files to the GitHub repository
del %git%%filename%.py
copy %filename%.py %git%

del %git%__main__.py
copy __main__.py %git%

del %git%%filename%.pyz
copy %filename%.pyz %git%



del %git%make.bat
copy make.bat %git%

cd %dest%

REM This makes a batch file in the destination folder
REM  so I can run it just by typing its name.
REM the %%^* prints a %* in the batch file.
REM the first % escapes the second % and the ^ escapes the *


ECHO @ECHO OFF > %filename%.bat
ECHO python %dest%%filename%.pyz %%^* >> %filename%.bat


cd %src%

pause