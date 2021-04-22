# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 17:10:25 2021

@author: 184277J
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
        f = re.search('.*"(.*)"', getPhaseName(cif, data)).group(1) + '.str'
        
        print("Now writing " + f)
        
        str_file = open(f, "w")
        str_file.write(s)
        str_file.close()
        
    print("Done.")


def createSTR(cif, data):
    s  = "str\n"
    s += getPhaseName(cif, data) + "\n"
    s += "\tscale @ 0.0001\n\tCS_L(,200)\n"
    s += getUnitCell(cif, data) + "\n"
    s += getSpaceGroup(cif, data) + "\n"
    s += getAtoms(cif, data)
    
    return s


def stripBrackets(l):
    # list f string or a single string with brackets at the end.
    # returns a list with strings or a string with just the first bit
    
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
    # list f string or a single string with brackets at the end.
    # returns a list with strings or a string with just the first bit
    
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


def concat(l, sep="_"):
    r = ""
    for s in l:
        r += s + sep
    r = r[0:len(r)-len(sep)] #get rid of final separator
    return r

 

#https://stackoverflow.com/a/67187811/36061
#see https://stackoverflow.com/questions/67187672/how-to-deal-with-repeated-chunks-of-code-in-function-dealing-with-dictionaries

def getDictEntry(dct, *keys, default=None):
    for key in keys:
        try:
            return dct[key]
        except KeyError:
            pass
    return default

     
def getPhaseName(cif, data):
    phasename = getDictEntry(cif[data], "_chemical_name_mineral", 
                                        "_chemical_name_common", 
                                        "_chemical_name_systematic", 
                                        "_chemical_name_structure_type", 
                                        default = "")
    return concat(["\tphase_name", '"'+concat([phasename, data])+'"'], sep=" ")
    
    
def getSpaceGroup(cif, data):
    spacegroup = getDictEntry(cif[data], "_symmetry_space_group_name_H-M", 
                                         "_symmetry_Int_Tables_number", 
                                         "_space_group_name_H-M_alt", 
                                         "_space_group_IT_number", 
                                         default = "")
    
    return concat(["\tspace_group", '"' + spacegroup + '"'], sep = " ")
    
    
def getUnitCell(cif, data):
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
            return concat(["\tCubic(",a_s,")"], sep="")
        if al == be and be == ga and al != float("90"): #rhombohedral
            return concat(["\tRhombohedral(",a_s,", ", al_s,")"], sep="")
    
    elif a == b and b != c: #tetragonal or hexagonal/trigonal
        if al == be and be == ga and al == float("90"): #tetragonal
            return concat(["\tTetragonal(",a_s,", ", c_s, ")"], sep="")
        if al == be and al == float("90") and ga == float("120"): #hexagonal (Trigonal resolves to Hexagonal in TOPAS)
            return concat(["\tHexagonal(",a_s,", ", c_s, ")"], sep="")
    
    elif a != b and a != c and b != c: #ortho, mono, tric
        if al == be and be == ga and al == float("90"): #ortho
            return concat(["\ta",a_s,"\n\tb",b_s,"\n\tc",c_s], sep=" ")
        if al != be and al != ga and be != ga: #tric
            return concat(["\ta",a_s,"\n\tb",b_s,"\n\tc",c_s,"\n\tal",al_s,"\n\tbe",be_s,"\n\tga",ga_s], sep=" ")
        if al == be and al != ga and al == float("90"): #mono_1
            return concat(["\ta",a_s,"\n\tb",b_s,"\n\tc",c_s,"\n\tga",ga_s], sep=" ")
        if al == ga and al != be and al == float("90"): #mono_2
            return concat(["\ta",a_s,"\n\tb",b_s,"\n\tc",c_s,"\n\tbe",be_s], sep=" ")
        if be == ga and be != al and be == float("90"): #mono_3
            return concat(["\ta",a_s,"\n\tb",b_s,"\n\tc",c_s,"\n\tal",al_s], sep=" ")

    #to catch everything else
    return concat(["\ta",a_s,"\n\tb",b_s,"\n\tc",c_s,"\n\tal",al_s,"\n\tbe",be_s,"\n\tga",ga_s], sep=" ")


def getUnitCell2(cif, data):
    a = stripBrackets(cif[data]["_cell_length_a"])
    b = stripBrackets(cif[data]["_cell_length_b"])
    c = stripBrackets(cif[data]["_cell_length_c"])
    al = stripBrackets(cif[data]["_cell_angle_alpha"])
    be = stripBrackets(cif[data]["_cell_angle_beta"])
    ga = stripBrackets(cif[data]["_cell_angle_gamma"]) 
    
    return concat(["\ta",a,"b",b,"c",c,"\n\tal",al,"be",be,"ga",ga], sep=" ")


def getAtoms(cif, data):
    labels = cif[data]["_atom_site_label"]
    x = stripBrackets(cif[data]["_atom_site_fract_x"])
    y = stripBrackets(cif[data]["_atom_site_fract_y"])
    z = stripBrackets(cif[data]["_atom_site_fract_z"])
    
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
    return concat(["\tsite",label,"num_posns 0 x", x, "y", y, "z", z, "occ", atom, occ, "beq",beq, "\n"], sep = " ")
    

def isThisAnAtom(s):
    #keeps the first two characters from a string and sees if it is an element
    # if not, keep the first character and try again
    # if not, return the original string
    elements = ("Ac","Ag","Al","Am","Ar","As","At","Au","Ba","B","Be","Bi","Br","Ca","Cd","C","Ce","Cl","Co","Cr","Cs","Cu","Dy","Er","Eu","F","Fe","Fr","Ga","Gd","Ge","H","He","Hg","Hf","Ho","I","In","Ir","K","Kr","La","Li","Lu","Mg","Mn","Mo","N","Na","Nb","Nd","Ne","Ni","O","Os","Pb","P","Pa","Pd","Po","Pr","Pm","Pt","Ra","Rb","Re","Rh","Rn","Ru","S","Sb","Sc","Sm","Se","Si","Sn","Sr","Ta","Tb","Tc","Te","Th","Tl","Ti","Tm","W","U","V","Xe","Y","Yb","Zn","Zr")
    
    r = s[0:2] #take the first two characters
    if r in elements:
        return r
    
    r = s[0:1] #take the first character
    if r in elements:
        return r
    
    return s #if everything fails, just return what the label was


def fixAtomSiteType(a):
    #In the sample CIFs I have, if an atom is given with a charge, then the number and sign
    #  are the wrong way around for TOPAS. This just switches the charge and sign around
    #  to make it compatible
    
    # Cu   --> Cu
    #  I   -->  I
    #  K+  -->  K+1
    #  V3+ -->  V+3
    # Fe2+ --> Fe+2
    #  O1- -->  O-1
    
    #assumes that the above strings are the only sort that can appear

    regex = re.search("([A-Za-z]{1,2})(\d{0,2})([+-]{0,1})(\d{0,2})", a)
    
    symbol = regex.group(1)
    charge = regex.group(2)
    sign = regex.group(3)
    digit = regex.group(4) #if there is a trailing digit, then that is probably the charge
    
    print(symbol)
    print(charge)
    print(sign)
    print(digit)
    
    
    #check for a single sign with no charge. eg F-. Needs to return F-1
    if len(sign) == 1 and len(charge) == 0:
        if len(digit) == 0:
            charge = "1"
        else: #the atom was probably the right way around to begin with
            return a
        
    return symbol+sign+charge
        
        
    
def getBeq(cif, data):
    
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
    return changeQuestionMark(stripBrackets(cif[data]["_atom_site_B_iso_or_equiv"]))


def getUiso(cif, data):
    Uiso = changeQuestionMark(stripBrackets(cif[data]["_atom_site_U_iso_or_equiv"]))
    
    Uiso = [float(i) for i in Uiso] #https://stackoverflow.com/a/1614247/36061 convert string list to float list
    Biso = [i * 8 * math.pi**2 for i in Uiso] #convert to Biso
    Biso = [str(i) for i in Biso]
    Biso = [i[0:i.index(".")+4] for i in Biso] #truncate string at 3 d.p.

    return Biso 


def getAniso(cif,data):  
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
    # Get anisotropic B values and return an average of the ellipsoid to make Biso

    #convert the str lists to float lists
    B11 = [float(i) for i in stripBrackets(cif[data]["_atom_site_aniso_B_11"])]
    B22 = [float(i) for i in stripBrackets(cif[data]["_atom_site_aniso_B_22"])]
    B33 = [float(i) for i in stripBrackets(cif[data]["_atom_site_aniso_B_33"])]

    Bequiv = [(B11[i] + B22[i] + B33[i])/3.0 for i in range(len(B11))] #get the average of the three values
    
    Bequiv = [str(i) for i in Bequiv]
    Bequiv = [i[0:i.index(".")+4] for i in Bequiv] #truncate string at 3 d.p.

    return Bequiv


def getUaniso(cif,data):
    # Get anisotropic U values and return an average of the ellipsoid to make Uiso.
    #  Then multiply by 8*Pi^2 to make Biso to work nicely with Topas
    
    
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
"specifc order of precedence, as detailed in the sections below. In general, if a value exists\n"+\
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
"The atomic sites are constructed as follows. The atom labels are taken from '_atom_site_label', \n"+\
"with the fractional x, y, and z coordinates given by '_atom_site_fract_x', '_y', and '_z'. \n"+\
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

#cif = cf.ReadCif("muscovite_9000837.cif")
#data = cif.keys()[0]

#text_file = open("test with space.str", "w")
#text_file.write(makeSTR(cif, data))
#text_file.close()


#   phase name
#   a b c
#   al be ga
#   space group
#   site x y z occ B 


