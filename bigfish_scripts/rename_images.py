# -*- coding: utf-8 -*-
# Author: Arthur Imbert <arthur.imbert.pro@gmail.com>
# License: BSD 3 clause

"""
Rename and organize raw images.
"""

import os
import shutil
import argparse

from utils import check_directories, initialize_script, end_script


# parameters
old_labels = [
    "r02c02", "r02c03", "r02c04", "r02c05", "r02c06",
    "r02c07", "r02c08", "r02c09", "r02c10", "r02c11",
    "r03c02", "r03c03", "r03c04", "r03c05", "r03c06",
    "r03c07", "r03c08", "r03c09", "r03c10", "r03c11",
    "r04c02", "r04c03", "r04c04", "r04c05", "r04c06",
    "r04c07", "r04c08", "r04c09", "r04c10", "r04c11",
    "r05c02", "r05c03", "r05c04", "r05c05", "r05c06",
    "r05c07", "r05c08", "r05c09", "r05c10", "r05c11",
    "r06c02", "r06c03", "r06c04", "r06c05", "r06c06",
    "r06c07", "r06c08", "r06c09", "r06c10", "r06c11",
    "r07c02", "r07c03", "r07c04", "r07c05", "r07c06",
    "r07c07", "r07c08", "r07c09", "r07c10", "r07c11"]

new_labels_1 = [
    "_B02_BICD2_CHX",
    "_B03_PCNT_CHX",
    "_B04_NIN_CHX",
    "_B05_CCDC88C_CHX",
    "_B06_NIN_CHX",
    "_B07_CEP350_CHX",
    "_B08_DYNC1H1_CHX",
    "_B09_KIF1C_CHX",
    "_B10_TRIM59_CHX",
    "_B11_TTBK2_CHX",

    "_C02_BICD2_CHX",
    "_C03_PCNT_CHX",
    "_C04_NIN_CHX",
    "_C05_CCDC88C_CHX",
    "_C06_NIN_CHX",
    "_C07_CEP350_CHX",
    "_C08_DYNC1H1_CHX",
    "_C09_KIF1C_CHX",
    "_C10_TRIM59_CHX",
    "_C11_TTBK2_CHX",

    "_D02_BICD2_Untreated",
    "_D03_PCNT_Untreated",
    "_D04_NIN_Untreated",
    "_D05_CCDC88C_Untreated",
    "_D06_NIN_Untreated",
    "_D07_CEP350_Untreated",
    "_D08_DYNC1H1_Untreated",
    "_D09_KIF1C_Untreated",
    "_D10_TRIM59_Untreated",
    "_D11_TTBK2_Untreated",

    "_E02_BICD2_Untreated",
    "_E03_PCNT_Untreated",
    "_E04_NIN_Untreated",
    "_E05_CCDC88C_Untreated",
    "_E06_NIN_Untreated",
    "_E07_CEP350_Untreated",
    "_E08_DYNC1H1_Untreated",
    "_E09_KIF1C_Untreated",
    "_E10_TRIM59_Untreated",
    "_E11_TTBK2_Untreated",

    "_F02_BICD2_Puro",
    "_F03_PCNT_Puro",
    "_F04_NIN_Puro",
    "_F05_CCDC88C_Puro",
    "_F06_NIN_Puro",
    "_F07_CEP350_Puro",
    "_F08_DYNC1H1_Puro",
    "_F09_KIF1C_Puro",
    "_F10_TRIM59_Puro",
    "_F11_TTBK2_Puro",

    "_G02_BICD2_Puro",
    "_G03_PCNT_Puro",
    "_G04_NIN_Puro",
    "_G05_CCDC88C_Puro",
    "_G06_NIN_Puro",
    "_G07_CEP350_Puro",
    "_G08_DYNC1H1_Puro",
    "_G09_KIF1C_Puro",
    "_G10_TRIM59_Puro",
    "_G11_TTBK2_Puro"]

new_labels_2 = [
    "_B02_BICD2_Untreated",
    "_B03_PCNT_Untreated",
    "_B04_NIN_Untreated",
    "_B05_CEP350_Untreated",
    "_B06_CCDC88C_Untreated",
    "_B07_TRIM59_Untreated",
    "_B08_TTBK2_Untreated",
    "_B09_CCDC88C_Untreated",
    "_B10_TRIM59_Untreated",
    "_B11_TMEM237_Untreated",

    "_C02_BICD2_Untreated",
    "_C03_PCNT_Untreated",
    "_C04_NIN_Untreated",
    "_C05_CEP350_Untreated",
    "_C06_CCDC88C_Untreated",
    "_C07_TRIM59_Untreated",
    "_C08_TTBK2_Untreated",
    "_C09_CCDC88C_Untreated",
    "_C10_TRIM59_Untreated",
    "_C11_NUMA1_Untreated",

    "_D02_BICD2_Puro",
    "_D03_PCNT_Puro",
    "_D04_NIN_Puro",
    "_D05_CEP350_Puro",
    "_D06_CCDC88C_Puro",
    "_D07_TRIM59_Puro",
    "_D08_TTBK2_Puro",
    "_D09_CCDC88C_Puro",
    "_D10_TRIM59_Puro",
    "_D11_TMEM237_Puro",

    "_E02_BICD2_Puro",
    "_E03_PCNT_Puro",
    "_E04_NIN_Puro",
    "_E05_CEP350_Puro",
    "_E06_CCDC88C_Puro",
    "_E07_TRIM59_Puro",
    "_E08_TTBK2_Puro",
    "_E09_CCDC88C_Puro",
    "_E10_TRIM59_Puro",
    "_E11_NUMA1_Puro",

    "_F02_BICD2_CHX",
    "_F03_PCNT_CHX",
    "_F04_NIN_CHX",
    "_F05_CEP350_CHX",
    "_F06_CCDC88C_CHX",
    "_F07_TRIM59_CHX",
    "_F08_TTBK2_CHX",
    "_F09_CCDC88C_CHX",
    "_F10_TRIM59_CHX",
    "_F11_TMEM237_CHX",

    "_G02_BICD2_CHX",
    "_G03_PCNT_CHX",
    "_G04_NIN_CHX",
    "_G05_CEP350_CHX",
    "_G06_CCDC88C_CHX",
    "_G07_TRIM59_CHX",
    "_G08_TTBK2_CHX",
    "_G09_CCDC88C_CHX",
    "_G10_TRIM59_CHX",
    "_G11_NUMA1_CHX"]

new_labels_3 = [
    "_B02_BICD2_Untreated",
    "_B03_PCNT_Untreated",
    "_B04_NIN_Untreated",
    "_B05_CEP350_Untreated",
    "_B06_CCDC88C_Untreated",
    "_B07_TRIM59_Untreated",
    "_B08_TTBK2_Untreated",
    "_B09_CCDC88C_Untreated",
    "_B10_TRIM59_Untreated",
    "_B11_TMEM237_Untreated",

    "_C02_BICD2_Untreated",
    "_C03_PCNT_Untreated",
    "_C04_NIN_Untreated",
    "_C05_CEP350_Untreated",
    "_C06_CCDC88C_Untreated",
    "_C07_TRIM59_Untreated",
    "_C08_TTBK2_Untreated",
    "_C09_CCDC88C_Untreated",
    "_C10_TRIM59_Untreated",
    "_C11_NUMA1_Untreated",

    "_D02_BICD2_Puro",
    "_D03_PCNT_Puro",
    "_D04_NIN_Puro",
    "_D05_CEP350_Puro",
    "_D06_CCDC88C_Puro",
    "_D07_TRIM59_Puro",
    "_D08_TTBK2_Puro",
    "_D09_CCDC88C_Puro",
    "_D10_TRIM59_Puro",
    "_D11_TMEM237_Puro",

    "_E02_BICD2_Puro",
    "_E03_PCNT_Puro",
    "_E04_NIN_Puro",
    "_E05_CEP350_Puro",
    "_E06_CCDC88C_Puro",
    "_E07_TRIM59_Puro",
    "_E08_TTBK2_Puro",
    "_E09_CCDC88C_Puro",
    "_E10_TRIM59_Puro",
    "_E11_NUMA1_Puro",

    "_F02_BICD2_CHX",
    "_F03_PCNT_CHX",
    "_F04_NIN_CHX",
    "_F05_CEP350_CHX",
    "_F06_CCDC88C_CHX",
    "_F07_TRIM59_CHX",
    "_F08_TTBK2_CHX",
    "_F09_CCDC88C_CHX",
    "_F10_TRIM59_CHX",
    "_F11_TMEM237_CHX",

    "_G02_BICD2_CHX",
    "_G03_PCNT_CHX",
    "_G04_NIN_CHX",
    "_G05_CEP350_CHX",
    "_G06_CCDC88C_CHX",
    "_G07_TRIM59_CHX",
    "_G08_TTBK2_CHX",
    "_G09_CCDC88C_CHX",
    "_G10_TRIM59_CHX",
    "_G11_NUMA1_CHX"]

new_labels_4 = [
    "_B02_HMMR_Untreated",
    "_B03_ASPM_Untreated",
    "_B04_NUMA1_Untreated",
    "_B05_POLR2A_Untreated",
    "_B06_NINL_Untreated",
    "_B07_A1catenine_Untreated",
    "_B08_B1catenine_Untreated",
    "_B09_golgi20_Untreated",
    "_B10_golgi30_Untreated",
    "_B11_golgi40_Untreated",

    "_C02_HMMR_Untreated",
    "_C03_ASPM_Untreated",
    "_C04_NUMA1_Untreated",
    "_C05_POLR2A_Untreated",
    "_C06_NINL_Untreated",
    "_C07_A1catenine_Untreated",
    "_C08_B1catenine_Untreated",
    "_C09_golgi20_Untreated",
    "_C10_golgi30_Untreated",
    "_C11_golgi40_Untreated",

    "_D02_HMMR_Puro",
    "_D03_ASPM_Puro",
    "_D04_NUMA1_Puro",
    "_D05_POLR2A_Puro",
    "_D06_NINL_Puro",
    "_D07_A1catenine_Puro",
    "_D08_B1catenine_Puro",
    "_D09_golgi20_Untreated",
    "_D10_golgi30_Untreated",
    "_D11_golgi40_Untreated",

    "_E02_HMMR_Puro",
    "_E03_ASPM_Puro",
    "_E04_NUMA1_Puro",
    "_E05_POLR2A_Puro",
    "_E06_NINL_Puro",
    "_E07_A1catenine_Puro",
    "_E08_B1catenine_Puro",
    "_E09_unknown_Untreated",
    "_E10_unknown_Untreated",
    "_E11_unknown_Untreated",

    "_F02_HMMR_CHX",
    "_F03_ASPM_CHX",
    "_F04_NUMA1_CHX",
    "_F05_POLR2A_CHX",
    "_F06_NINL_CHX",
    "_F07_A1catenine_CHX",
    "_F08_B1catenine_CHX",
    "_F09_unknown_Untreated",
    "_F10_unknown_Untreated",
    "_F11_unknown_Untreated",

    "_G02_HMMR_CHX",
    "_G03_ASPM_CHX",
    "_G04_NUMA1_CHX",
    "_G05_POLR2A_CHX",
    "_G06_NINL_CHX",
    "_G07_A1catenine_CHX",
    "_G08_B1catenine_CHX",
    "_G09_unknown_Untreated",
    "_G10_unknown_Untreated",
    "_G11_unknown_Untreated"]

new_labels_5 = [
    "_B02_HMMR_Untreated",
    "_B03_HMMR_Untreated",
    "_B04_ASPM_Untreated",
    "_B05_ASPM_Untreated",
    "_B06_NUMA1_Untreated",
    "_B07_NUMA1_Untreated",
    "_B08_GORASP2_Untreated",
    "_B09_unknown_Untreated",
    "_B10_unknown_Untreated",
    "_B11_unknown_Untreated",

    "_C02_HMMR_Untreated",
    "_C03_HMMR_Untreated",
    "_C04_ASPM_Untreated",
    "_C05_ASPM_Untreated",
    "_C06_NUMA1_Untreated",
    "_C07_NUMA1_Untreated",
    "_C08_GORASP2_Untreated",
    "_C09_unknown_Untreated",
    "_C10_unknown_Untreated",
    "_C11_unknown_Untreated",

    "_D02_HMMR_Puro",
    "_D03_HMMR_Puro",
    "_D04_ASPM_Puro",
    "_D05_ASPM_Puro",
    "_D06_NUMA1_Puro",
    "_D07_NUMA1_Puro",
    "_D08_GORASP2_Puro",
    "_D09_unknown_Untreated",
    "_D10_unknown_Untreated",
    "_D11_unknown_Untreated",

    "_E02_HMMR_Puro",
    "_E03_HMMR_Puro",
    "_E04_ASPM_Puro",
    "_E05_ASPM_Puro",
    "_E06_NUMA1_Puro",
    "_E07_NUMA1_Puro",
    "_E08_GORASP2_Puro",
    "_E09_unknown_Untreated",
    "_E10_unknown_Untreated",
    "_E11_unknown_Untreated",

    "_F02_HMMR_CHX",
    "_F03_HMMR_CHX",
    "_F04_ASPM_CHX",
    "_F05_ASPM_CHX",
    "_F06_NUMA1_CHX",
    "_F07_NUMA1_CHX",
    "_F08_unknown_Untreated",
    "_F09_unknown_Untreated",
    "_F10_unknown_Untreated",
    "_F11_unknown_Untreated",

    "_G02_HMMR_CHX",
    "_G03_HMMR_CHX",
    "_G04_ASPM_CHX",
    "_G05_ASPM_CHX",
    "_G06_NUMA1_CHX",
    "_G07_NUMA1_CHX",
    "_G08_unknown_Untreated",
    "_G09_unknown_Untreated",
    "_G10_unknown_Untreated",
    "_G11_unknown_Untreated"]

new_labels_6 = [
    "_B02_HMMR_Untreated",
    "_B03_HMMR_Untreated",
    "_B04_HMMR_Untreated",
    "_B05_ASPM_Untreated",
    "_B06_ASPM_Untreated",
    "_B07_ASPM_Untreated",
    "_B08_NUMA1_Untreated",
    "_B09_NUMA1_Untreated",
    "_B10_NUMA1_Untreated",
    "_B11_unknown_Untreated",

    "_C02_HMMR_Untreated",
    "_C03_HMMR_Untreated",
    "_C04_HMMR_Untreated",
    "_C05_ASPM_Untreated",
    "_C06_ASPM_Untreated",
    "_C07_ASPM_Untreated",
    "_C08_NUMA1_Untreated",
    "_C09_NUMA1_Untreated",
    "_C10_NUMA1_Untreated",
    "_C11_unknown_Untreated",

    "_D02_HMMR_Puro",
    "_D03_HMMR_Puro",
    "_D04_HMMR_Puro",
    "_D05_ASPM_Puro",
    "_D06_ASPM_Puro",
    "_D07_ASPM_Puro",
    "_D08_NUMA1_Puro",
    "_D09_NUMA1_Puro",
    "_D10_NUMA1_Puro",
    "_D11_unknown_Untreated",

    "_E02_HMMR_Puro",
    "_E03_HMMR_Puro",
    "_E04_HMMR_Puro",
    "_E05_ASPM_Puro",
    "_E06_ASPM_Puro",
    "_E07_ASPM_Puro",
    "_E08_NUMA1_Puro",
    "_E09_NUMA1_Puro",
    "_E10_NUMA1_Puro",
    "_E11_unknown_Untreated",

    "_F02_HMMR_CHX",
    "_F03_HMMR_CHX",
    "_F04_HMMR_CHX",
    "_F05_ASPM_CHX",
    "_F06_ASPM_CHX",
    "_F07_ASPM_CHX",
    "_F08_NUMA1_CHX",
    "_F09_NUMA1_CHX",
    "_F10_NUMA1_CHX",
    "_F11_unknown_Untreated",

    "_G02_HMMR_CHX",
    "_G03_HMMR_CHX",
    "_G04_HMMR_CHX",
    "_G05_ASPM_CHX",
    "_G06_ASPM_CHX",
    "_G07_ASPM_CHX",
    "_G08_NUMA1_CHX",
    "_G09_NUMA1_CHX",
    "_G10_NUMA1_CHX",
    "_G11_unknown_Untreated"]

old_fovs_4x4 = ["01", "02", "03", "04", "05", "06", "07", "08",
                "09", "10", "11", "12", "13", "14", "15", "16"]

new_fovs_4x4 = ["16", "01", "02", "03", "04", "08", "07", "06",
                "05", "09", "10", "11", "12", "15", "14", "13"]

old_fovs_5x5 = ["01", "02", "03", "04", "05",
                "06", "07", "08", "09", "10",
                "11", "12", "13", "14", "15",
                "16", "17", "18", "19", "20",
                "21", "22", "23", "24", "25"]

new_fovs_5x5 = ["16", "01", "02", "03", "04",
                "05", "10", "09", "08", "07",
                "06", "11", "12", "13", "14",
                "15", "20", "19", "18", "17",
                "21", "22", "23", "24", "25"]


if __name__ == "__main__":
    print()

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_directory",
                        help="Path of the input directory.",
                        type=str)
    parser.add_argument("output_directory",
                        help="Path of the output directory.",
                        type=str)
    parser.add_argument("--log_directory",
                        help="Path of the log directory.",
                        type=str,
                        default="/Users/arthur/output/2020_adham/log")

    # initialize parameters
    args = parser.parse_args()
    input_directory_ = args.input_directory
    output_directory = args.output_directory
    log_directory = args.log_directory
    input_directory_plate_1a = os.path.join(input_directory_, "plate_1a/MIP")
    input_directory_plate_1b = os.path.join(input_directory_, "plate_1b/MIP")
    input_directory_plate_2 = os.path.join(input_directory_, "plate_2/MIP")
    input_directory_plate_3a = os.path.join(input_directory_, "plate_3a/MIP")
    input_directory_plate_3b = os.path.join(input_directory_, "plate_3b/MIP")
    input_directory_plate_4 = os.path.join(input_directory_, "plate_4/MIP")
    input_directory_plate_5 = os.path.join(input_directory_, "plate_5/MIP")
    input_directory_plate_6 = os.path.join(input_directory_, "plate_6/MIP")

    # check directories exists
    check_directories([input_directory_, output_directory, log_directory,
                       input_directory_plate_1a,
                       input_directory_plate_1b,
                       input_directory_plate_2,
                       input_directory_plate_3a,
                       input_directory_plate_3b,
                       input_directory_plate_4,
                       input_directory_plate_5,
                       input_directory_plate_6])

    # initialize script
    start_time = initialize_script(log_directory)
    nb_images = 0
    print("Images are saved with the pattern plate_well_gene_drug_fov_channel")
    print()

    # ### plate 1a ###
    plate = "1a"
    print("Plate 1a (4x4)", "\n")

    # rename files 4x4
    filenames = os.listdir(input_directory_plate_1a)

    # well level
    for i, old_label in enumerate(old_labels):
        new_label = new_labels_1[i]
        well = new_label.split("_")[1].lower()
        gene = new_label.split("_")[2].lower()
        drug = new_label.split("_")[3].lower()

        # FoV level
        for j, old_fov in enumerate(old_fovs_4x4):
            new_fov = new_fovs_4x4[j]
            fov = int(new_fov)

            # channel level
            for channel in ["405", "488", "561", "640"]:
                old_filename = "{0}f{1}MAX_{2}.tif".format(
                    old_label, old_fov, channel)
                new_filename = "{0}_{1}_{2}_{3}_{4}_{5}.tif".format(
                    plate, well, gene, drug, fov, channel)

                # copy file in a new directory
                path_input = os.path.join(input_directory_plate_1a,
                                          old_filename)
                path_output = os.path.join(output_directory, new_filename)
                print("{0} => {1}".format(old_filename, new_filename))
                shutil.copyfile(path_input, path_output)
                nb_images += 1

    print()

    # ### plate 1b ###
    plate = "1b"
    print("Plate 1b (5x5)", "\n")

    # rename files 5x5
    filenames = os.listdir(input_directory_plate_1b)

    # well level
    for i, old_label in enumerate(old_labels):
        new_label = new_labels_1[i]
        well = new_label.split("_")[1].lower()
        gene = new_label.split("_")[2].lower()
        drug = new_label.split("_")[3].lower()

        # FoV level
        for j, old_fov in enumerate(old_fovs_5x5):
            new_fov = new_fovs_5x5[j]
            fov = int(new_fov)

            # channel level
            for channel in ["405", "488", "561", "640"]:
                old_filename = "{0}f{1}MAX_{2}.tif".format(
                    old_label, old_fov, channel)
                new_filename = "{0}_{1}_{2}_{3}_{4}_{5}.tif".format(
                    plate, well, gene, drug, fov, channel)

                # copy file in a new directory
                path_input = os.path.join(input_directory_plate_1b,
                                          old_filename)
                path_output = os.path.join(output_directory, new_filename)
                print("{0} => {1}".format(old_filename, new_filename))
                shutil.copyfile(path_input, path_output)
                nb_images += 1

    print()

    # ### plate 2 ###
    plate = 2
    print("Plate 2 (5x5)", "\n")

    # rename files 5x5
    filenames = os.listdir(input_directory_plate_2)

    # well level
    for i, old_label in enumerate(old_labels):
        new_label = new_labels_2[i]
        well = new_label.split("_")[1].lower()
        gene = new_label.split("_")[2].lower()
        drug = new_label.split("_")[3].lower()

        # FoV level
        for j, old_fov in enumerate(old_fovs_5x5):
            new_fov = new_fovs_5x5[j]
            fov = int(new_fov)

            # channel level
            for channel in ["405", "488", "561", "640"]:
                old_filename = "{0}f{1}MAX_{2}.tif".format(
                    old_label, old_fov, channel)
                new_filename = "{0}_{1}_{2}_{3}_{4}_{5}.tif".format(
                    plate, well, gene, drug, fov, channel)

                # copy file in a new directory
                path_input = os.path.join(input_directory_plate_2,
                                          old_filename)
                path_output = os.path.join(output_directory, new_filename)
                print("{0} => {1}".format(old_filename, new_filename))
                shutil.copyfile(path_input, path_output)
                nb_images += 1

    print()

    # ### plate 3a ###
    plate = "3a"
    print("Plate 3a (5x5)", "\n")

    # rename files 5x5
    filenames = os.listdir(input_directory_plate_3a)

    # well level
    for i, old_label in enumerate(old_labels):
        new_label = new_labels_3[i]
        well = new_label.split("_")[1].lower()
        gene = new_label.split("_")[2].lower()
        drug = new_label.split("_")[3].lower()

        # FoV level
        for j, old_fov in enumerate(old_fovs_5x5):
            new_fov = new_fovs_5x5[j]
            fov = int(new_fov)

            # channel level
            for channel in ["405", "488", "561", "640"]:
                old_filename = "{0}f{1}MAX_{2}.tif".format(
                    old_label, old_fov, channel)
                new_filename = "{0}_{1}_{2}_{3}_{4}_{5}.tif".format(
                    plate, well, gene, drug, fov, channel)

                # copy file in a new directory
                path_input = os.path.join(input_directory_plate_3a,
                                          old_filename)
                path_output = os.path.join(output_directory, new_filename)
                print("{0} => {1}".format(old_filename, new_filename))
                shutil.copyfile(path_input, path_output)
                nb_images += 1

    print()

    # ### plate 3b ###
    plate = "3b"
    print("Plate 3b (4x4)", "\n")

    # rename files 4x4
    filenames = os.listdir(input_directory_plate_3b)

    # well level
    for i, old_label in enumerate(old_labels):
        new_label = new_labels_3[i]
        well = new_label.split("_")[1].lower()
        gene = new_label.split("_")[2].lower()
        drug = new_label.split("_")[3].lower()

        # FoV level
        for j, old_fov in enumerate(old_fovs_4x4):
            new_fov = new_fovs_4x4[j]
            fov = int(new_fov)

            # channel level
            for channel in ["405", "488", "561", "640"]:
                old_filename = "{0}f{1}MAX_{2}.tif".format(
                    old_label, old_fov, channel)
                new_filename = "{0}_{1}_{2}_{3}_{4}_{5}.tif".format(
                    plate, well, gene, drug, fov, channel)

                # copy file in a new directory
                path_input = os.path.join(input_directory_plate_3b,
                                          old_filename)
                path_output = os.path.join(output_directory, new_filename)
                print("{0} => {1}".format(old_filename, new_filename))
                shutil.copyfile(path_input, path_output)
                nb_images += 1

    print()

    # ### plate 4 ###
    plate = "4"
    print("Plate 4 (4x4)", "\n")

    # rename files 4x4
    filenames = os.listdir(input_directory_plate_4)

    # well level
    for i, old_label in enumerate(old_labels):
        new_label = new_labels_4[i]
        well = new_label.split("_")[1].lower()
        gene = new_label.split("_")[2].lower()
        drug = new_label.split("_")[3].lower()

        # FoV level
        for j, old_fov in enumerate(old_fovs_4x4):
            new_fov = new_fovs_4x4[j]
            fov = int(new_fov)

            # channel level
            for channel in ["405", "488", "561", "640"]:
                old_filename = "{0}f{1}MAX_{2}.tif".format(
                    old_label, old_fov, channel)
                new_filename = "{0}_{1}_{2}_{3}_{4}_{5}.tif".format(
                    plate, well, gene, drug, fov, channel)

                # copy file in a new directory
                path_input = os.path.join(input_directory_plate_4,
                                          old_filename)
                path_output = os.path.join(output_directory, new_filename)
                print("{0} => {1}".format(old_filename, new_filename))
                shutil.copyfile(path_input, path_output)
                nb_images += 1

    print()

    # ### plate 5 ###
    plate = "5"
    print("Plate 5 (4x4)", "\n")

    # rename files 4x4
    filenames = os.listdir(input_directory_plate_5)

    # well level
    for i, old_label in enumerate(old_labels):
        new_label = new_labels_5[i]
        well = new_label.split("_")[1].lower()
        gene = new_label.split("_")[2].lower()
        drug = new_label.split("_")[3].lower()

        # FoV level
        for j, old_fov in enumerate(old_fovs_4x4):
            new_fov = new_fovs_4x4[j]
            fov = int(new_fov)

            # channel level
            for channel in ["405", "488", "561", "640"]:
                old_filename = "{0}f{1}MAX_{2}.tif".format(
                    old_label, old_fov, channel)
                new_filename = "{0}_{1}_{2}_{3}_{4}_{5}.tif".format(
                    plate, well, gene, drug, fov, channel)

                # copy file in a new directory
                path_input = os.path.join(input_directory_plate_5,
                                          old_filename)
                path_output = os.path.join(output_directory, new_filename)
                print("{0} => {1}".format(old_filename, new_filename))
                shutil.copyfile(path_input, path_output)
                nb_images += 1

    print()

    # ### plate 6 ##
    plate = "6"
    print("Plate 6 (4x4)", "\n")

    # rename files 4x4
    filenames = os.listdir(input_directory_plate_6)

    # well level
    for i, old_label in enumerate(old_labels):
        new_label = new_labels_6[i]
        well = new_label.split("_")[1].lower()
        gene = new_label.split("_")[2].lower()
        drug = new_label.split("_")[3].lower()

        # continue if 11th column
        if old_label[3:] == "c11":
            continue

        # FoV level
        for j, old_fov in enumerate(old_fovs_4x4):
            new_fov = new_fovs_4x4[j]
            fov = int(new_fov)

            # channel level
            for channel in ["405", "488", "561", "640"]:
                old_filename = "{0}f{1}MAX_{2}.tif".format(
                    old_label, old_fov, channel)
                new_filename = "{0}_{1}_{2}_{3}_{4}_{5}.tif".format(
                    plate, well, gene, drug, fov, channel)

                # copy file in a new directory
                path_input = os.path.join(input_directory_plate_6,
                                          old_filename)
                path_output = os.path.join(output_directory, new_filename)
                print("{0} => {1}".format(old_filename, new_filename))
                shutil.copyfile(path_input, path_output)
                nb_images += 1

    print()

    print("Number of images: {0}".format(nb_images))
    end_script(start_time)
