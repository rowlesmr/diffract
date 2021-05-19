# -*- coding: utf-8 -*-
"""
Created on Sat May 15 23:10:34 2021

@author: 184277J
"""

# pylint: disable=line-too-long.

import unittest
import ciftostr as cf

class Testciftostr(unittest.TestCase):

    def test_strip_brackets(self):
        self.assertEqual(cf.strip_brackets("0.234(6)"), "0.234")
        self.assertEqual(cf.strip_brackets("0.234(6)78"), "0.234")
        self.assertEqual(cf.strip_brackets("0.234(678)"), "0.234")
        self.assertEqual(cf.strip_brackets("0.234"), "0.234")

    def test_change_NA_value(self):
        self.assertIsNone(cf.change_NA_value("."))
        self.assertIsNone(cf.change_NA_value("?"))
        self.assertEqual(cf.change_NA_value("string"), "string")
        self.assertEqual(cf.change_NA_value(".."), "..")
        self.assertEqual(cf.change_NA_value("??"), "??")
        self.assertEqual(cf.change_NA_value(".?"), ".?")

    def test_val_to_frac(self):
        self.assertEqual(cf.val_to_frac("0.16667"), "=1/6;")
        self.assertEqual(cf.val_to_frac("0.33333"), "=1/3;")
        self.assertEqual(cf.val_to_frac("0.66667"), "=2/3;")
        self.assertEqual(cf.val_to_frac("0.83333"), "=5/6;")
        self.assertEqual(cf.val_to_frac("0.12345"), "0.12345")
        self.assertIsNone(cf.val_to_frac(None))

    def test_get_dict_entry_copy(self):
        cif = { "data" : {"_chemical_name_mineral": "name1",
                          "_chemical_name_common" : "name2",
                          "_chemical_name_systematic" : "name3",
                          "_chemical_name_structure_type" : "name4"}}
        a_copy = {"_chemical_name_mineral": "name1",
                    "_chemical_name_common" : "name2",
                    "_chemical_name_systematic" : "name3",
                    "_chemical_name_structure_type" : "name4"}

        self.assertEqual(cf.get_dict_entry_copy(cif, "data"), a_copy)
        self.assertEqual(cf.get_dict_entry_copy(cif["data"], "_chemical_name_structure_type"), "name4")
        self.assertIsNone(cf.get_dict_entry_copy(cif["data"], "_something_different"))
        self.assertEqual(cf.get_dict_entry_copy(cif["data"], "_something_different", default ="str"), "str")
        self.assertEqual(cf.get_dict_entry_copy(cif, "data"), cif["data"])
        self.assertFalse(cf.get_dict_entry_copy(cif, "data") is cif["data"])

    def test_get_dict_entry_copy_throw_error(self):
        cif = { "data" : {"_chemical_name_mineral": "name1",
                          "_chemical_name_common" : "name2",
                          "_chemical_name_systematic" : "name3",
                          "_chemical_name_structure_type" : "name4"}}
        a_copy = {"_chemical_name_mineral": "name1",
                    "_chemical_name_common" : "name2",
                    "_chemical_name_systematic" : "name3",
                    "_chemical_name_structure_type" : "name4"}

        self.assertEqual(cf.get_dict_entry_copy_throw_error(cif, "data"), a_copy)
        self.assertEqual(cf.get_dict_entry_copy_throw_error(cif["data"], "_chemical_name_structure_type"), "name4")
        self.assertRaises(KeyError, cf.get_dict_entry_copy_throw_error, cif["data"], "_something_different")
        self.assertEqual(cf.get_dict_entry_copy_throw_error(cif, "data"), cif["data"])
        self.assertFalse(cf.get_dict_entry_copy_throw_error(cif, "data") is cif["data"])

    def test_pad_string_list(self):
        self.assertIsNone(cf.pad_string_list(None))
        self.assertEqual(cf.pad_string_list(["0.123", "-0.345", "0.4567"]), [" 0.123 ", "-0.345 ", " 0.4567"])

    def test_pad_string(self):
        self.assertEqual(cf.pad_string("0.123", 6, "post"), "0.123 ")
        self.assertEqual(cf.pad_string("0.123", 6, "pre"), " 0.123")
        self.assertEqual(cf.pad_string("0.123", 3, "post"), "0.123")
        self.assertIsNone(cf.pad_string(None, 4, "pre"))

    def test_count_nones(self):
        self.assertEqual(cf.count_nones([1,2,None]), 1)
        self.assertEqual(cf.count_nones([]), 0)
        self.assertEqual(cf.count_nones([None]), 1)
        self.assertEqual(cf.count_nones([1,2,3,4,5]), 0)
        self.assertEqual(cf.count_nones([None, None]), 2)

    def test_clean_phasename(self):
        self.assertEqual(cf.clean_phasename("name"), "name")
        self.assertEqual(cf.clean_phasename("  name \t"), "name")
        self.assertEqual(cf.clean_phasename("\nname"), "name")
        self.assertEqual(cf.clean_phasename("name\r"), "name")

    def test_clean_filename(self):
        self.assertEqual(cf.clean_filename("name"), "name")
        self.assertEqual(cf.clean_filename("name."), "name_")
        self.assertEqual(cf.clean_filename("con"), "con_")
        self.assertEqual(cf.clean_filename("CON"), "CON_")
        self.assertEqual(cf.clean_filename("n*:am<e>"), "n__am_e_")

    def test_make_atom_site_string(self):
        self.assertEqual(cf.make_atom_site_string("Al1", "0.123", "0.234", "0.345", "Al+3", "0.5", "1."),
                                                  "\t\tsite Al1 num_posns 0\tx 0.123 y 0.234 z 0.345 occ Al+3 0.5 beq 1.")

    def test_convert_site_label_to_atom(self):
        self.assertEqual(cf.convert_site_label_to_atom("as"), "as")
        self.assertEqual(cf.convert_site_label_to_atom("AS"), "AS")
        self.assertEqual(cf.convert_site_label_to_atom("As"), "As")
        self.assertEqual(cf.convert_site_label_to_atom("pz"), "pz")
        self.assertEqual(cf.convert_site_label_to_atom("Pz"), "P")
        self.assertEqual(cf.convert_site_label_to_atom("As1"), "As")
        self.assertEqual(cf.convert_site_label_to_atom("OW1"), "O")
        self.assertEqual(cf.convert_site_label_to_atom("ss123"), "ss123")     
        self.assertEqual(cf.convert_site_label_to_atom("WatX6A"), "O")

    def test_fix_atom_type(self):
        self.assertEqual(cf.fix_atom_type("Cu"),   "Cu")
        self.assertEqual(cf.fix_atom_type("I"),    "I")
        self.assertEqual(cf.fix_atom_type("K+"),   "K+1")
        self.assertEqual(cf.fix_atom_type("V3+"),  "V+3")
        self.assertEqual(cf.fix_atom_type("Fe2+"), "Fe+2")
        self.assertEqual(cf.fix_atom_type("O1-"),  "O-1")
        self.assertEqual(cf.fix_atom_type("Cu0+"), "Cu")
        self.assertEqual(cf.fix_atom_type("Cu0"),  "Cu")
        self.assertEqual(cf.fix_atom_type("Fe+3"), "Fe+3")

    def test_convert_atom_type_to_topas(self):
        self.assertEqual(cf.convert_atom_type_to_topas("H"),    "H")
        self.assertEqual(cf.convert_atom_type_to_topas("H+1"),  "H")
        self.assertEqual(cf.convert_atom_type_to_topas("H-1"),  "H-1")
        self.assertEqual(cf.convert_atom_type_to_topas("Si+0"), "Si")
        self.assertEqual(cf.convert_atom_type_to_topas("Cu+8"), "Cu")

    def test_convert_u_to_b(self):
        self.assertIsNone(cf.convert_u_to_b(None))
        self.assertEqual(cf.convert_u_to_b("0.0123"), '0.971')
        self.assertEqual(cf.convert_u_to_b("1"), "78.957")

    def test_get_phasename(self):
        cif = { "data" : {"_chemical_name_mineral": "name1",
                          "_chemical_name_common" : "name2",
                          "_chemical_name_systematic" : "name3",
                          "_chemical_name_structure_type" : "name4"}}
        self.assertEqual(cf.get_phasename(cif, "data"), "name1_data")

        cif = { "data" : {"_chemical_name_common" : "name2",
                          "_chemical_name_systematic" : "name3",
                          "_chemical_name_structure_type" : "name4"}}
        self.assertEqual(cf.get_phasename(cif, "data"), "name2_data")

        cif = { "data" : {"_chemical_name_systematic" : "name3",
                          "_chemical_name_structure_type" : "name4"}}
        self.assertEqual(cf.get_phasename(cif, "data"), "name3_data")

        cif = { "data" : {"_chemical_name_structure_type" : "name4"}}
        self.assertEqual(cf.get_phasename(cif, "data"), "name4_data")

        cif = { "data" : {"_something_different" : "name5"}}
        self.assertEqual(cf.get_phasename(cif, "data"), "data")

        cif = { "data" : {"_chemical_name_structure_type" : "."}}
        self.assertEqual(cf.get_phasename(cif, "data"), "data")

        cif = { "data" : {"_chemical_name_structure_type" : "?"}}
        self.assertEqual(cf.get_phasename(cif, "data"), "data")

        cif = { "data" : {"_chemical_name_structure_type" : ""}}
        self.assertEqual(cf.get_phasename(cif, "data"), "data")

        #cif = { "data" : {"_chemical_name_structure_type" : None}}
        #self.assertEqual(cf.get_phasename(cif, "data"), "data")


    def test_get_spacegroup(self):
        cif = { "data" : {"_symmetry_space_group_name_H-M": "sg1",
                          "_space_group_name_H-M_alt" : "sg2",
                          "_symmetry_Int_Tables_number" : "3",
                          "_space_group_IT_number" : "4"}}
        self.assertEqual(cf.get_spacegroup(cif, "data"), "sg1")

        cif = { "data" : {"_space_group_name_H-M_alt" : "sg2",
                          "_symmetry_Int_Tables_number" : "3",
                          "_space_group_IT_number" : "4"}}
        self.assertEqual(cf.get_spacegroup(cif, "data"), "sg2")

        cif = { "data" : {"_symmetry_Int_Tables_number" : "3",
                          "_space_group_IT_number" : "4"}}
        self.assertEqual(cf.get_spacegroup(cif, "data"), "3")

        cif = { "data" : {"_space_group_IT_number" : "4"}}
        self.assertEqual(cf.get_spacegroup(cif, "data"), "4")

        cif = { "data" : {"_something_different" : "4"}}
        self.assertEqual(cf.get_spacegroup(cif, "data"), "")


    def test_get_unitcell(self):
        cif = { "data" : {"_cell_length_a" : "5.12",
                          "_cell_length_b" : "5.12",
                          "_cell_length_c" : "5.12",
                          "_cell_angle_alpha" : "90",
                          "_cell_angle_beta"  : "90.",
                          "_cell_angle_gamma" : "90.000"}}
        self.assertEqual(cf.get_unitcell(cif, "data"), '\t\tCubic(5.12)')

        cif = { "data" : {"_cell_length_a" : "5.12",
                          "_cell_length_b" : "5.12",
                          "_cell_length_c" : "5.12",
                          "_cell_angle_alpha" : "63",
                          "_cell_angle_beta"  : "63",
                          "_cell_angle_gamma" : "63"}}
        self.assertEqual(cf.get_unitcell(cif, "data"), '\t\tRhombohedral(5.12, 63)')

        cif = { "data" : {"_cell_length_a" : "5.12",
                          "_cell_length_b" : "5.12",
                          "_cell_length_c" : "6.34",
                          "_cell_angle_alpha" : "90",
                          "_cell_angle_beta"  : "90.",
                          "_cell_angle_gamma" : "90.000"}}
        self.assertEqual(cf.get_unitcell(cif, "data"), '\t\tTetragonal(5.12, 6.34)')

        cif = { "data" : {"_cell_length_a" : "5.12",
                          "_cell_length_b" : "5.12",
                          "_cell_length_c" : "6.34",
                          "_cell_angle_alpha" : "90",
                          "_cell_angle_beta"  : "90.",
                          "_cell_angle_gamma" : "120."}}
        self.assertEqual(cf.get_unitcell(cif, "data"), '\t\tHexagonal(5.12, 6.34)')

        cif = { "data" : {"_cell_length_a" : "5.12",
                          "_cell_length_b" : "6.34",
                          "_cell_length_c" : "7.56",
                          "_cell_angle_alpha" : "90",
                          "_cell_angle_beta"  : "90.",
                          "_cell_angle_gamma" : "90.000"}}
        self.assertEqual(cf.get_unitcell(cif, "data"), "\t\ta 5.12\n\t\tb 6.34\n\t\tc 7.56")

        cif = { "data" : {"_cell_length_a" : "5.12",
                          "_cell_length_b" : "6.34",
                          "_cell_length_c" : "7.56",
                          "_cell_angle_alpha" : "123",
                          "_cell_angle_beta"  : "89.5",
                          "_cell_angle_gamma" : "92"}}
        self.assertEqual(cf.get_unitcell(cif, "data"), "\t\ta  5.12\n\t\tb  6.34\n\t\tc  7.56\n\t\tal 123\n\t\tbe 89.5\n\t\tga 92")

        cif = { "data" : {"_cell_length_a" : "5.12",
                          "_cell_length_b" : "6.34",
                          "_cell_length_c" : "7.56",
                          "_cell_angle_alpha" : "90",
                          "_cell_angle_beta"  : "90",
                          "_cell_angle_gamma" : "92"}}
        self.assertEqual(cf.get_unitcell(cif, "data"), "\t\ta  5.12\n\t\tb  6.34\n\t\tc  7.56\n\t\tga 92")

        cif = { "data" : {"_cell_length_a" : "5.12",
                          "_cell_length_b" : "6.34",
                          "_cell_length_c" : "7.56",
                          "_cell_angle_alpha" : "90",
                          "_cell_angle_beta"  : "92",
                          "_cell_angle_gamma" : "90"}}
        self.assertEqual(cf.get_unitcell(cif, "data"), "\t\ta  5.12\n\t\tb  6.34\n\t\tc  7.56\n\t\tbe 92")

        cif = { "data" : {"_cell_length_a" : "5.12",
                          "_cell_length_b" : "6.34",
                          "_cell_length_c" : "7.56",
                          "_cell_angle_alpha" : "92",
                          "_cell_angle_beta"  : "90",
                          "_cell_angle_gamma" : "90"}}
        self.assertEqual(cf.get_unitcell(cif, "data"), "\t\ta  5.12\n\t\tb  6.34\n\t\tc  7.56\n\t\tal 92")

        cif = { "data" : {"_cell_length_a" : "6.3399",
                          "_cell_length_b" : "6.34",
                          "_cell_length_c" : "6.34",
                          "_cell_angle_alpha" : "90",
                          "_cell_angle_beta"  : "90",
                          "_cell_angle_gamma" : "90"}}
        self.assertEqual(cf.get_unitcell(cif, "data"), "\t\ta  6.3399\n\t\tb  6.34\n\t\tc  6.34\n\t\tal 90\n\t\tbe 90\n\t\tga 90")


    def test_get_unitcell2(self):
        cif = { "data" : {"_cell_length_a" : "5.12(3)",
                          "_cell_length_b" : "6.34",
                          "_cell_length_c" : "7.56",
                          "_cell_angle_alpha" : "90.12(4)",
                          "_cell_angle_beta"  : "95.34",
                          "_cell_angle_gamma" : "100.56"}}
        self.assertEqual(cf.get_unitcell2(cif, "data"), "\t\ta 5.12 b 6.34 c 7.56\n\t\tal 90.12 be 95.34 ga 100.56")

    def test_get_atom_sites_string(self):
        cif = { "data" : {"_atom_site_label" : ["O-H1"],
                          "_atom_site_fract_x" : ["0.123(4)"],
                          "_atom_site_fract_y" : ["0.66667"],
                          "_atom_site_fract_z" : ["0"],
                          "_atom_site_type_symbol"  : ["O2-"],
                          "_atom_site_occupancy" : ["0.75"]}}
        self.assertEqual(cf.get_atom_sites_string(cif, "data"),
                          "\t\tsite O-H1 num_posns 0\tx 0.123 y =2/3; z 0 occ O-2 0.75 beq 1.\n")

        cif = { "data" : {"_atom_site_label" : ["O-H1"],
                          "_atom_site_fract_x" : ["0.123(4)"],
                          "_atom_site_fract_y" : ["0.66667"],
                          "_atom_site_fract_z" : ["0"],
                          "_atom_site_occupancy" : ["0.75"]}}
        self.assertEqual(cf.get_atom_sites_string(cif, "data"),
                          "\t\tsite O-H1 num_posns 0\tx 0.123 y =2/3; z 0 occ O 0.75 beq 1.\n")

        cif = { "data" : {"_atom_site_label" : ["O-H1", "Na1"],
                          "_atom_site_fract_x" : ["0.123(4)", "0.34567"],
                          "_atom_site_fract_y" : ["0.66667", "-0.343444"],
                          "_atom_site_fract_z" : ["0", "-0.0033"],
                          "_atom_site_B_iso_or_equiv" : [".", "0.23"],
                          "_atom_site_occupancy" : ["0.75", "1."]}}
        self.assertEqual(cf.get_atom_sites_string(cif, "data"),
                          "\t\tsite O-H1 num_posns 0\tx 0.123   y  =2/3;    z  0      occ O  0.75 beq 1.  \n"+\
                          "\t\tsite Na1  num_posns 0\tx 0.34567 y -0.343444 z -0.0033 occ Na 1.   beq 0.23\n")


    def test_get_beq(self):
        cif = { "data" : {"_atom_site_label" : ["O-H1", "Na1", "H"],
                          "_atom_site_B_iso_or_equiv" : [".", "0.23", "0"]}}
        self.assertEqual(cf.get_beq(cif, "data"), ['1.', '0.23', '1.'])

        cif = { "data" : {"_atom_site_label" : ["O-H1", "Na1", "H"],
                          "_atom_site_U_iso_or_equiv" : [".", "0.23", "0"]}}
        self.assertEqual(cf.get_beq(cif, "data"), ['1.', '18.16', '1.'])

        cif = { "data" : {"_atom_site_label" : ["O-H1", "Na1"],
                          "_atom_site_aniso_label" : ["O-H1", "Na1"],
                          "_atom_site_aniso_B_11" : ["1.2", "2.3(3)"],
                          "_atom_site_aniso_B_22" : ["1.4", "2.5"],
                          "_atom_site_aniso_B_33" : ["1.5", "2.6"]}}
        self.assertEqual(cf.get_beq(cif, "data"), ['1.367', '2.467'])

        cif = { "data" : {"_atom_site_label" : ["O-H1", "Na1"],
                          "_atom_site_aniso_label" : ["O-H1", "Na1"],
                          "_atom_site_aniso_B_11" : ["1.2", "2.3(3)"],
                          "_atom_site_aniso_B_22" : ["1.4", "2.5"],
                          "_atom_site_aniso_B_33" : ["1.5", "2.6"],
                          "_atom_site_aniso_U_11" : ["1.2", "2.3(3)"],
                          "_atom_site_aniso_U_22" : ["1.4", "2.5"],
                          "_atom_site_aniso_U_33" : ["1.5", "2.6"]}}
        self.assertEqual(cf.get_beq(cif, "data"), ['1.367', '2.467'])

        cif = { "data" : {"_atom_site_label" : ["O-H1", "Na1"],
                          "_atom_site_B_iso_or_equiv" : ["0.23", "."],
                          "_atom_site_aniso_label" : ["Na1"],
                          "_atom_site_aniso_B_11" : ["2.3(3)"],
                          "_atom_site_aniso_B_22" : ["2.5"],
                          "_atom_site_aniso_B_33" : ["2.6"]}}
        self.assertEqual(cf.get_beq(cif, "data"), ['0.23', '2.467'])

        cif = { "data" : {"_atom_site_label" : ["O-H1", "Na1"],
                          "_atom_site_B_iso_or_equiv" : ["0.23", "2.5"],
                          "_atom_site_aniso_label" : ["Na1"],
                          "_atom_site_aniso_B_11" : ["2.3(3)"],
                          "_atom_site_aniso_B_22" : ["2.5"],
                          "_atom_site_aniso_B_33" : ["2.6"]}}
        self.assertEqual(cf.get_beq(cif, "data"), ['0.23', '2.5'])


    def test_make_b_dict(self):
        cif = { "data" : {"_atom_site_label" : ["O-H1", "Na1", "H"],
                          "_atom_site_B_iso_or_equiv" : [".", "0.23", "0"]}}
        self.assertEqual(cf.make_b_dict(cif, "data", "b_iso"), {'Na1': '0.23', 'H': '0'})

        cif = { "data" : {"_atom_site_label" : ["O-H1", "Na1", "H"],
                          "_atom_site_B_iso_or_equiv" : [".", "0.23", "0"]}}
        self.assertEqual(cf.make_b_dict(cif, "data", "u_iso"), {})

        cif = { "data" : {"_atom_site_label" : ["O-H1", "Na1", "H"],
                          "_atom_site_U_iso_or_equiv" : [".", "0.23", "0"]}}
        self.assertEqual(cf.make_b_dict(cif, "data", "u_iso"), {'Na1': '18.16', 'H': '0.0'})

        cif = { "data" : {"_atom_site_label" : ["O-H1", "Na1"],
                          "_atom_site_aniso_label" : ["O-H1", "Na1"],
                          "_atom_site_aniso_B_11" : ["1.2", "2.3(3)"],
                          "_atom_site_aniso_B_22" : ["1.4", "2.5"],
                          "_atom_site_aniso_B_33" : ["1.5", "2.6"]}}
        self.assertEqual(cf.make_b_dict(cif, "data", "b_aniso"), {'O-H1': '1.367', 'Na1': '2.467'})

        cif = { "data" : {"_atom_site_label" : ["O-H1", "Na1"],
                          "_atom_site_aniso_label" : ["Na1", "O-H1"],
                          "_atom_site_aniso_B_11" :  ["2.3(3)", "1.2"],
                          "_atom_site_aniso_B_22" :  ["2.5", "1.4"],
                          "_atom_site_aniso_B_33" :  ["2.6", "1.5"]}}
        self.assertEqual(cf.make_b_dict(cif, "data", "b_aniso"), {'O-H1': '1.367', 'Na1': '2.467'})

        cif = { "data" : {"_atom_site_label" : ["O-H1", "Na1"],
                          "_atom_site_aniso_label" : ["O-H1", "Na1"],
                          "_atom_site_aniso_U_11" : ["1.2", "2.3(3)"],
                          "_atom_site_aniso_U_22" : ["1.4", "2.5"],
                          "_atom_site_aniso_U_33" : ["1.5", "2.6"]}}
        self.assertEqual(cf.make_b_dict(cif, "data", "u_aniso"), {'O-H1': '107.908', 'Na1': '194.76'})
        self.assertRaises(ValueError, cf.make_b_dict, cif, "data", "blah")


    def test_get_b_iso(self):
        cif = { "data" : {"_atom_site_B_iso_or_equiv" : [".", "0.23", "0.53(3)", "?"]}}
        self.assertEqual(cf.get_b_iso(cif, "data"), [None, "0.23", "0.53", None])

        cif = { "data" : {"_something_different" : [".", "0.23", "0.53(3)", "?"]}}
        self.assertRaises(KeyError, cf.get_b_iso, cif, "data")


    def test_get_u_iso(self):
        cif = { "data" : {"_atom_site_U_iso_or_equiv" : [".", "0.0023", "0.053(3)", "?"]}}
        self.assertEqual(cf.get_u_iso(cif, "data"), [None, '0.182', '4.185', None])

        cif = { "data" : {"_something_different" : [".", "0.0023", "0.053(3)", "?"]}}
        self.assertRaises(KeyError, cf.get_u_iso, cif, "data")


    def test_get_b_aniso(self):
        cif = { "data" : {"_atom_site_aniso_B_11" : ["1.2", "2.3(3)"],
                          "_atom_site_aniso_B_22" : ["1.4", "2.5"],
                          "_atom_site_aniso_B_33" : ["1.5", "2.6"]}}
        self.assertEqual(cf.get_b_aniso(cif, "data"), ['1.367', '2.467'])

        cif = { "data" : {"_something_different"  : ["1.2", "2.3(3)"],
                          "_atom_site_aniso_B_22" : ["1.4", "2.5"],
                          "_atom_site_aniso_B_33" : ["1.5", "2.6"]}}
        self.assertRaises(KeyError, cf.get_b_aniso, cif, "data")


    def test_get_u_aniso(self):
        cif = { "data" : {"_atom_site_aniso_U_11" : ["1.2", "2.3(3)"],
                          "_atom_site_aniso_U_22" : ["1.4", "2.5"],
                          "_atom_site_aniso_U_33" : ["1.5", "2.6"]}}
        self.assertEqual(cf.get_u_aniso(cif, "data"), ['107.908', '194.76'])

        cif = { "data" : {"_something_different"  : ["1.2", "2.3(3)"],
                          "_atom_site_aniso_U_22" : ["1.4", "2.5"],
                          "_atom_site_aniso_U_33" : ["1.5", "2.6"]}}
        self.assertRaises(KeyError, cf.get_u_aniso, cif, "data")


if __name__ == "__main__":
    unittest.main()
