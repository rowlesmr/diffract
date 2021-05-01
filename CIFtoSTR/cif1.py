# -*- coding: utf-8 -*-
"""

SPDX-License-Identifier:  GNU Lesser General Public License v3.0 or later

Copyright © 2021 Matthew Rowles


Created on Fri Apr 23 10:57:06 2021

@author: Matthew Rowles
"""

import sys #for command line arguments
import ciftostr

HELP = \
"""
Command line arguments should be as follows:
   cif1 input_file output_file

Matthew Rowles. matthew.rowles@curtin.edu.au
https://github.com/rowlesmr/diffract/tree/main/CIFtoSTR
"""


#cifFile = "testcifs\\internet01.cif"
#strFile = "something.str"


def convert_cif_to_str(cifFile, strFile, isTopas):
    """
    Manages the call to ciftostr to write the STR file    

    Args:
        cifFile: the filename of the ciff that you want to convert
        strFile: the name of the STR file you want to write it to
        topas: Do I want to treat it as Topas running the program?
    Returns:
        None
    """
    try:
        ciftostr.write_str(cifFile, str_file = strFile, data="last", does_str_file_have_path=isTopas)
        print("--------------------")
    except Exception as e: #just print the exception and keep going
        print(e)


def main():
    """
    Defines the main method for the program to actually run.

    Returns
    -------
    None.

   
    """
    for s in sys.argv:
        print(s)
    
    if len(sys.argv) < 3: #someone probably want's help on how to use it
        print(HELP)
        sys.exit()
    
    cif_to_read = sys.argv[1]
    str_to_write = sys.argv[2]
    isTopas = False
    
    if str_to_write.endswith("cif1.tmp"): #topas gives this name to the output file.
        isTopas = True
    
    convert_cif_to_str(cif_to_read, str_to_write, isTopas) #this does the actual CIF to STR conversion


main()
