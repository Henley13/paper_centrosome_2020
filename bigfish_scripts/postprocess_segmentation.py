# -*- coding: utf-8 -*-
# Author: Arthur Imbert <arthur.imbert.pro@gmail.com>
# License: BSD 3 clause

"""
Format cell and nuclei segmentation results.
"""

import os
import argparse

import numpy as np

from utils import check_directories, initialize_script, end_script
from loader import get_fov_names

import bigfish.stack as stack
import bigfish.segmentation as segmentation
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
    experiment = args.experiment
    input_directory = args.input_directory
    output_directory = args.output_directory
    nuc_directory = os.path.join(output_directory, "nuc", experiment)
    cell_directory = os.path.join(output_directory, "cell", experiment)
    nuc_mask_directory = os.path.join(output_directory, "segmented_nuc")
    cell_mask_directory = os.path.join(output_directory, "segmented_cell")
    plot_directory = os.path.join(output_directory, "plot")
    nuc_plot_directory = os.path.join(plot_directory, "nuc_segmentation")
    cell_plot_directory = os.path.join(plot_directory, "cell_segmentation")
    segmentation_plot_directory = os.path.join(plot_directory, "segmentation")
    log_directory = args.log_directory

    # check directories exists
    check_directories([input_directory, output_directory, nuc_directory,
                       cell_directory, nuc_mask_directory, cell_mask_directory,
                       plot_directory, nuc_plot_directory, cell_plot_directory,
                       segmentation_plot_directory])

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

        # read original images
        path = os.path.join(input_directory, "{0}_405.tif".format(fov_name))
        nuc = stack.read_image(path)
        plate = fov_name.split("_")[0]
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

        # contrast FISH channel
        rna_contrasted = stack.rescale(rna, channel_to_stretch=0)

        # read segmentation results
        path = os.path.join(nuc_directory, "{0}_cp_masks.png"
                            .format(fov_name))
        nuc_label = stack.read_image(path).astype(np.int64)
        path = os.path.join(cell_directory, "{0}_cp_masks.png"
                            .format(fov_name))
        cell_label = stack.read_image(path).astype(np.int64)

        # postprocessing
        nuc_label = segmentation.clean_segmentation(nuc_label,
                                                    small_object_size=None,
                                                    fill_holes=True,
                                                    smoothness=1,
                                                    delimit_instance=True)
        cell_label = segmentation.clean_segmentation(cell_label,
                                                     small_object_size=None,
                                                     fill_holes=True,
                                                     smoothness=1,
                                                     delimit_instance=True)
        nuc_label, cell_label = segmentation.match_nuc_cell(nuc_label,
                                                            cell_label)

        # save segmentation results
        path = os.path.join(nuc_mask_directory, "{0}.png".format(filename))
        stack.save_image(nuc_label, path)
        path = os.path.join(cell_mask_directory, "{0}.png".format(filename))
        stack.save_image(cell_label, path)

        # plot
        path = os.path.join(nuc_plot_directory, "{0}.png".format(filename))
        plot.plot_segmentation(nuc, nuc_label,
                               rescale=True, title=fov_name,
                               path_output=path, ext="png", show=False)
        path = os.path.join(cell_plot_directory, "{0}.png".format(filename))
        plot.plot_segmentation(cell, cell_label,
                               rescale=True, title=fov_name,
                               path_output=path, show=False)
        path = os.path.join(segmentation_plot_directory,
                            "{0}.png".format(filename))
        plot.plot_segmentation_boundary(rna_contrasted, cell_label, nuc_label,
                                        title=fov_name, path_output=path,
                                        show=False)

        nb_images += 1

    print()

    print("Number of images: {0}".format(nb_images))
    end_script(start_time)
