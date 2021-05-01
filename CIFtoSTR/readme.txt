This program converts an arbitrary number of CIFs, each containing an arbitrary number of 
structures, into a number of individual STR files that are compatible with TOPAS.+ 

If the program is run with zero command line arguments, then a GUI is launched, otherwise it is
command-line driven.

Choose the files you want to convert using the 'Browse' button, then click 'Convert' to convert them.

If you would like to run it in the command line, you need to provide some command line arguments:
>python ciftostr.pyz *.cif

or you can type the individual names of CIFs to use after the pyz file.

For information on exactly what the program does, click 'Info', or running
>python ciftostr.pyz --info

ciftostr.py, __main__.py, ciftostr.pyz, and ciftostr.exe are made available under the 
GNU Lesser General Public License v3.0 or later.


This program is designed to reformat data from a CIF format into the STR format suitable
for use by the Rietveld analysis software, TOPAS. It doesn't carry out any validation checks
to ensure the data is consistent, but simply transcribes the data as given in the CIF.
    
Where similar or identical data could be given in several places, the values are taken in a
specific order of precedence, as detailed in the sections below. In general, if a value exists
in an earlier place, the later places are not looked at.

This program uses the PyCifRW library, written by James Hester, to parse the CIF files into
a format easily used to remix the underlying data. For the source code and other information,
see https://bitbucket.org/jamesrhester/pycifrw/src/development. The GUI was created using PySimpleGUI. 
    
The STR's phase_name is taken from '_chemical_name_mineral', '_chemical_name_common',
'_chemical_name_systematic', or '_chemical_name_structure_type', in that order, appended with
the value of the 'data' block. If none of these keys are available, then the name of the 'data_'
block is used. This is also used as the filename of the STR file.
    
The unit cell parameters are taken from '_cell_length_a', '_cell_length_b', '_cell_length_c', 
'_cell_angle_alpha', '_cell_angle_beta', and '_cell_angle_gamma'. Some comparisons are made to
enable some standard macros to be used (eg Cubic, Tetragonal...). In any of these fail, then all
parameters are given as a fail safe.

The space_group is taken from '_symmetry_space_group_name_H-M', '_space_group_name_H-M_alt', 
'_symmetry_Int_Tables_number', or '_space_group_IT_number', in that order. If none of these keys
are available, then an empty string is written as the space group. The value of the space group is 
as exactly given in the CIF. No validation or editing is done.

The atomic sites are constructed as follows: The atom labels are taken from '_atom_site_label', 
with the fractional x, y, and z coordinates given by '_atom_site_fract_x', '_y', and '_z'. 
If the decimal values of the fractional coordinates are consistent with the fractions 1/6, 1/3, 2/3,
or 5/6, then the decimal value is replaced by the fractions.
The site occupancy is given by '_atom_site_occupancy', or by '1', if that key is not given.
The atom type is given by '_atom_site_type_symbol', where available, or by the first one or two
characters of the site label. If these characters match an element symbol, then that is used, 
otherwise, the label is used in it's entirety, and the user must decide the correct atom type to use.
An attempt is also made to reorder the charge given on an atom, to ensure it is compatible with
TOPAS ordering, eg Fe+2, not Fe2+.

Isotropic Atomic Displacement Parameters (ADPs; Biso), are taken from '_atom_site_B_iso_or_equiv', or
from '_atom_site_U_iso_or_equiv', where they are then multiplied by 8*Pi^2 to give B values.
If anisotropic ADPs are given, then '_atom_site_aniso_B_11', '_atom_site_aniso_B_22', and
'_atom_site_aniso_B_33' are averaged to give an equivalent Biso value. Alternatively, the equivalent
U values are used to calculate Biso. As anisotropic values could be given for a subset of the atoms
in the structure, the labels given by '_atom_site_label' and '_atom_site_aniso_label' are matched, 
and if an atom doesn't have an anisotropic value, it takes its isotropic value, or is assigned a
value of '1'.

The atomic site is also given a 'num_posns 0' entry, which will update with the multiplicity of the
site following a refinement. This will allow the user to compare this value with the CIF or Vol A
to help ensure that the correct symmetry is being applied.

Finally, the STR is given a fixed Lorentzian crystallite size of 200 nm, and a refinable scale factor
of 0.0001 to allow for an easy start to a refinement. All other values given in the STR are fixed,
and require active intervention to name, refine, constrain, or restrain them.

If you have any feedback, please contact me. If you find any bugs, please provide the CIF which 
caused the error, a description of the error, and a description of how you believe the program
should work in that instance.

Thanks, Matthew Rowles.
matthew.rowles@curtin.edu.au