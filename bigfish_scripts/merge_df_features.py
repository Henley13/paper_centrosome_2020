# -*- coding: utf-8 -*-
# Author: Arthur Imbert <arthur.imbert.pro@gmail.com>
# License: BSD 3 clause

"""
Merge dataframes from features computation step.
"""

import os
import argparse

import pandas as pd

from utils import check_directories, initialize_script, end_script
from loader import get_experiments, get_fov_names

import bigfish.stack as stack
import bigfish.classification as classification


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
    input_directory = args.input_directory
    output_directory = args.output_directory
    dataframe_directory = os.path.join(output_directory, "dataframes_features")
    log_directory = args.log_directory

    # check directories exists
    check_directories([input_directory, output_directory, dataframe_directory])

    # initialize script
    start_time = initialize_script(log_directory)
    nb_dataframes = 0
    print("Dataframes are saved with the pattern plate_well_gene_drug_fov")
    print()

    # initialize final dataframe
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
    df_features = pd.DataFrame(columns=all_feature_names)

    # concatenate dataframes
    experiment_generator = get_experiments()
    for experiment in experiment_generator:
        fov_names_generator = get_fov_names(experiment)
        for fov_name in fov_names_generator:

            # load dataframe
            path = os.path.join(dataframe_directory,
                                "{0}.csv".format(fov_name))
            df_fov = stack.read_dataframe_from_csv(path)
            print("\r {0}: {1}".format(fov_name, df_fov.shape))

            # concatenate dataframes
            df_features = pd.concat([df_features, df_fov])

            nb_dataframes += 1

    # save final dataframe
    df_features.reset_index(drop=True, inplace=True)
    path = os.path.join(output_directory, "dataframe_features.csv")
    stack.save_data_to_csv(df_features, path)

    print()
    print("Shape of the final dataframe: {0}".format(df_features.shape))
    print("Columns:")
    columns_name = df_features.columns
    for col in columns_name:
        print("\t", col)

    print()
    print("Done ({0} dataframes)!".format(nb_dataframes), "\n")

    # read extraction dataframe
    path = os.path.join(output_directory, "dataframe_extraction.csv")
    df_extraction = pd.read_csv(path, sep=';', encoding="utf-8")
    print("Shape of the extraction dataframe: {0}".format(df_extraction.shape))

    # merge dataframes
    df = pd.merge(left=df_extraction, right=df_features,
                  how='inner', on=["cell_name"])
    path = os.path.join(output_directory, "merged.csv")
    df.reset_index(drop=True, inplace=True)
    stack.save_data_to_csv(df, path)

    print()
    print("Shape of the merged dataframe: {0}".format(df.shape))
    print("Columns:")
    columns_name = df.columns
    for col in columns_name:
        print("\t", col)

    end_script(start_time)
