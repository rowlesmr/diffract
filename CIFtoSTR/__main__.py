# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 10:57:06 2021

@author: Matthew Rowles
"""

from glob import glob #for command line arguments
import sys #for command line arguments
import PySimpleGUI as sg #for gui
import ciftostr
import citationdate


CITATION = "\nMatthew R. Rowles, CIFtoSTR, https://github.com/rowlesmr/diffract/tree/main/CIFtoSTR, "+\
           "version date: " + citationdate.datetime + "\n"


HELP = \
"\nThis program converts an arbitrary number of CIFs, each containing an arbitrary number of \n"+\
"structures, into a number of individual STR files that are (supposed to be) compatible with TOPAS.\n\n"+ \
\
"Choose the files you want to convert using the 'Browse' button, then click 'Convert' to convert them.\n\n"+\
\
"If you would like to run it in the command line, you need to provide some command line arguments:\n"+\
">python ciftostr.pyz *.cif\nor you can type the individual names of CIFs to use after the pyz file.\n\n" + \
\
"For information on exactly what the program does, click 'Info', or run >python ciftostr.pyz -info\n\n"+\
\
"Matthew Rowles. matthew.rowles@curtin.edu.au\n\n"+\
\
"For citation: "+ CITATION + \
"------------------------\n"




INFO = \
"This program is designed to reformat data from a CIF format into the STR format suitable\n"+\
"for use by the Rietveld analysis software, TOPAS. It doesn't carry out any validation checks\n"+\
"to ensure the data is consistent, but simply transcribes the data as given in the CIF.\n\n"+\
    \
"Where similar or identical data could be given in several places, the values are taken in a\n"+\
"specific order of precedence, as detailed in the sections below. In general, if a value exists\n"+\
"in an earlier place, the later places are not looked at.\n\n"+\
\
"This program uses the PyCifRW library, written by James Hester, to parse the CIF files into\n"+\
"a format easily used to remix the underlying data. For the source code and other information,\n"+\
"see https://bitbucket.org/jamesrhester/pycifrw/src/development\n\n" + \
    \
"The STR's phase_name is taken from '_chemical_name_mineral', '_chemical_name_common',\n"+\
"'_chemical_name_systematic', or '_chemical_name_structure_type', in that order, appended with\n"+\
"the value of the 'data' block. If none of these keys are available, then the name of the 'data_'\n"+\
"block is used. This is also used as the filename of the STR file.\n\n"+\
    \
"The unit cell parameters are taken from '_cell_length_a', '_cell_length_b', '_cell_length_c', \n"+\
"'_cell_angle_alpha', '_cell_angle_beta', and '_cell_angle_gamma'. Some comparisons are made to\n"+\
"enable some standard macros to be used (eg Cubic, Tetragonal...). In any of these fail, then all\n"+\
"parameters are given as a fail safe.\n\n"+\
\
"The space_group is taken from '_symmetry_space_group_name_H-M', '_space_group_name_H-M_alt', \n"+\
"'_symmetry_Int_Tables_number', or '_space_group_IT_number', in that order. If none of these keys\n"+\
"are available, then an empty string is written as the space group. The value of the space group is \n"+\
"as exactly given in the CIF. No validation or editing is done.\n\n"+\
\
"The atomic sites are constructed as follows: The atom labels are taken from '_atom_site_label', \n"+\
"with the fractional x, y, and z coordinates given by '_atom_site_fract_x', '_y', and '_z'. \n"+\
"If the decimal values of the fractional coordinates are consistent with the fractions 1/6, 1/3, 2/3,\n"+\
"or 5/6, then the decimal value is replaced by the fractions.\n"+\
"The site occupancy is given by '_atom_site_occupancy', or by '1', if that key is not given.\n"+\
"The atom type is given by '_atom_site_type_symbol', where available, or by the first one or two\n"+\
"characters of the site label. If these characters match an element symbol, then that is used, \n"+\
"otherwise, the label is used in it's entirety, and the user must decide the correct atom type to use.\n"+\
"An attempt is also made to reorder the charge given on an atom, to ensure it is compatible with\n"+\
"TOPAS ordering, ie Fe+2, not Fe2+.\n\n"+\
\
"Isotropic Atomic Displacement Parameters (ADPs; Biso), are taken from '_atom_site_B_iso_or_equiv', or\n"+\
"from '_atom_site_U_iso_or_equiv', where they are then multiplied by 8*Pi^2 to give B values.\n"+\
"If anisotropic ADPs are given, then '_atom_site_aniso_B_11', '_atom_site_aniso_B_22', and\n"+\
"'_atom_site_aniso_B_33' are averaged to give an equivalent Biso value. Alternatively, the equivalent\n"+\
"U values are used to calculate Biso. As anisotropic values could be given for a subset of the atoms\n"+\
"in the structure, the labels given by '_atom_site_label' and '_atom_site_aniso_label' are matched, \n"+\
"and if an atom doesn't have an anisotropic value, it takes its isotropic value, or is assigned a\n"+\
"value of '1'.\n\n"+\
\
"The atomic site is also given a 'num_posns 0' entry, which will update with the multiplicity of the\n"+\
"site following a refinement. This will allow the user to compare this value with the CIF or Vol A\n"+\
"to help ensure that the correct symmetry is being applied.\n\n"+\
\
"Finally, the STR is given a fixed Lorentzian crystallite size of 200 nm, and a refinable scale factor\n"+\
"of 0.0001 to allow for an easy start to a refinement. All other values given in the STR are fixed,\n"+\
"and require active intervention to name, refine, constrain, or restrain them.\n\n"+\
\
"If you have any feedback, please contact me. If you find any bugs, please provide the CIF which \n"+\
"caused the error, a description of the error, and a description of how you believe the program\n"+\
"should work in that instance.\n\n"+\
\
"Thanks, Matthew Rowles.\n"+\
"matthew.rowles@curtin.edu.au\n\n"+\
    \
"For citation: "+ CITATION +\
"\n------------------------\n"



def gui():
    """
    Defines the GUI elements.

    Returns
    -------
    None.

    """
    #https://stackoverflow.com/questions/55573754/load-multiple-file-with-pysimplegui
    #https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Script_Launcher_Realtime_Output.py
    layout = [
              [sg.Multiline(size=(90,20),
                            background_color='black',
                            text_color='white',
                            reroute_stdout=True,
                            reroute_stderr=True,
                            autoscroll = True)],

              [sg.Input(key='_FILES_'),
               sg.FilesBrowse(file_types=(("CIFs", "*.cif"),("All files", "*.*"),))],

              [sg.Button('Convert'), sg.Button('Exit'), sg.Button('Info')]
             ]

    window = sg.Window("CIFtoSTR", layout, finalize=True)

    #initial help text every time you open the program.
    print(HELP)

    while True:             # Event Loop
        event, values = window.read() #window.read() is a tuple
        filenames = values['_FILES_'].split(';') # list of filenames
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Convert':          
            convertCifs(filenames) #this does the actual CIF to STR conversion
        elif event == 'Info':
            print(INFO)

    window.close()




def main():
    """
    Defines the main method for the program to actually run.

    Returns
    -------
    None.

   
    """
    if len(sys.argv) <= 1: #Assume the user wants the gui
        print(HELP) #just in case there are commandline people wanting to know.
        gui()
        sys.exit()

    if "-info" in sys.argv:
        print(INFO)
        sys.exit()

    filenames = []
    for i in range(1,len(sys.argv)):
        filenames += glob(sys.argv[i])

    convertCifs(filenames) #this does the actual CIF to STR conversion




def convertCifs(filenames):
    """
    Helper function to keep the creation of STRs consistent between the commandline and GUI versions

    Args:
        filenames: a list of filenames as strings
    Returns:
        None
    """
    for file in filenames:
        try:
            ciftostr.writeSTR(file)
            print("--------------------")
        except Exception as e: #just print the exception and keep going
            print(e)
    print("All done.")



main()

print("Thanks for using CIFtoSTR. If you liked this, please cite " + CITATION)
