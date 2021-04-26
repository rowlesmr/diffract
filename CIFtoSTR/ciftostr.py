# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 17:10:25 2021

@author: Matthew Rowles
"""

import math
import re #regular expression
import os #ntpath #to separate path and filename
import copy
#https://pypi.org/project/PyCifRW/4.4/  https://bitbucket.org/jamesrhester/pycifrw/downloads/
import CifFile as cf

#cif = cf.ReadCif("testcifs\\1000073.cif")
#data = cif.keys()[0]



def writeSTR(ciffile):
    """
    Writes all structures in a given CIF to file from a give cif file..

    Args:
        ciffile: path to a CIF file as a string
    Returns:
        None. Writes file to disk.
     """
    print("Reading " + ciffile + ".")
    cif = cf.ReadCif(ciffile)
    datakeys = cif.keys()

    path = os.path.dirname(ciffile)

    for data in datakeys:
        s = createSTR(cif, data)
        f = os.path.join(path, cleanFileName(getPhaseName(cif, data)) + '.str')

        str_file = open(f, "w")
        print("Now writing " + str_file.name + ".")
        str_file.write(s)
        str_file.close()

    print("Done.")


def createSTR(cif, data):
    """
    Creates a single string formatted as a STR representing the give data block in the cif.

    Args:
        cif: PyCifRW representation of a cif file
        data: the key of the data block to convert to a STR
    Returns:
        A single string formatted as a TOPAS STR.
     """
    s  = "str\n"
    s += '\tphase_name "' + getPhaseName(cif, data) + '"\n'
    s += "\tscale @ 0.0001\n\tCS_L(,200)\n"
    s += getUnitCell(cif, data) + "\n"
    s += '\tspace_group "' + getSpaceGroup(cif, data) + '"\n'
    s += getAtoms(cif, data)

    return s


def stripBrackets(l):
    """
    Strips the brackets at the end of a string.
    The main use case is to remove the error values, eg '0.123(45)' --> '0.123'.

    Args:
        l: A list of strings, or a single string.
    Returns:
        A list of strings, or a single string, with no brackets at the end of each string
     """
     
    l = l[:] # get a copy 
    changeMe = False
    if isinstance(l, str): #if it's a single string, make it a list
        l = [l]
        changeMe = True

    for i in range(len(l)):
        s = l[i]

        try:
            bracket = s.index("(")
        except ValueError: #if there isn't a bracket, just keep going.
            bracket = len(s)

        l[i]=s[0:bracket]

    if changeMe: #if it was a list, change it back
        l = l[0]

    return l


def changeNAValue(l):
    """
    If a string consists of a single question mark ('?') or full stop ('.'),
    it is replaced with a None
    These are normally markers of "no value recorded"

    Args:
        l: A list of strings, or a single string.
    Returns:
        A list of strings, or a single string, with None in place of a single question
        mark or full stop
     """

    changeMe = False
    l = l[:] # take a copy
    if isinstance(l, str): #if it's a single string, make it a list
        l = [l]
        changeMe = True

    for i in range(len(l)):
        s = l[i]

        if s in ("?", "."):
            l[i] = None

    if changeMe: #if t was a list, change it back
        l = l[0]

    return l


def concat(*ss, sep="_"):
    """
    Concatenate an aribtrary number of strings using the given separator.

    Args:
        *ss: An arbitrary number of strings
        sep: A string used to separate each string. Defaults to "_"
    Returns:
        A single string consisting of the given strings separated by the separator
     """
    r = ""
    for s in ss:
        r += s + sep
    r = r[0:len(r)-len(sep)] #get rid of final separator
    return r



def valToFrac(l):
    """
    Checks a list (or single) strings consisting of numeric values for
    values which are consistent with fractional values.

    If those values are consistent with 1/6, 1/3, 2/3, or 5/6, then the decimal
    representation is altered to be a fractional representation.

    TOPAS requires atoms on special positions with values that have non-terminating
    decimal representations to have be represented as fractions.

    Args:
        l: A list of strings, or a single string represent numerical values.
    Returns:
        A list of strings, or a single string, with fractions representing 1/6, 1/3, 2/3, or 5/6
    """
    oneSixth = ("0.1666","0.16666","0.166666","0.1666666",\
                "0.1667","0.16667","0.166667","0.1666667")
    oneThird = ("0.3333","0.33333","0.333333","0.3333333")
    twoThird = ("0.6666","0.66666","0.666666","0.6666666",\
                "0.6667","0.66667","0.666667","0.6666667")
    fiveSixth= ("0.8333","0.83333","0.833333","0.8333333")

    oneSixthFrac = "=1/6;"
    oneThirdFrac = "=1/3;"
    twoThirdFrac = "=2/3;"
    fiveSixthFrac= "=5/6;"



    l = l[:] #get a copy
    fractionDetected = False
    changeMe = False
    if isinstance(l, str): #if it's a single string, make it a list
        l = [l]
        changeMe = True

    for i in range(len(l)):
        fractionDetected = False
        if l[i] in oneSixth:
            fractionDetected = True
            l[i] = oneSixthFrac
        elif l[i] in oneThird:
            fractionDetected = True
            l[i] = oneThirdFrac
        elif l[i] in twoThird:
            fractionDetected = True
            l[i] = twoThirdFrac
        elif l[i] in fiveSixth:
            fractionDetected = True
            l[i] = fiveSixthFrac
        else:
            pass #l[i] is all good


        if fractionDetected:
            print("Fractional atomic coordinate detected and replaced.")

    if changeMe: #if it was a list, change it back
        l = l[0]

    return l


def getDictEntryCopy(dct, *keys, default=None):
    """
    Returns a deepcopy of the first dictionary value to match from an arbitrary number of given keys.
    If there is no match, the default value is returned.
    #https://stackoverflow.com/a/67187811/36061


    Args:
        dct: A dictionary
        *keys: an arbitrary number of keys in order of preference for return.
        default: The value to return if no matching entry is found in the dictionary.
    Returns:
        A deepcopy of the dictionary value associated with the first key to match, or the default value.
     """
    for key in keys:
        try:
            return copy.deepcopy(dct[key])
        except KeyError:
            pass
    return default


def padStringList(l):
    """
    Given a list of atomic ordinates, labels, or the like, pad the length of the strings 
    such that they are all the same

    Parameters
    ----------
    l : list of strings
    
    Returns
    -------
    List of strings, all of the same length

    """
    # if any strings start with '-', it's probably a negative number, and I need to prepend 
    #  a space to those that don't start with a '-'.
    negativeString = False
    l=l[:] #don't alter the original
    for s in l:
        if s.startswith("-"):
            negativeString =True
            
    
    if negativeString: #Prepend the string
        for i in range(len(l)):
            if not l[i].startswith("-"):
                l[i] = " "+l[i]
                
    #what is the max str len?
    maxLen = 0          
    for s in l:
        if len(s) > maxLen:
            maxLen = len(s)
    
    for i in range(len(l)):
        l[i] = postPadString(l[i], maxLen)
 
    return l
                
        
        
def postPadString(s, d):
    """
    Add spaces to the end of a string until it is the length given by d
    If len is already more than d, it just returns s

    Parameters
    ----------
    s : string you want to pad at the end with spaces
    d : Integer that you want the final string length to be

    Returns
    -------
    s : String of length d. If len(s) < d originalyy, then s is returned unchanged.

    """
    while len(s) < d:
        s += " "
    return s
        
    
def cleanPhaseName(s):
    """
    Removes new lines, carriage returns, and leading/trailing whitespace from a 
    string representing a phase name

    Args:
        s: a string

    Returns:
        A string with no newlines, carriage returns, or leading/trailing whitespace
     """
    return s.strip().replace('\n', '').replace('\r', '')


def cleanFileName(s):
    """
    Replaces illegal characters from a string which is to be used as a filename. 
    This doesn't deal with the path, just the name. Also, not the extension.
    
    eg 'string' could be used to construct 'C:\important\string.cif' at a later point in the program.
    
    / \ | : * ? " < >  are replaced by "_"
    
    Whitespace is also replaced by "_"
    
    Also checks for illegal names like 'CON', and 'PRN'.
    
    Yes, the is Windows-centric, but so is TOPAS.
    
    Trying to follow guidelines in:
    https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file#naming-conventions

    Args:
        s: a string

    Returns:
        A string with no illegal characters
     """    
    illegalNames = ( "CON",  "PRN",  "AUX",  "NUL", "COM1", "COM2", "COM3", "COM4", 
                    "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", 
                    "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",    ".",   "..")     

    if s.upper() in illegalNames:
        s = s + "_"
        
    if s.endswith("."):
        s[:-1] + "_"

    return re.sub("[\\\\/:*?\"<>|\s]", "_", s)




def getPhaseName(cif, data):
    """
    Returns a string to be used as the name of the phase.

    The name is taken from (in order of preference):
        "_chemical_name_mineral", "_chemical_name_common",
        "_chemical_name_systematic", or "_chemical_name_structure_type"
    The value of the data block is then appended to this value.

    Args:
        cif: a PyCifRW dictionary
        data: the key value for a data block in the CIF
    Returns:
        A string denoting the name of the phase
     """
    phasename = getDictEntryCopy(cif[data], "_chemical_name_mineral",
                                            "_chemical_name_common",
                                            "_chemical_name_systematic",
                                            "_chemical_name_structure_type",
                                            default = "")
    phasename = cleanPhaseName(phasename)

    r = ""
    #check that all the types of non-name names are accounted for.
    if phasename in ("", ".", "?", None):
        r = data
    else:
        r = concat(phasename, data)

    return r

def getSpaceGroup(cif, data):
    """
    Returns a string to be used as the spacegroup.

    The space group  is taken from (in order of preference):
        "_symmetry_space_group_name_H-M", "_symmetry_Int_Tables_number",
        "_space_group_name_H-M_alt", or "_space_group_IT_number",

    No validation is done on the space group.

    Args:
        cif: a PyCifRW dictionary
        data: the key value for a data block in the CIF
    Returns:
        A string denoting the space group of the phase, as given in the CIF.
     """
    spacegroup = getDictEntryCopy(cif[data], "_symmetry_space_group_name_H-M",
                                             "_symmetry_Int_Tables_number",
                                             "_space_group_name_H-M_alt",
                                             "_space_group_IT_number",
                                             default = "")

    return spacegroup


def getUnitCell(cif, data):
    """
    Returns a string giving the unit cell parameters of the structure.
    Some pattern matching is carried out to return TOPAS macros for
    unit cell prms, but no validation or space group consistency is done.

    see also getUnitCell2() - it makes no attempt to pattern-match


    Args:
        cif: a PyCifRW dictionary
        data: the key value for a data block in the CIF
    Returns:
        A string containing the unit cell parameters in STR format.
    Raises:
        KeyError: if any of the unit cell parameters are not present in the datablock.
    """

    a_s  = stripBrackets(getDictEntryCopy(cif[data],"_cell_length_a"))
    b_s  = stripBrackets(getDictEntryCopy(cif[data],"_cell_length_b"))
    c_s  = stripBrackets(getDictEntryCopy(cif[data],"_cell_length_c"))
    al_s = stripBrackets(getDictEntryCopy(cif[data],"_cell_length_alpha"))
    be_s = stripBrackets(getDictEntryCopy(cif[data],"_cell_length_beta"))
    ga_s = stripBrackets(getDictEntryCopy(cif[data],"_cell_length_gamma"))

    a  = float(a_s)
    b  = float(b_s)
    c  = float(c_s)
    al = float(al_s)
    be = float(be_s)
    ga = float(ga_s)

    s = ""
    if a == b and b == c: #cubic or rhombohedral
        if al == be and be == ga and al == float("90"): #cubic
            s = concat("\tCubic(",a_s,")", sep="")
        if al == be and be == ga and al != float("90"): #rhombohedral
            s = concat("\tRhombohedral(",a_s,", ", al_s,")", sep="")

    elif a == b and b != c: #tetragonal or hexagonal/trigonal
        if al == be and be == ga and al == float("90"): #tetragonal
            s = concat("\tTetragonal(",a_s,", ", c_s, ")", sep="")
        if al == be and al == float("90") and ga == float("120"): #hexagonal or trigonal
            s = concat("\tHexagonal(",a_s,", ", c_s, ")", sep="")

    elif a != b and a != c and b != c: #ortho, mono, tric
        if al == be and be == ga and al == float("90"): #ortho
            s = concat("\ta",a_s,"\n\tb",b_s,"\n\tc",c_s, sep=" ")
        if al != be and al != ga and be != ga: #tric
            s = concat("\ta ",a_s,"\n\tb ",b_s,"\n\tc ",c_s,"\n\tal",al_s,"\n\tbe",be_s,"\n\tga",ga_s, sep=" ")
        if al == be and al != ga and al == float("90"): #mono_1
            s = concat("\ta ",a_s,"\n\tb ",b_s,"\n\tc ",c_s,"\n\tga",ga_s, sep=" ")
        if al == ga and al != be and al == float("90"): #mono_2
            s = concat("\ta ",a_s,"\n\tb ",b_s,"\n\tc ",c_s,"\n\tbe",be_s, sep=" ")
        if be == ga and be != al and be == float("90"): #mono_3
            s = concat("\ta ",a_s,"\n\tb ",b_s,"\n\tc ",c_s,"\n\tal",al_s, sep=" ")

    #to catch everything else
    else:
        s = concat("\ta ",a_s,"\n\tb ",b_s,"\n\tc ",c_s,
                   "\n\tal",al_s,"\n\tbe",be_s,"\n\tga",ga_s, sep=" ")

    return s

def getUnitCell2(cif, data):
    """
    Returns a string giving the unit cell parameters of the structure.
    see also getUnitCell()

    Args:
        cif: a PyCifRW dictionary
        data: the key value for a data block in the CIF
    Returns:
        A string containing the unit cell parameters in STR format.
    Raises:
        KeyError: if any of the unit cell parameters are not present in the datablock.
    """
    a  = stripBrackets(getDictEntryCopy(cif[data],"_cell_length_a"))
    b  = stripBrackets(getDictEntryCopy(cif[data],"_cell_length_b"))
    c  = stripBrackets(getDictEntryCopy(cif[data],"_cell_length_c"))
    al = stripBrackets(getDictEntryCopy(cif[data],"_cell_length_alpha"))
    be = stripBrackets(getDictEntryCopy(cif[data],"_cell_length_beta"))
    ga = stripBrackets(getDictEntryCopy(cif[data],"_cell_length_gamma"))

    return concat("\ta",a,"b",b,"c",c,"\n\tal",al,"be",be,"ga",ga, sep=" ")


def getAtoms(cif, data):
    """
    Returns a string giving the site parameters for all of the sites in the CIF.

    They are formatted as necessary for TOPAS. A single site consists of:
        "site _1_ num_posns 0 x _2_ y _3_ z _4_ occ _5_ _6_ beq _7_"

    1 - the site label is taken directly from "_atom_site_label"
    2 - the fractional x ordinate is taken from "_atom_site_fract_x"
    3 - the fractional y ordinate is taken from "_atom_site_fract_y"
    4 - the fractional z ordinate is taken from "_atom_site_fract_z"
    5 - the atom type is taken from "_atom_site_type_symbol" or inferred from the site label
    6 - the occupancy is taken from "_atom_site_occupancy" or given the value "1"
    7 - the isotropic displacement parameter,B, is taken from "_atom_site_B_iso_or_equiv"
        or 8*Pi^2*"_atom_site_U_iso_or_equiv". If anisotropic values are present as
        "_atom_site_aniso_B_11", "_22", "_33", then their average is used. If
        "_atom_site_aniso_U_11", "_22", "_33", then 8*Pi^2 times their average is used. If
        no values are present the the value "1" is assigned.

    If the decimal values of the fractional coordinates are consistent with the fractions
    1/6, 1/3, 2/3, or 5/6, then the decimal value is replaced by the fractional representation.


    Args:
        cif: a PyCifRW dictionary
        data: the key value for a data block in the CIF
    Returns:
        A string containing the atomic site parameters in STR format.
    Raises:
        KeyError: if any of the site label or fractional coordinate keys are not present.
    """
    labels = padStringList(getDictEntryCopy(cif[data],"_atom_site_label"))
    
    # to valToFrac first, as a real match wouldn't have any errors to strip
    x = padStringList(stripBrackets(valToFrac(getDictEntryCopy(cif[data],"_atom_site_fract_x"))))
    y = padStringList(stripBrackets(valToFrac(getDictEntryCopy(cif[data],"_atom_site_fract_y"))))
    z = padStringList(stripBrackets(valToFrac(getDictEntryCopy(cif[data],"_atom_site_fract_z"))))

    #type of atom
    try:
        atoms = getDictEntryCopy(cif[data],"_atom_site_type_symbol")
        atoms = [fixAtomSiteType(i) for i in atoms]

    except KeyError:
        print("Warning! Atom types inferred from site labels. Please check for correctness.")
        atoms = []
        for l in labels:
            atoms += [isThisAnAtom(l)]
    atoms = padStringList(atoms)

    #occupancy
    try:
        occ = stripBrackets(getDictEntryCopy(cif[data],"_atom_site_occupancy"))
    except KeyError:
        occ = ["1"] * len(labels)
    occ = padStringList(occ)

    #ADPs
    Biso = padStringList(getBeq(cif, data))

    r = ""
    for i in range(len(labels)):
        r += makeSiteString(labels[i],x[i],y[i],z[i],atoms[i],occ[i],Biso[i])

    return r


def makeSiteString(label, x, y, z, atom, occ, beq):
    """
    Returns a string giving the site parameters necessary for TOPAS:
        "site _1_ num_posns 0 x _2_ y _3_ z _4_ occ _5_ _6_ beq _7_"

    This is used by getAtoms().

    Args:
        label: a string to describe the site (1)
        x: the fractional x ordinate (2)
        y: the fraction y ordinate (3)
        z: the fractional z ordinate (4)
        atom: the scattering factors to use for this site (5)
        occ: the statistical occupancy of this site (6)
        beq: the isotropic atomic displacement factor for this site (B) (7)

    Returns:
        A string containing the atomic site parameters in STR format.
    """
    return concat("\tsite",label,"num_posns 0\tx", x, "y", y, "z", z,
                  "occ", atom, occ, "beq", beq, "\n", sep = " ")


def isThisAnAtom(s):
    """
    Given a site label string, the first 2 or 1 characters are checked
    (case-sensitive) to see if they match an element symbols. If they do,
    this symbol is returned. If not, the entire site label is returned.

    Args:
        s: a string to denoting the site label

    Returns:
        A string containing the element symbol, or the entire label.
    """
    elements = ("Ac","Ag","Al","Am","Ar","As","At","Au","Ba", "B",\
                "Be","Bi","Br","Ca","Cd", "C","Ce","Cl","Co","Cr",\
                "Cs","Cu","Dy","Er","Eu", "F","Fe","Fr","Ga","Gd",\
                "Ge", "H","He","Hg","Hf","Ho", "I","In","Ir", "K",\
                "Kr","La","Li","Lu","Mg","Mn","Mo", "N","Na","Nb",\
                "Nd","Ne","Ni", "O","Os","Pb", "P","Pa","Pd","Po",\
                "Pr","Pm","Pt","Ra","Rb","Re","Rh","Rn","Ru", "S",\
                "Sb","Sc","Sm","Se","Si","Sn","Sr","Ta","Tb","Tc",\
                "Te","Th","Tl","Ti","Tm", "W", "U", "V","Xe", "Y",\
                "Yb","Zn","Zr","Np","Pu","Am","Cm","Bk","Cf", "D")



    r = s[0:2] #take the first two characters
    if r in elements:
        return r

    r = s[0:1] #take the first character
    if r in elements:
        return r

    return s #if everything fails, just return what the label was


def fixAtomSiteType(a):
    """
    Given an atom type from "_atom_site_type_symbol", any charge given is sometimes the wrong
    way around for TOPAS to handle. This function uses a regex to switch and given charge
    to the correct format, whilst leaving neutral atoms as they were.

    For example
    Cu   --> Cu
     I   -->  I
     K+  -->  K+1
     V3+ -->  V+3
    Fe2+ --> Fe+2
     O1- -->  O-1

    Furthermore, the charge is checked against the list of scattering factors supported
    by TOPAS, and if a mismatch is detected, a charged atom is replaced by the neutral one.
    eg: H+1 --> H

    Args:
        s: a string to denoting the atom type, with or without a charge

    Returns:
        A string containing the atom type with the charge in the correct order, if one is given.
    """

    regex = re.search("([A-Za-z]{1,2})(\d{0,2})([+-]{0,1})(\d{0,2})", a)

    symbol = regex.group(1)
    charge = regex.group(2)
    sign = regex.group(3)
    digit = regex.group(4) #if there is a trailing digit, then that is probably the charge


    if symbol == "W":
        print("W detected. Do you mean tungsten or oxygen from a water molecule?")


    if charge == "0": #ie Si0+ is a valid symbol, but it is a neutral atom
        charge = ""
        sign = ""

    #check for a single sign with no charge. eg F-. Needs to return F-1
    if len(sign) == 1 and len(charge) == 0:
        if len(digit) == 0:
            charge = "1"
        else: #the atom was probably the right way around to begin with
            return a

    return allowedAtomTypes(symbol+sign+charge)



def allowedAtomTypes(a):
    """
    Given an atom type in the correct TOPAS site format, the CIF dictionary can allow charges
    for which there are no scattering factors..

    The charge is checked against the list of scattering factors supported by TOPAS, and if
    a mismatch is detected, a charged atom is replaced by the neutral one.
    eg: H+1 --> H

    Args:
        s: a string to denoting the atom type, with or without a charge

    Returns:
        A string containing the atom type with the charge in the correct order, if one is given.
    """
    allowed = ("D", "H", "H-1", "D-1", "He", "Li", "Li+1", "Be", "Be+2", "B", "C", "N",
               "O", "O-1", "O-2", "F", "F-1", "Ne", "Na", "Na+1", "Mg", "Mg+2", "Al",
               "Al+3", "Si", "Si+4", "P", "S", "Cl", "Cl-1", "Ar", "K", "K+1", "Ca",
               "Ca+2", "Sc", "Sc+3", "Ti", "Ti+2", "Ti+3", "Ti+4", "V", "V+2", "V+3",
               "V+5", "Cr", "Cr+2", "Cr+3", "Mn", "Mn+2", "Mn+3", "Mn+4", "Fe", "Fe+2",
               "Fe+3", "Co", "Co+2", "Co+3", "Ni", "Ni+2", "Ni+3", "Cu", "Cu+1", "Cu+2",
               "Zn", "Zn+2", "Ga", "Ga+3", "Ge", "Ge+4", "As", "Se", "Br", "Br-1", "Kr",
               "Rb", "Rb+1", "Sr", "Sr+2", "Y", "Y+3", "Zr", "Zr+4", "Nb", "Nb+3", "Nb+5",
               "Mo", "Mo+3", "Mo+5", "Mo+6", "Tc", "Ru", "Ru+3", "Ru+4", "Rh", "Rh+3",
               "Rh+4", "Pd", "Pd+2", "Pd+4", "Ag", "Ag+1", "Ag+2", "Cd", "Cd+2", "In",
               "In+3", "Sn", "Sn+2", "Sn+4", "Sb", "Sb+3", "Sb+5", "Te", "I", "I-1", "Xe",
               "Cs", "Cs+1", "Ba", "Ba+2", "La", "La+3", "Ce", "Ce+3", "Ce+4", "Pr", "Pr+3",
               "Pr+4", "Nd", "Nd+3", "Pm", "Pm+3", "Sm", "Sm+3", "Eu", "Eu+2", "Eu+3", "Gd",
               "Gd+3", "Tb", "Tb+3", "Dy", "Dy+3", "Ho", "Ho+3", "Er", "Er+3", "Tm", "Tm+3",
               "Yb", "Yb+2", "Yb+3", "Lu", "Lu+3", "Hf", "Hf+4", "Ta", "Ta+5", "W", "W+6",
               "Re", "Os", "Os+4", "Ir", "Ir+3", "Ir+4", "Pt", "Pt+2", "Pt+4", "Au", "Au+1",
               "Au+3", "Hg", "Hg+1", "Hg+2", "Tl", "Tl+1", "Tl+3", "Pb", "Pb+2", "Pb+4",
               "Bi", "Bi+3", "Bi+5", "Po", "At", "Rn", "Fr", "Ra", "Ra+2", "Ac", "Ac+3",
               "Th", "Th+4", "Pa", "U", "U+3", "U+4", "U+6", "Np", "Np+3", "Np+4", "Np+6",
               "Pu", "Pu+3", "Pu+4", "Pu+6", "Am", "Cm", "Bk", "Cf")

    if a in allowed:
        return a


    #if we get here, the atom doesn't exist in the tuple.
    regex = re.search("([A-Za-z]{1,2})([+-]{0,1})(\d{0,2})", a) #Cu+2
    symbol = regex.group(1)

    print(a + " is not a legal TOPAS scattering factor. Atom replaced with " + symbol + ".")

    return symbol




def getBeq(cif, data):
    """
    Returns a list of strings giving the isotropic atomic displacement parameters, B, of
    all atomic sites.

    They values are taken from "_atom_site_aniso_U_11", "_22", "_33" or
    "_atom_site_aniso_B_11", "_22", "_33", or "_atom_site_U_iso_or_equiv", or
    "_atom_site_B_iso_or_equiv".

    If no values are present, then a value of "1" is assigned.

    Args:
        cif: a PyCifRW dictionary
        data: the key value for a data block in the CIF
    Returns:
        A list containing the isotropic atomic displacement parameters, B, of
    all atomic sites.
    """
    goToEnd = False
    r = []
    try:
        r = getAnisoAsIso(cif,data)
        goToEnd = True
    except KeyError:
        pass

    if not goToEnd:
        try:
            r = getUiso(cif, data)
            goToEnd = True
        except KeyError:
            pass

    if not goToEnd:
        try:
            r = getBiso(cif,data)
            goToEnd = True
        except KeyError:
            pass

    #if we get here, there were no B values in the CIF. Booo!
    if not goToEnd:
        r = [None]*len(getDictEntryCopy(cif[data],"_atom_site_label"))


    for i in range(len(r)):
        if r[i] is None:
            print("Warning! Biso value missing! Default value of 1 entered")
            r[i] = "1."


    #do the final check for negative values
    for s in r:
        if s.startswith("-"):
            print("Warning! Negative atomic displacement parameter detected!")

    return r


def getBiso(cif, data):
    """
    Returns a list of strings giving the isotropic atomic displacement parameters, B, of
    all atomic sites taken from "_atom_site_B_iso_or_equiv".

    Used by getBeq().

    Args:
        cif: a PyCifRW dictionary
        data: the key value for a data block in the CIF
    Returns:
        A list containing the isotropic atomic displacement parameters, B, of all atomic sites.
    Raises:
        KeyError: if the key "_atom_site_B_iso_or_equiv" is not present.
    """
    return changeNAValue(stripBrackets(getDictEntryCopy(cif[data],"_atom_site_B_iso_or_equiv")))



def convertUToB(s):
    """
    Take a string representing a U value and return a string representing a B value
    B = 8*Pi^2 * U

    Parameters
    ----------
    s : a string representing a U value. Could be None

    Returns
    -------
    A string representing a B value. Could be None.

    """
    if s is None:
        return None
    
    s = float(s)
    s = 8*math.pi**2*s
    s = str(round(float(s), 3)) # round B value to 3 d.p.
    return s
    





def getUiso(cif, data):
    """
    Returns a list of strings giving the isotropic atomic displacement parameters, B, of
    all atomic sites taken from "_atom_site_U_iso_or_equiv" found by multiplying their
    value by 8*Pi^2

    Used by getBeq().

    Args:
        cif: a PyCifRW dictionary
        data: the key value for a data block in the CIF
    Returns:
        A list containing the isotropic atomic displacement parameters, B, of all atomic sites.
    Raises:
        KeyError: if the key "_atom_site_U_iso_or_equiv" is not present.
    """
    Uiso = changeNAValue(stripBrackets(getDictEntryCopy(cif[data],"_atom_site_U_iso_or_equiv")))

    Biso = [convertUToB(i) for i in Uiso] ##https://stackoverflow.com/a/1614247/36061 convert string list to float list


    return Biso


def getAnisoAsIso(cif,data):
    """
    Returns a list of strings giving the equivalent isotropic atomic displacement parameters,
    B, of all atomic sites.

    The anisotropic and isotropic U and B values are obtained, where possible, and their
    relevant site labels are compared ("_atom_site_aniso_label" vs "_atom_site_label"). If a
    site is present in both lists, it takes the equivalent anisotropic value. If it is present
    only in "_atom_site_label", it takes the isotropic value. If no B values are given, it
    takes tha value "1"

    Used by getBeq().

    Args:
        cif: a PyCifRW dictionary
        data: the key value for a data block in the CIF
    Returns:
        A list containing the isotropic atomic displacement parameters, B, of all atomic sites.
    Raises:
        KeyError: if the key "_atom_site_aniso_label" is not present.
    """

    labelsAniso = getDictEntryCopy(cif[data],"_atom_site_aniso_label") #get a copy of the labels!!!
    labels      = getDictEntryCopy(cif[data],"_atom_site_label") # I alwys believe the labels. they are cannonical

    #if we get to here, then there should be some sort of anisotropic values
    try:
        Bequiv = getBaniso(cif,data) #if it isn't Baniso,
    except KeyError:
        Bequiv = getUaniso(cif,data) #then it should be Uaniso

    #do comparison with atom_labels to make sure
    # every atom has a Bequiv
    if labelsAniso == labels: #everything is there
        return Bequiv

    #if we get to here, labelsAniso != labels, and we need to figure 
    #  out which atoms are missing, and if they have B or Uiso value
    try:
        Biso = getBiso(cif, data)
    except KeyError:
        try:
            Biso = getUiso(cif, data)
        except KeyError:
            Biso = [None] * len(labels)

    #I now have the Biso values from the atom_label list

    #need to build a list of Biso values to return
    r = [None] * len(labels)
    for i in range(len(labels)): # iterate over all of the atom labels
        atom_label = labels[i] 
        try:
            aniso_index = labelsAniso.index(atom_label) #if the atom label matches aniso label, 
            r[i] = Bequiv[aniso_index] #  then copy that value into the returning list
        except ValueError:
            r[i] = Biso[i] #if the label doesn't match, then copy the result from the Biso list


    return r



def getBaniso(cif,data):
    """
    Returns a list of strings giving the equivalent isotropic atomic displacement parameters, B,
    of all atomic sites by taking the average value of "_atom_site_aniso_B_11", "_22", and "_33".

    Used by getAniso().

    Args:
        cif: a PyCifRW dictionary
        data: the key value for a data block in the CIF
    Returns:
        A list containing the isotropic atomic displacement parameters, B, of all atomic sites.
    Raises:
        KeyError: if any of the keys "_atom_site_aniso_B_11", "_22", or "_33" is not present.
    """

    #convert the str lists to float lists
    B11 = [float(i) for i in stripBrackets(getDictEntryCopy(cif[data],"_atom_site_aniso_B_11"))]
    B22 = [float(i) for i in stripBrackets(getDictEntryCopy(cif[data],"_atom_site_aniso_B_22"))]
    B33 = [float(i) for i in stripBrackets(getDictEntryCopy(cif[data],"_atom_site_aniso_B_33"))]

    Bequiv = [(B11[i] + B22[i] + B33[i])/3.0 for i in range(len(B11))] #get the average of the three values

    Bequiv = [str(round(float(i), 3)) for i in Bequiv] # round to 3 d.p.
    

    return Bequiv


def getUaniso(cif,data):
    """
    Returns a list of strings giving the equivalent isotropic atomic displacement parameters, B,
    of all atomic sites by multiplying the average value of "_atom_site_aniso_U_11", "_22",
    and "_33" by 8*Pi^2.

    Used by getAniso().

    Args:
        cif: a PyCifRW dictionary
        data: the key value for a data block in the CIF
    Returns:
        A list containing the isotropic atomic displacement parameters, B, of all atomic sites.
    Raises:
        KeyError: if any the keys "_atom_site_aniso_U_11", "_22", or "_33" is not present.
    """
    #convert the str lists to float lists
    U11 = [float(i) for i in stripBrackets(getDictEntryCopy(cif[data],"_atom_site_aniso_U_11"))]
    U22 = [float(i) for i in stripBrackets(getDictEntryCopy(cif[data],"_atom_site_aniso_U_22"))]
    U33 = [float(i) for i in stripBrackets(getDictEntryCopy(cif[data],"_atom_site_aniso_U_33"))]

    #get the average of the three values
    Bequiv = [convertUToB(str((U11[i] + U22[i] + U33[i])/3.0)) for i in range(len(U11))]

    return Bequiv




#cif = cf.ReadCif("albite_9002196.cif") #U_aniso
#cif = cf.ReadCif("9326-ICSD_3.cif")     #B_iso
#cif = cf.ReadCif("albite_9009663.cif")  #U_iso
#cif = cf.ReadCif("example.cif")  #U_iso & U_aniso - not all atoms have aniso
#cif = cf.ReadCif("Labradorits_1008757.cif") #B_aniso
#cif = cf.ReadCif("quartz_1011172.cif") # z = 1/3
#cif = cf.ReadCif("muscovite_9000837.cif")
#cif = cf.ReadCif("7217727.cif")
#data = cif.keys()[0]
