# -*- coding: utf-8 -*-
# Author: Arthur Imbert <arthur.imbert.pro@gmail.com>
# License: BSD 3 clause

"""
Plot contrasted MIP images.
"""

import os
import argparse

from utils import check_directories, initialize_script, end_script
from loader import get_fov_names
import bigfish.stack as stack
import bigfish.plot as plot


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
    experiment = args.experiment
    log_directory = args.log_directory

    # check directories exists
    check_directories([input_directory, output_directory, log_directory])

    # initialize script
    start_time = initialize_script(log_directory, experiment)
    nb_images = 0
    print("Images are saved with the pattern plate_well_gene_drug_fov_channel")
    print()

    # read image
    fov_names_generator = get_fov_names(experiment)
    for i, fov_name in enumerate(fov_names_generator):
        for channel in ["405", "488", "561", "640"]:
            filename = "{0}_{1}".format(fov_name, channel)
            print("\r", filename)

            # read image
            path = os.path.join(input_directory, filename + ".tif")
            image = stack.read_image(path)

            # save plot
            image = stack.rescale(image, channel_to_stretch=0)
            path_output = os.path.join(output_directory, filename + ".png")
            plot.plot_images(
                image,
                titles=filename,
                framesize=(8, 8),
                remove_frame=True,
                path_output=path_output,
                show=False)
            nb_images += 1

    print()

    print("Number of images: {0}".format(nb_images))
    end_script(start_time)
