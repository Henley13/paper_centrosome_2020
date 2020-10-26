# -*- coding: utf-8 -*-
# Author: Arthur Imbert <arthur.imbert.pro@gmail.com>
# License: BSD 3 clause

"""
Gather detection and segmentation results and extract them at the cell level.
"""

import os
import argparse

from utils import check_directories, initialize_script, end_script
from loader import get_fov_names

import bigfish.stack as stack


def get_cell_name(row):
    """Build cell name from FoV name and cell id."""

    cell_name = "{0}_{1}".format(row["fov_name"], int(row["cell_id"]))

    return cell_name


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
    parser.add_argument("experiment",
                        help="Name of the experiment.",
                        type=str)
    parser.add_argument("--log_directory",
                        help="Path of the log directory.",
                        type=str,
                        default="/Users/arthur/output/2020_adham/log")

    # initialize parameters
    args = parser.parse_args()
    experiment = args.experiment
    input_directory = args.input_directory
    output_directory = args.output_directory
    nuc_mask_directory = os.path.join(output_directory, "segmented_nuc")
    cell_mask_directory = os.path.join(output_directory, "segmented_cell")
    spot_directory = os.path.join(output_directory, "detected_spots")
    foci_directory = os.path.join(output_directory, "detected_foci")
    centrosome_directory = os.path.join(output_directory,
                                        "detected_centrosomes")
    dataframe_directory = os.path.join(output_directory,
                                       "dataframes_extraction")
    final_directory = os.path.join(output_directory, "extracted_cell")
    log_directory = args.log_directory

    # check directories exists
    check_directories([input_directory, output_directory, nuc_mask_directory,
                       cell_mask_directory, spot_directory, foci_directory,
                       centrosome_directory, dataframe_directory,
                       final_directory])

    # initialize script
    start_time = initialize_script(log_directory, experiment)
    nb_images = 0
    print("Images are saved with the pattern plate_well_gene_drug_fov")
    print()

    # process images
    fov_names_generator = get_fov_names(experiment)
    for i, fov_name in enumerate(fov_names_generator):
        filename = "{0}".format(fov_name)
        print("\r", filename)

        # get information from FoV name
        x = fov_name.split("_")
        plate = x[0]
        well = x[1]
        gene = x[2]
        treatment = x[3]
        fov = int(x[4])

        # read original images
        path = os.path.join(input_directory, "{0}_405.tif".format(fov_name))
        nuc = stack.read_image(path)
        if plate in ["4", "5", "6"]:
            path = os.path.join(input_directory,
                                "{0}_640.tif".format(fov_name))
        else:
            path = os.path.join(input_directory,
                                "{0}_488.tif".format(fov_name))
        gfp = stack.read_image(path)
        # if plate in ["4", "5", "6"]:
        #     path = os.path.join(input_directory,
        #                         "{0}_488.tif".format(fov_name))
        # else:
        #     path = os.path.join(input_directory,
        #                         "{0}_640.tif".format(fov_name))
        path = os.path.join(input_directory, "{0}_640.tif".format(fov_name))
        cell = stack.read_image(path)
        path = os.path.join(input_directory, "{0}_561.tif".format(fov_name))
        rna = stack.read_image(path)

        # read segmentation results
        path = os.path.join(nuc_mask_directory, "{0}.png".format(fov_name))
        nuc_label = stack.read_image(path)
        path = os.path.join(cell_mask_directory, "{0}.png".format(fov_name))
        cell_label = stack.read_image(path)

        # read detection results
        path = os.path.join(spot_directory, "{0}.npy".format(fov_name))
        spots = stack.read_array(path)
        path = os.path.join(foci_directory, "{0}.npy".format(fov_name))
        foci = stack.read_array(path)
        path = os.path.join(centrosome_directory, "{0}.npy".format(fov_name))
        centrosomes = stack.read_array(path)

        # extract results at the cell level
        fov_results = stack.extract_cell(
            cell_label=cell_label,
            ndim=2,
            nuc_label=nuc_label,
            rna_coord=spots,
            others_coord={"foci": foci, "centrosomes": centrosomes},
            image=rna,
            others_image={"dapi": nuc, "gfp": gfp,
                          "cellmask": cell, "smfish": rna})

        # summarize fov results
        df = stack.summarize_extraction_results(
            fov_results, ndim=2)

        # save an empty dataframe if no cell are detected
        if len(df) == 0:
            path = os.path.join(dataframe_directory,
                                "{0}.csv".format(filename))
            stack.save_data_to_csv(df, path)
            print("\t dataframe shape: {0}".format(df.shape))
            nb_images += 1
            continue

        # complete fov dataframe with experiment metadata
        n = len(df)
        df.loc[:, "fov_name"] = [fov_name] * n
        df.loc[:, "plate"] = [plate] * n
        df.loc[:, "well"] = [well] * n
        df.loc[:, "gene"] = [gene] * n
        df.loc[:, "treatment"] = [treatment] * n
        df.loc[:, "fov"] = [fov] * n

        if plate in ["4", "5", "6"]:
            cell_line = "bac"
        else:
            cell_line = "endogenous"
        df.loc[:, "cell_line"] = [cell_line] * n

        if plate in ["3a", "3b", "5", "6"]:
            treatment_duration = "10mn"
        else:
            treatment_duration = "5mn"
        df.loc[:, "treatment_duration"] = [treatment_duration] * n

        if plate in ["1a", "1b", "4"]:
            temperature = "ambient"
        else:
            temperature = "controlled"
        df.loc[:, "temperature"] = [temperature] * n

        # build cell_name
        df.loc[:, "cell_name"] = df.apply(get_cell_name, axis=1)

        # cast dataframe columns to the proper dtypes
        df = df.astype({"cell_id": "str",
                        "fov_name": "str",
                        "cell_name": "str",
                        "plate": "str",
                        "well": "str",
                        "gene": "str",
                        "treatment": "str",
                        "fov": "str",
                        "cell_line": "str",
                        "treatment_duration": "str",
                        "temperature": "str"})

        # save fov dataframe
        path = os.path.join(dataframe_directory, "{0}.csv".format(filename))
        stack.save_data_to_csv(df, path)
        print("\t dataframe shape: {0}".format(df.shape))

        # save cell results
        for cell_results in fov_results:
            cell_id = cell_results["cell_id"]
            path = os.path.join(final_directory, "{0}_{1}.npz"
                                .format(filename, cell_id))
            stack.save_cell_extracted(cell_results, path)

        nb_images += 1

    print()

    print("Number of images: {0}".format(nb_images))
    end_script(start_time)
