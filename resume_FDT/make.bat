
set filename=resume_FDT
set dest=R:\XRDSF-ROWLEM-SE05479\Rowles\programs\
set git=C:\Users\184277j\Documents\GitHub\diffraction\resume_FDT\
set src=%~dp0


REM setup and complete the remote directory
del %dest%%filename%.py
copy %filename%.py %dest%


REM Copy the relevant files to the GitHub repository

del %git%*.py
copy *.py %git%

del %git%make.bat
copy make.bat %git%

cd %dest%

REM This makes a batch file in the destination folder
REM  so I can run it just by typing its name.
REM the %%^* prints a %* in the batch file.
REM the first % escapes the second % and the ^ escapes the *


ECHO @ECHO OFF > %filename%.bat
ECHO python %dest%%filename%.py %%^* >> %filename%.bat


cd %src%

pause