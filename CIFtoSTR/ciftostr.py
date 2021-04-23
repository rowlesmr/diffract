# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 17:10:25 2021

@author: Matthew Rowles
"""

import CifFile as cf #https://pypi.org/project/PyCifRW/4.4/  https://bitbucket.org/jamesrhester/pycifrw/downloads/
import math
import re #regular expression
import sys #for command line arguments
from glob import glob #for command line arguments


def writeSTR(ciffile):
    cif = cf.ReadCif(ciffile)
    datakeys = cif.keys()
    
    for data in datakeys:
        s = createSTR(cif, data)
        f = getPhaseName(cif, data) + '.str'
        
        print("Now writing " + f)
        
        str_file = open(f, "w")
        str_file.write(s)
        str_file.close()
        
    print("Done.")


def createSTR(cif, data):
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

   
def changeQuestionMark(l):
    """
    If a string consists of a single question mark ('?'), it is replaced with a zero ('0'). 
    
    Args:
        l: A list of strings, or a single string.
    Returns:
        A list of strings, or a single string, with zero in place of a single question mark
     """
    
    changeMe = False
    if isinstance(l, str): #if it's a single string, make it a list
        l = [l]
        changeMe = True
    
    for i in range(len(l)):
        s = l[i]    
        
        if s == "?":
            l[i] = "0"
        
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
    
    
    
    changeMe = False
    if isinstance(l, str): #if it's a single string, make it a list
        l = [l]
        changeMe = True
    
    for i in range(len(l)):
        if l[i] in oneSixth:
            l[i] = oneSixthFrac
        elif l[i] in oneThird:
            l[i] = oneThirdFrac
        elif l[i] in twoThird:
            l[i] = twoThirdFrac
        elif l[i] in fiveSixth:
            l[i] = fiveSixthFrac
        else:
            pass #l[i] is all good
        
    if changeMe: #if it was a list, change it back
        l = l[0]

    return l
                






def getDictEntry(dct, *keys, default=None):
    """
    Returns the first dictionary value to match from an arbitrary number of given keys.
    If there is no match, the default value is returned.
    #https://stackoverflow.com/a/67187811/36061

    
    Args:
        dct: A dictionary
        *keys: an arbitrary number of keys in order of preference for return.
        default: The value to return if no matching entry is found in the dictionary.
    Returns:
        The dictionary value associated with the first key to match, or the default value.
     """
    for key in keys:
        try:
            return dct[key]
        except KeyError:
            pass
    return default

     
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
    phasename = getDictEntry(cif[data], "_chemical_name_mineral", 
                                        "_chemical_name_common", 
                                        "_chemical_name_systematic", 
                                        "_chemical_name_structure_type", 
                                        default = "")
    return concat(phasename, data)
    
    
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
    spacegroup = getDictEntry(cif[data], "_symmetry_space_group_name_H-M", 
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
    
    a_s  = stripBrackets(cif[data]["_cell_length_a"])
    b_s  = stripBrackets(cif[data]["_cell_length_b"])
    c_s  = stripBrackets(cif[data]["_cell_length_c"])
    al_s = stripBrackets(cif[data]["_cell_angle_alpha"])
    be_s = stripBrackets(cif[data]["_cell_angle_beta"])
    ga_s = stripBrackets(cif[data]["_cell_angle_gamma"]) 
    
    a  = float(a_s)
    b  = float(b_s)
    c  = float(c_s)
    al = float(al_s)
    be = float(be_s)
    ga = float(ga_s)
    
    if a == b and b == c: #cubic or rhombohedral
        if al == be and be == ga and al == float("90"): #cubic
            return concat("\tCubic(",a_s,")", sep="")
        if al == be and be == ga and al != float("90"): #rhombohedral
            return concat("\tRhombohedral(",a_s,", ", al_s,")", sep="")
    
    elif a == b and b != c: #tetragonal or hexagonal/trigonal
        if al == be and be == ga and al == float("90"): #tetragonal
            return concat("\tTetragonal(",a_s,", ", c_s, ")", sep="")
        if al == be and al == float("90") and ga == float("120"): #hexagonal (Trigonal resolves to Hexagonal in TOPAS)
            return concat("\tHexagonal(",a_s,", ", c_s, ")", sep="")
    
    elif a != b and a != c and b != c: #ortho, mono, tric
        if al == be and be == ga and al == float("90"): #ortho
            return concat("\ta",a_s,"\n\tb",b_s,"\n\tc",c_s, sep=" ")
        if al != be and al != ga and be != ga: #tric
            return concat("\ta",a_s,"\n\tb",b_s,"\n\tc",c_s,"\n\tal",al_s,"\n\tbe",be_s,"\n\tga",ga_s, sep=" ")
        if al == be and al != ga and al == float("90"): #mono_1
            return concat("\ta",a_s,"\n\tb",b_s,"\n\tc",c_s,"\n\tga",ga_s, sep=" ")
        if al == ga and al != be and al == float("90"): #mono_2
            return concat("\ta",a_s,"\n\tb",b_s,"\n\tc",c_s,"\n\tbe",be_s, sep=" ")
        if be == ga and be != al and be == float("90"): #mono_3
            return concat("\ta",a_s,"\n\tb",b_s,"\n\tc",c_s,"\n\tal",al_s, sep=" ")

    #to catch everything else
    return concat("\ta",a_s,"\n\tb",b_s,"\n\tc",c_s,"\n\tal",al_s,"\n\tbe",be_s,"\n\tga",ga_s, sep=" ")


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
    a = stripBrackets(cif[data]["_cell_length_a"])
    b = stripBrackets(cif[data]["_cell_length_b"])
    c = stripBrackets(cif[data]["_cell_length_c"])
    al = stripBrackets(cif[data]["_cell_angle_alpha"])
    be = stripBrackets(cif[data]["_cell_angle_beta"])
    ga = stripBrackets(cif[data]["_cell_angle_gamma"]) 
    
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
    labels = cif[data]["_atom_site_label"]
    x = valToFrac(stripBrackets(cif[data]["_atom_site_fract_x"]))
    y = valToFrac(stripBrackets(cif[data]["_atom_site_fract_y"]))
    z = valToFrac(stripBrackets(cif[data]["_atom_site_fract_z"]))
    
    #type of atom
    try:
        atoms = cif[data]["_atom_site_type_symbol"]
        
        atoms = [fixAtomSiteType(i) for i in atoms]
        
    except KeyError:
        atoms = []
        for l in labels:
            atoms += [isThisAnAtom(l)]

    #occupancy
    try:
        occ = stripBrackets(cif[data]["_atom_site_occupancy"])
    except KeyError:
        occ = ["1"] * len(labels)

    #ADPs
    Biso = getBeq(cif, data)
    
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
    return concat("\tsite",label,"num_posns 0 x", x, "y", y, "z", z, "occ", atom, occ, "beq",beq, "\n", sep = " ")
    

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
                "Yb","Zn","Zr")
    
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
        
    #check for a single sign with no charge. eg F-. Needs to return F-1
    if len(sign) == 1 and len(charge) == 0:
        if len(digit) == 0:
            charge = "1"
        else: #the atom was probably the right way around to begin with
            return a
        
    return symbol+sign+charge
        
        
    
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
    
    try:
        return getAniso(cif,data)
    except KeyError:
        pass
    
    try:
        return getUiso(cif, data)
    except KeyError:
        pass
       
    try:
        return getBiso(cif,data)
    except KeyError:
        pass
    
    #if we get here, there were no B values in the CIF. Booo!
    return ["1"]*len(cif[data]["_atom_site_label"])


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
    return changeQuestionMark(stripBrackets(cif[data]["_atom_site_B_iso_or_equiv"]))


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
    Uiso = changeQuestionMark(stripBrackets(cif[data]["_atom_site_U_iso_or_equiv"]))
    
    Uiso = [float(i) for i in Uiso] #https://stackoverflow.com/a/1614247/36061 convert string list to float list
    Biso = [i * 8 * math.pi**2 for i in Uiso] #convert to Biso
    Biso = [str(i) for i in Biso]
    Biso = [i[0:i.index(".")+4] for i in Biso] #truncate string at 3 d.p.

    return Biso 


def getAniso(cif,data):  
    """
    Returns a list of strings giving the equivalent isotropic atomic displacement parameters, B, 
    of all atomic sites.
    
    The anisotropic and isotropic U and B values are obtained, where possible, and their relevant
    site labels are compared ("_atom_site_aniso_label" vs "_atom_site_label"). If a site is present 
    in both lists, it takes the equivalent anisotropic value. If it is present only in "_atom_site_label",
    it takes the isotropic value. If no B values are given, it takes tha value "1"
    
    Used by getBeq().
    
    Args:
        cif: a PyCifRW dictionary
        data: the key value for a data block in the CIF
    Returns:
        A list containing the isotropic atomic displacement parameters, B, of all atomic sites.
    Raises:
        KeyError: if the key "_atom_site_aniso_label" is not present.
    """

    labelsAniso = cif[data]["_atom_site_aniso_label"]
    labels      = cif[data]["_atom_site_label"]
    
    #if we get to here, then there should be some sort of anisotropic values
    try:
        Bequiv = getBaniso(cif,data) #if it isn't Baniso, 
    except KeyError:
        Bequiv = getUaniso(cif,data) #then it should be Uaniso
    
    
    #do comparison with atom_labels to make sure
    # every atom has a Bequiv
    if labelsAniso == labels: #everything is there
        return Bequiv
    
    #if we get to here, labelsAniso != labels, and we need to figure out what is good.
    try:
        Biso = getBiso(cif, data)
    except KeyError:
        try:
            Biso = getUiso(cif, data)
        except KeyError:
            Biso = ["1"] * len(labels)
    
    #I now have the Biso values from the atom_label list
    
    #need to build a list of Biso values to return
    r = ["1"] * len(labels)
    for i in range(len(labels)):
        atom_label = labels[i]
        try:
            aniso_index = labelsAniso.index(atom_label)
            r[i] = Bequiv[aniso_index]
        except ValueError:
            r[i] = Biso[i]
    
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
    B11 = [float(i) for i in stripBrackets(cif[data]["_atom_site_aniso_B_11"])]
    B22 = [float(i) for i in stripBrackets(cif[data]["_atom_site_aniso_B_22"])]
    B33 = [float(i) for i in stripBrackets(cif[data]["_atom_site_aniso_B_33"])]

    Bequiv = [(B11[i] + B22[i] + B33[i])/3.0 for i in range(len(B11))] #get the average of the three values
    
    Bequiv = [str(i) for i in Bequiv]
    Bequiv = [i[0:i.index(".")+4] for i in Bequiv] #truncate string at 3 d.p.

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
    U11 = [float(i) for i in stripBrackets(cif[data]["_atom_site_aniso_U_11"])]
    U22 = [float(i) for i in stripBrackets(cif[data]["_atom_site_aniso_U_22"])]
    U33 = [float(i) for i in stripBrackets(cif[data]["_atom_site_aniso_U_33"])]

    Bequiv = [8*math.pi**2 * (U11[i] + U22[i] + U33[i])/3.0 for i in range(len(U11))] #get the average of the three values
    
    Bequiv = [str(i) for i in Bequiv]
    Bequiv = [i[0:i.index(".")+4] for i in Bequiv] #truncate string at 3 d.p.

    return Bequiv

 
    
    
    
       
    
help_s = \
"\nThis program converts an arbitrary number of CIFs, each containing an arbitrary number of \n"+\
"structures into a number of individual STR files that are (supposed to be) compatible with TOPAS.\n\n"+ \
\
">python ciftostr.py *.cif\n or you can type the individual names of CIFs to use after the py file.\n\n" + \
\
"If you would like some information on what the program does: >python ciftostr.py -info\n\n"+\
\
"This program requires PyCifRW. For instructions on how to install it, please see \n"+\
 "https://bitbucket.org/jamesrhester/pycifrw/src/development/INSTALLATION\n\n" + \
\
"Matthew Rowles. matthew.rowles@curtin.edu.au 22 Apr 21"
    
 


info_s = \
"This program is designed to reformat data from a CIF format into the STR format suitable\n"+\
"for use by the Rietveld analysis software, TOPAS. It doesn't carry out any validation checks\n"+\
"to ensure the data is consistent, but simply transcribes the data as given in the CIF.\n\n"+\
    \
"Where similar or identical data could be given in several places, the values are taken in a\n"+\
"specific order of precedence, as detailed in the sections below. In general, if a value exists\n"+\
"in an earlier place, the later places are not looked at.\n\n"+\
\
"This program uses the PyCifRW library, written by James Hester, to parse the CIF files in to\n"+\
"a format easily used to remix the underlying data.\n\n"+\
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
"The space_group is taken from '_symmetry_space_group_name_H-M', '_symmetry_Int_Tables_number', \n"+\
"'_space_group_name_H-M_alt', or '_space_group_IT_number', in that order. If none of these keys\n"+\
"are available, then an empty string is written as the space group. The value of the space group is \n"+\
"as exactly given in the CIF. No validation or editing is done.\n\n"+\
\
"The atomic sites are constructed as follows: The atom labels are taken from '_atom_site_label', \n"+\
"with the fractional x, y, and z coordinates given by '_atom_site_fract_x', '_y', and '_z'. \n"+\
"If the decimal values of the fractional coordinates are consistent with the fractions 1/6, 1/3, 2/3,\n"+\
"or 5/6, then the decimal value is replaced by the fractional representation.\n"+\
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
"Finally, the STR is given a Lorentzian crystallite size of 200 nm, and a refinable scale factor\n"+\
"of 0.0001 to allow for an easy start to a refinement. All values given in the STR are fixed,\n"+\
"and require active intervention to refine, constrain, or restrain them.\n\n"+\
\
"If you have any feedback, please contact me. If you find any bugs, please provide the CIF which \n"+\
"caused the error, a description of the error, and a description of how you believe the program\n"+\
"should work in that instance.\n\n"+\
\
"Thanks, Matthew Rowles.\n"+\
"matthew.rowles@curtin.edu.au\n"+\
"22 Apr 21"    

    
#This is the actaul bit that does the work.    



if len(sys.argv) <= 1: #there aren't any files to deal with
    print(help_s)
    sys.exit()
 
    
if "-info" in sys.argv:
    print(info_s)
    sys.exit()
 
    
filenames = []
for i in range(1,len(sys.argv)):
    filenames += glob(sys.argv[i])



for file in filenames:
    
    try:
        writeSTR(file)

    except Exception as e: #just print the exception and keep going

       # print traceback.format_exc()
        print(e)





#cif = cf.ReadCif('jun_01_2.cif')




#see the end of the file for the actual bits that do the work


#for arg in glob(sys.argv):
#    print(arg)



#cif = cf.ReadCif("albite_9002196.cif") #U_aniso 
#cif = cf.ReadCif("9326-ICSD_3.cif")     #B_iso
#cif = cf.ReadCif("albite_9009663.cif")  #U_iso
#cif = cf.ReadCif("example.cif")  #U_iso & U_aniso - not all atoms have aniso
#cif = cf.ReadCif("Labradorits_1008757.cif") #B_aniso
cif = cf.ReadCif("quartz_1011172.cif") # z = 1/3
#cif = cf.ReadCif("muscovite_9000837.cif")
data = cif.keys()[0]

#text_file = open("test with space.str", "w")
#text_file.write(makeSTR(cif, data))
#text_file.close()


#   phase name
#   a b c
#   al be ga
#   space group
#   site x y z occ B 


