# -*- coding: utf-8 -*-
# Author: Arthur Imbert <arthur.imbert.pro@gmail.com>
# License: BSD 3 clause

"""
Prepare CellMask images for cells segmentation.
"""

import os
import argparse
import shutil

from utils import check_directories, initialize_script, end_script
from loader import get_fov_names
import bigfish.stack as stack


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
    input_directory = args.input_directory
    output_directory = args.output_directory
    final_directory = os.path.join(output_directory, "cell")
    experiment = args.experiment
    log_directory = args.log_directory

    # check directories exists
    check_directories([input_directory, output_directory, final_directory,
                       log_directory])

    # initialize script
    start_time = initialize_script(log_directory, experiment)
    nb_images = 0
    print("Images are saved with the pattern plate_well_gene_drug_fov")
    print()

    # create experiment directory
    experiment_directory = os.path.join(final_directory, experiment)
    if os.path.exists(experiment_directory):
        shutil.rmtree(experiment_directory)
    os.mkdir(experiment_directory)

    # read cellmask channel
    fov_names_generator = get_fov_names(experiment)
    for i, fov_name in enumerate(fov_names_generator):
        filename = "{0}".format(fov_name)
        print("\r", filename)

        # read image
        plate = fov_name.split("_")[0]
        # if plate in ["4", "5", "6"]:
        #     path = os.path.join(input_directory,
        #                         "{0}_488.tif".format(fov_name))
        # else:
        #     path = os.path.join(input_directory,
        #                         "{0}_640.tif".format(fov_name))
        path = os.path.join(input_directory, "{0}_640.tif".format(fov_name))
        cell = stack.read_image(path)

        # save image
        path = os.path.join(experiment_directory, filename + ".tif")
        stack.save_image(cell, path)

        nb_images += 1

    print()

    print("Number of images: {0}".format(nb_images))
    end_script(start_time)
