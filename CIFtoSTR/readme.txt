You want to use ciftostr.pyz or ciftostr.exe, depending on your preference.

THe PyCifRW and PySimpleGUI dependencies are included in the pyz file.

If the program is run with zero command line arguments, then a GUI is launched, otherwise it is
command-line driven.


This program converts an arbitrary number of CIFs, each containing an arbitrary number of 
structures, into a number of individual STR files that are (supposed to be) compatible with TOPAS. 

Choose the files you want to convert using the 'Browse' button, then click 'Convert' to convert them.

If you would like to run it in the command line, you need to provide some command line arguments:
>python ciftostr.py *.cif or you can type the individual names of CIFs to use after the py file.  

If you would like some information on what the program does, click 'Info', or run >python ciftostr.py -info

This program requires PyCifRW. For instructions on how to install it, please see 
 https://bitbucket.org/jamesrhester/pycifrw/src/development/INSTALLATION  

Matthew Rowles. matthew.rowles@curtin.edu.au 22 Apr 21
------------------------
