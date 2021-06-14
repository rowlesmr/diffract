# resume_FDT Readme

Resume, as in curriculum vitae.

## Introduction

This program reads an arbitrary number of FDT files (Thermofisher, formally Inel, X-ray diffraction data format), writing the metadata to a file for inspection. This includes, data collection time, file save time, motor positions, and temperature, for each dataset in the FDT. The data is written as it is read, resulting in no issues with regard to the file-size of the FDT file.


## How to get a copy

The Python file you see in this directory is all you need.


## How to run

If you would like to run it in the command line, you need to provide some command-line arguments:

`python resume_FDT.py *.fdt`<br />
will run through all of the FDT files in that directory.

`python resume_FDT.py data.fdt`<br />
will do just that one FDT file

The metadata is saved in a text file with the same name as the source file, with `.resume` added to the end. e.g. `data.fdt.resume`.


## Dependencies

Uses just Python. Written and tested in v3.9. May work in earlier versions.


## Supported platforms

resume_FDT is written entirely in Python (v3.9), and so should run wherever Python runs.


## Licence

resume_FDT is made available using the LGPLv3 license. The full text is [here](https://github.com/rowlesmr/diffract/blob/main/CIFtoSTR/LICENSE.LESSER)



Thanks, Matthew Rowles.<br />
matthew.rowles@curtin.edu.au
