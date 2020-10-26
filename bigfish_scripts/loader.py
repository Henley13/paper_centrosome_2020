# -*- coding: utf-8 -*-
# Author: Arthur Imbert <arthur.imbert.pro@gmail.com>
# License: BSD 3 clause

"""
Parse files and read images.
"""

import bigfish.stack as stack


# parameters
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

    "_C02_HMMR_Untreated",
    "_C03_HMMR_Untreated",
    "_C04_HMMR_Untreated",
    "_C05_ASPM_Untreated",
    "_C06_ASPM_Untreated",
    "_C07_ASPM_Untreated",
    "_C08_NUMA1_Untreated",
    "_C09_NUMA1_Untreated",
    "_C10_NUMA1_Untreated",

    "_D02_HMMR_Puro",
    "_D03_HMMR_Puro",
    "_D04_HMMR_Puro",
    "_D05_ASPM_Puro",
    "_D06_ASPM_Puro",
    "_D07_ASPM_Puro",
    "_D08_NUMA1_Puro",
    "_D09_NUMA1_Puro",
    "_D10_NUMA1_Puro",

    "_E02_HMMR_Puro",
    "_E03_HMMR_Puro",
    "_E04_HMMR_Puro",
    "_E05_ASPM_Puro",
    "_E06_ASPM_Puro",
    "_E07_ASPM_Puro",
    "_E08_NUMA1_Puro",
    "_E09_NUMA1_Puro",
    "_E10_NUMA1_Puro",

    "_F02_HMMR_CHX",
    "_F03_HMMR_CHX",
    "_F04_HMMR_CHX",
    "_F05_ASPM_CHX",
    "_F06_ASPM_CHX",
    "_F07_ASPM_CHX",
    "_F08_NUMA1_CHX",
    "_F09_NUMA1_CHX",
    "_F10_NUMA1_CHX",

    "_G02_HMMR_CHX",
    "_G03_HMMR_CHX",
    "_G04_HMMR_CHX",
    "_G05_ASPM_CHX",
    "_G06_ASPM_CHX",
    "_G07_ASPM_CHX",
    "_G08_NUMA1_CHX",
    "_G09_NUMA1_CHX",
    "_G10_NUMA1_CHX"]

# plate_1a 16
# plate_1b 25
# plate_2 25
# plate_3a 25
# plate_3b 16
# plate_4 16
# plate_5 16
# plate_6 16


def get_all_fov_names(plate="all", channel=None):
    # check parameters
    stack.check_parameter(plate=str,
                          channel=(str, type(None)))
    if plate == "all":
        plates = ["1a", "1b", "2", "3a", "3b", "4", "5", "6"]
    elif plate in ["1a", "1b", "2", "3a", "3b", "4", "5", "6"]:
        plates = [plate]
    else:
        raise ValueError("'plate' should be '1a', '1b', '2', '3a', '3b', '4', "
                         "'5', '6' or 'all', not {0}".format(plate))

    # build filename
    for plate in plates:
        if plate == "1a":
            n_fov = 16
            new_labels = new_labels_1

        elif plate == "1b":
            n_fov = 25
            new_labels = new_labels_1

        elif plate == "2":
            n_fov = 25
            new_labels = new_labels_2

        elif plate == "3a":
            n_fov = 25
            new_labels = new_labels_3

        elif plate == "3b":
            n_fov = 16
            new_labels = new_labels_3

        elif plate == "4":
            n_fov = 16
            new_labels = new_labels_4

        elif plate == "5":
            n_fov = 16
            new_labels = new_labels_5

        else:
            n_fov = 16
            new_labels = new_labels_6

        for new_label in new_labels:
            well = new_label.split("_")[1].lower()
            gene = new_label.split("_")[2].lower()
            drug = new_label.split("_")[3].lower()

            for fov in range(1, n_fov + 1):

                if channel is None:
                    filename = "{0}_{1}_{2}_{3}_{4}".format(
                        plate, well, gene, drug, fov)
                elif channel in ["405", "488", "561", "640"]:
                    filename = "{0}_{1}_{2}_{3}_{4}_{5}".format(
                        plate, well, gene, drug, fov, channel)
                else:
                    raise ValueError("'channel' should be among '405', '488', "
                                     "'561' or '640', not {0}".format(plate))

                yield filename


def get_experiments(plate="all"):
    # check parameters
    stack.check_parameter(plate=str)
    if plate == "all":
        plates = ["1a", "1b", "2", "3a", "3b", "4", "5", "6"]
    elif plate in ["1a", "1b", "2", "3a", "3b", "4", "5", "6"]:
        plates = [plate]
    else:
        raise ValueError("'plate' should be '1a', '1b', '2', '3a', '3b', '4', "
                         "'5', '6' or 'all', not {0}".format(plate))

    # build filename
    for plate in plates:

        # get new labels
        if plate in ["1a", "1b"]:
            new_labels = new_labels_1
        elif plate == "2":
            new_labels = new_labels_2
        elif plate in ["3a", "3b"]:
            new_labels = new_labels_3
        elif plate == "4":
            new_labels = new_labels_4
        elif plate == "5":
            new_labels = new_labels_5
        else:
            new_labels = new_labels_6

        # get experiment name
        for new_label in new_labels:
            well = new_label.split("_")[1].lower()
            gene = new_label.split("_")[2].lower()
            drug = new_label.split("_")[3].lower()
            experiment = "{0}_{1}_{2}_{3}".format(plate, well, gene, drug)

            yield experiment


def get_fov_names(experiment):
    plate = experiment.split("_")[0].lower()

    # get number of FoV
    if plate in ["1a", "3b", "4", "5", "6"]:
        n_fov = 16
    else:
        n_fov = 25

    # build fov_name
    for fov in range(1, n_fov + 1):
        fov_name = "{0}_{1}".format(experiment, fov)

        yield fov_name


if __name__ == "__main__":
    print()

    # initialize script
    nb_images = 0

    # generate filenames
    experiments = get_experiments()
    for i, experiment in enumerate(experiments):
        plate = experiment.split("_")[0]
        if plate in ["4", "5", "6"]:
            cell_diameter = 110
            nuc_diameter = 70
        else:
            cell_diameter = 220
            nuc_diameter = 140
        print(i + 1, experiment, -1, -1, nuc_diameter, cell_diameter)
        nb_images += 1

    print()

    print("Number of experiments: {0}".format(nb_images))
