# -*- coding: utf-8 -*-
# Author: Arthur Imbert <arthur.imbert.pro@gmail.com>
# License: BSD 3 clause

"""
Compute features.
"""

import os
import argparse

from utils import check_directories, initialize_script, end_script
from loader import get_fov_names

import bigfish.stack as stack
import bigfish.classification as classification

import pandas as pd


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
    extraction_directory = os.path.join(output_directory, "extracted_cell")
    dataframe_extraction_directory = os.path.join(output_directory,
                                                  "dataframes_extraction")
    dataframe_features_directory = os.path.join(output_directory,
                                                "dataframes_features")
    log_directory = args.log_directory

    # check directories exists
    check_directories([input_directory, output_directory, extraction_directory,
                       dataframe_extraction_directory,
                       dataframe_features_directory])

    # initialize script
    start_time = initialize_script(log_directory, experiment)
    nb_images = 0
    print("Images are saved with the pattern plate_well_gene_drug_fov")
    print()

    # parameter
    plate = experiment.split("_")[0]
    if plate in ["4", "5", "6"]:
        voxel_size_yx = 206
    else:
        voxel_size_yx = 103

    # get features name
    feature_names = classification.get_features_name(
        names_features_distance=False,
        names_features_intranuclear=False,
        names_features_protrusion=False,
        names_features_dispersion=False,
        names_features_topography=False,
        names_features_foci=False,
        names_features_area=False,
        names_features_centrosome=True)
    all_feature_names = feature_names + ["cell_name"]

    # process images
    fov_names_generator = get_fov_names(experiment)
    for i, fov_name in enumerate(fov_names_generator):
        filename = "{0}".format(fov_name)
        print("\r", filename)

        # initialize features dataframe
        df_features = pd.DataFrame(columns=all_feature_names)

        # load cell extraction dataframe for the related experience
        path = os.path.join(dataframe_extraction_directory, fov_name + ".csv")
        df_extraction = pd.read_csv(path, sep=';', encoding="utf-8")

        # save an empty dataframe if no cell are segmented
        if len(df_extraction) == 0:
            path = os.path.join(dataframe_features_directory,
                                "{0}.csv".format(filename))
            stack.save_data_to_csv(df_features, path)
            print("\t dataframe shape: {0}".format(df_features.shape))
            continue

        # loop over segmented cells
        cell_names = list(df_extraction.loc[:, "cell_name"])
        for cell_name in cell_names:

            # get cell id
            cell_id = cell_name.split("_")[-1]

            # read extracted results
            path = os.path.join(extraction_directory, cell_name + ".npz")
            data = stack.read_cell_extracted(path)
            cell_mask = data["cell_mask"]
            nuc_mask = data["nuc_mask"]
            rna_coord = data["rna_coord"]
            centrosome_coord = data["centrosomes"]
            smfish = data["smfish"]

            # compute features
            features = classification.compute_features(
                cell_mask, nuc_mask, ndim=2, rna_coord=rna_coord,
                smfish=smfish, voxel_size_yx=voxel_size_yx,
                centrosome_coord=centrosome_coord,
                compute_distance=False,
                compute_intranuclear=False,
                compute_protrusion=False,
                compute_dispersion=False,
                compute_topography=False,
                compute_foci=False,
                compute_area=False,
                compute_centrosome=True)
            features = features.reshape((1, -1))

            # build dataframe
            df_cell = pd.DataFrame(data=features, columns=feature_names)
            df_cell.loc[:, "cell_name"] = [cell_name] * len(df_cell)

            # concatenate dataframes
            df_features = pd.concat([df_features, df_cell])

        # cast dataframe columns to the proper dtypes
        df_features = df_features.astype({"cell_name": "str"})

        # save fov dataframe
        path = os.path.join(dataframe_features_directory,
                            "{0}.csv".format(filename))
        stack.save_data_to_csv(df_features, path)
        print("\t dataframe shape: {0}".format(df_features.shape))

        nb_images += 1

    print()

    print("Number of images: {0}".format(nb_images))
    end_script(start_time)
