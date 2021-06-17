# -*- coding: utf-8 -*-
"""
SPDX-License-Identifier:  GNU Lesser General Public License v3.0 or later

Copyright © 2021 Matthew Rowles

Created on Thu Jun 10 16:18:56 2021

@author: Matthew Rowles
"""
from struct import unpack
from glob import glob #for command line arguments
import sys #for command line arguments


def change_endian(hexstr):
  change_me = bytearray.fromhex(hexstr)
  change_me.reverse()
  str_little = "".join(format(x, "02x") for x in change_me)
  return str_little

def get_hex_codes(hexstr, offset, length):
    offset *= 2 #these values are given in octets, now they're in chrs for the string
    length = offset + 2*length
    return hexstr[offset:length]

def hex_to_char(hexstr):
    return hex_to_str(hexstr)

def hex_to_str(hexstr):
    try:
        return bytes.fromhex(hexstr).decode("ASCII")
    except UnicodeDecodeError:
        return "_?_"

def hex_to_int(hexstr):
    return int(change_endian(hexstr), 16)

def hex_to_double(hexstr):
    return unpack("d", bytes.fromhex(hexstr))[0]

def hex_to_float(hexstr):
    return unpack("f", bytes.fromhex(hexstr))[0]

def conv_hex(hexstr, conv="byte"):
    if conv == "char" or conv == "str":
        return hex_to_char(hexstr)
    elif conv == "int":
        return hex_to_int(hexstr)
    elif conv == "double":
        return hex_to_double(hexstr)
    elif conv == "float" or conv == "single":
        return hex_to_float(hexstr)
    else:
        return hexstr

def get_info_from_chunk(hex_chunk, scan, resolution, rounding = 50):
    day        = str(      conv_hex(get_hex_codes(hex_chunk, 0                , 2), "int"))
    month      = str(      conv_hex(get_hex_codes(hex_chunk, 2                , 2), "int"))
    year       = str(      conv_hex(get_hex_codes(hex_chunk, 4                , 2), "int"))
    hour       = str(      conv_hex(get_hex_codes(hex_chunk, 6                , 2), "int"))
    minute     = str(      conv_hex(get_hex_codes(hex_chunk, 8                , 2), "int"))
    second     = str(      conv_hex(get_hex_codes(hex_chunk, 10               , 2), "int"))
    millis     = str(      conv_hex(get_hex_codes(hex_chunk, 12               , 2), "int"))
    count_time = str(round(conv_hex(get_hex_codes(hex_chunk, 14               , 4), "single"), rounding))
    omega      = str(round(conv_hex(get_hex_codes(hex_chunk, 18 + 4*resolution, 4), "single"), rounding))
    phi        = str(round(conv_hex(get_hex_codes(hex_chunk, 22 + 4*resolution, 4), "single"), rounding))
    theta2     = str(round(conv_hex(get_hex_codes(hex_chunk, 26 + 4*resolution, 4), "single"), rounding))
    chi        = str(round(conv_hex(get_hex_codes(hex_chunk, 30 + 4*resolution, 4), "single"), rounding))
    Tr_X       = str(round(conv_hex(get_hex_codes(hex_chunk, 34 + 4*resolution, 4), "single"), rounding))
    Tr_Y       = str(round(conv_hex(get_hex_codes(hex_chunk, 38 + 4*resolution, 4), "single"), rounding))
    Tr_Z       = str(round(conv_hex(get_hex_codes(hex_chunk, 42 + 4*resolution, 4), "single"), rounding))
    temperature= str(round(conv_hex(get_hex_codes(hex_chunk, 46 + 4*resolution, 4), "single"), rounding))
    filters    = str(round(conv_hex(get_hex_codes(hex_chunk, 50 + 4*resolution, 4), "single"), rounding))
    label      = str(      conv_hex(get_hex_codes(hex_chunk, 54 + 4*resolution,10), "char"))

    return (str(scan), year, month, day, hour, minute, second, millis, count_time, theta2, omega, phi, chi, Tr_X, Tr_Y, Tr_Z, temperature, filters, label)


def do_FDT(inFile, outFile):
    header_str = ("scan", "year", "month", "day", "hour","minute","second","millis","time",
                  "theta2","omega","phi", "chi","X","Y","Z","temp","filter","label\n")

    with open(inFile, "rb") as binaryFile, open(outFile, "w") as outputFile:
        print(f"Reading {inFile}.")
        header = binaryFile.read(16448).hex()

        resolution  = conv_hex(get_hex_codes(header, 0, 2), "int") * 1024
        total_scans = conv_hex(get_hex_codes(header, 2, 2), "int")

        chunk_size = 64 + 4*resolution

        outputFile.write("\t".join(header_str))

        print(f"Writing to {outFile}.")
        for scan in range(1, total_scans + 1):
            print(f"Now doing {scan} of {total_scans}")
            chunk = binaryFile.read(chunk_size).hex()
            data = "\t".join(get_info_from_chunk(chunk, scan, resolution, 5)) + "\n"
            outputFile.write(data)

HELP = "To output the resumes of FDT files.\n>python resume_FDT.py *.fdt\nMatthew Rowles matthew.rowles@curtin.edu.au"

def main():
    if len(sys.argv) <= 1: #Assume the user needs some guidance
        print(HELP)
        sys.exit()

    inFilenames = []
    for i in range(1,len(sys.argv)):
        globarg = glob(sys.argv[i])
        inFilenames += globarg
    outFilenames = [f + ".resume" for f in inFilenames]

    for inFile, outFile in zip(inFilenames, outFilenames):
        do_FDT(inFile, outFile)

if __name__ == "__main__":
    main()
