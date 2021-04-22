@ECHO OFF 
call conda activate base
python C:\Users\184277j\Documents\GitHub\diffraction\CIFtoSTR\cifreader.py %*
call conda deactivate



