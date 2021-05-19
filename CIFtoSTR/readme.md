# ciftostr Readme


## Introduction

This program converts an arbitrary number of CIF (Crystallographic Information Format) files, each containing an arbitrary number of crystal structures, into a number of individual STR files that are compatible with the Rietveld analysis software, TOPAS. 

If the program is run with zero command line arguments, then a GUI is launched, otherwise it is command-line driven.


## How to get a copy

A Windows executable file is available [here](https://github.com/rowlesmr/diffract/blob/main/CIFtoSTR/executables/ciftostr.exe).
A Python zip application is available [here](https://github.com/rowlesmr/diffract/blob/main/CIFtoSTR/executables/ciftostr.pyz).

You will need to click on the "Download" button to get your copy.

The pure python is available [here](https://github.com/rowlesmr/diffract/tree/main/CIFtoSTR). You'll need both `ciftostr.py` and `__main__.py`


## How to run

If using the Windows executable, for all the commands below, replace "`python ciftostr.pyz`" with "`ciftostr`"

If you would like to run it in the command line, you need to provide some command-line arguments:

`python ciftostr.pyz *.cif`<br />
will run through all of the CIF files in that directory.

`python ciftostr.pyz C:\user\username\some\directory\name.cif D:\data\experiment\file.cif`<br />
`python ciftostr.pyz /nfs/an/disks/jj/home/dir/file.cif home/folder/nest/deeper/important.cif`<br />
will convert these two CIF files specifically. The resulting STR files will be saved in the same path as their parent CIF file. Relative or absolute file paths can be used.

`python ciftostr.pyz`<br />
will launch the GUI. Use the "Browse" button to select files, and "Convert" to convert them.

Bonus Windows executable behaviour: You can drag a CIF file onto the program icon, and it will convert the CIF for you. It may also work with the pyz file, depending on how your computer is set up.

`python ciftostr.pyz --help`<br />
will show some help information

`python ciftostr.pyz --info`<br />
will show some detailed information on what ciftostr is doing to the CIF data to convert to Topas STR format

`python ciftostr.pyz --licence`<br />
will show some licence information

## jEdit integration

[John Evans](http://topas.dur.ac.uk) has made available [a number of macros](http://topas.dur.ac.uk/topaswiki/doku.php?id=jedit) for the text editor [jEdit](http://www.jedit.org/) that make it integrate very well with TOPAS when operating in launch mode.

As a part of these macros, there is the ability to insert CIF files in STR format. If you wish to use `ciftostr` to generate the STR information, then you need to make the following changes:

0. Install python (or use `ciftostr.exe`)
1. Copy `ciftostr.pyz` to the TOPAS directory (e.g. C:\TOPAS6).
2. Replace your copy of `TAInsertCIF.bsh` with [this one](TAInsertCIF.bsh). (Your file is probably found in C:\Users\\?????\AppData\Roaming\jEdit\macros)
3. If you are using the Windows executable file, then you will need to change part of line 22 in the [BSH file](TAInsertCIF.bsh) from "`python ciftostr.pyz`" to "`ciftostr`"

Now, when you choose "`Insert CIFs in INP format`" from the plugin in jEdit, `ciftostr` will be used in the background to generate that format.

## Dependencies

If you are using the .py files, you need to install these dependencies. If you are using the .pyz or .exe file, they are already included.

[PyCifRW v4.4.3](https://bitbucket.org/jamesrhester/pycifrw/src/development/) (or greater) is required to parse the CIF files.<br />
[PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/) is required for the GUI. v4.39.1 was tested, but others may work.


PyCifRW can be installed in a conda environment as <br />
`conda install pycifrw -c conda-forge`<br />
or using `pip` as<br />
`pip install pycifrw`

For further PyCifRW instructions, [see here](https://bitbucket.org/jamesrhester/pycifrw/src/development/INSTALLATION).<br />
PyCIFRW is available under the [Python 2.0 license](https://bitbucket.org/jamesrhester/pycifrw/src/development/LICENSE).



PySimpleGUI can be installed as<br />
`python -m pip install PySimpleGUI`

PySimpleGUI is available under the [LGPLv3 license](https://github.com/PySimpleGUI/PySimpleGUI/blob/master/license.txt). 


## Supported platforms

ciftostr is written entirely in Python (v3.9), and so should run wherever Python runs.

ciftostr.exe was made using [Pyinstaller](https://www.pyinstaller.org/index.html), and should work on Windows


## Licence

ciftostr is made available using the LGPLv3 license. The full text is [here](https://github.com/rowlesmr/diffract/blob/main/CIFtoSTR/LICENSE.LESSER)




## What, exactly, does it do?


This program is designed to reformat data from a CIF format into the STR format suitable for use by the Rietveld analysis software, TOPAS. It doesn't carry out any validation checks to ensure the data is consistent, but simply transcribes the data as given in the CIF.
    
Where similar or identical data could be given in several places, the values are taken in a specific order of precedence, as detailed in the sections below. In general, if a value exists in an earlier place, the later places are not looked at.

This program uses the PyCifRW library, written by James Hester, to parse the CIF files into a format easily used to remix the underlying data. For the source code and other information, see https://bitbucket.org/jamesrhester/pycifrw/src/development. The GUI was created using PySimpleGUI. 
    
The STR's phase\_name is taken from '\_chemical\_name\_mineral', '\_chemical\_name\_common', '\_chemical\_name\_systematic', or '\_chemical\_name\_structure\_type', in that order, appended with the value of the 'data' block. If none of these keys are available, then the name of the 'data\_' block is used. This is also used as the filename of the STR file.
    
The unit cell parameters are taken from '\_cell\_length\_a', '\_cell\_length\_b', '\_cell\_length\_c', '\_cell\_angle\_alpha', '\_cell\_angle\_beta', and '\_cell\_angle\_gamma'. Some comparisons are made to enable some standard macros to be used (eg Cubic, Tetragonal...). In any of these fail, then all parameters are given as a fail safe.

The space\_group is taken from '\_symmetry\_space\_group\_name\_H-M', '\_space\_group\_name\_H-M\_alt', '\_symmetry\_Int\_Tables\_number', or '\_space\_group\_IT\_number', in that order. If none of these keys are available, then an empty string is written as the space group. The value of the space group is as exactly given in the CIF. No validation or editing is done.

The atomic sites are constructed as follows: The atom labels are taken from '\_atom\_site\_label', with the fractional x, y, and z coordinates given by '\_atom\_site\_fract\_x', '\_y', and '\_z'. If the decimal values of the fractional coordinates are consistent with the fractions 1/6, 1/3, 2/3, or 5/6, then the decimal value is replaced by the fractions. The site occupancy is given by '\_atom\_site\_occupancy', or by '1', if that key is not given. The atom type is given by '\_atom\_site\_type\_symbol', where available, or by the first one or two characters of the site label. If these characters match an element symbol, then that is used, otherwise, the label is used in it's entirety, and the user must decide the correct atom type to use. If the site label starts with 'Wat', (and no atom type is given) it is assumed that oxygen (from water) is correct. An attempt is also made to reorder the charge given on an atom, to ensure it is compatible with TOPAS ordering, eg Fe+2, not Fe2+.

Isotropic Atomic Displacement Parameters (ADPs; Biso), are taken from '\_atom\_site\_B\_iso\_or\_equiv', or from '\_atom\_site\_U\_iso\_or\_equiv', where they are then multiplied by 8*Pi^2 to give B values. If anisotropic ADPs are given, then '\_atom\_site\_aniso\_B\_11', '\_atom\_site\_aniso\_B\_22', and '\_atom\_site\_aniso\_B\_33' are averaged to give an equivalent Biso value. Alternatively, the equivalent U values are used to calculate Biso. As anisotropic values could be given for a subset of the atoms in the structure, the labels given by '\_atom\_site\_label' and '\_atom\_site\_aniso\_label' are matched, and if an atom doesn't have an anisotropic value, it takes its isotropic value, or is assigned a value of '1'.

The atomic site is also given a 'num\_posns 0' entry, which will update with the multiplicity of the site following a refinement. This will allow the user to compare this value with the CIF or Vol A to help ensure that the correct symmetry is being applied.

Finally, the STR is given a fixed Lorentzian crystallite size of 200 nm, and a refinable scale factor of 0.0001 to allow for an easy start to a refinement. All other values given in the STR are fixed, and require active intervention to name, refine, constrain, or restrain them.

If you have any feedback, please contact me. If you find any bugs, please provide the CIF which caused the error, a description of the error, and a description of how you believe the program should work in that instance.

Thanks, Matthew Rowles.<br />
matthew.rowles@curtin.edu.au
