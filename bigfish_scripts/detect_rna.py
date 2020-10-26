# -*- coding: utf-8 -*-
# Author: Arthur Imbert <arthur.imbert.pro@gmail.com>
# License: BSD 3 clause

"""
Detect mRNAs spots in the smFISH images.
"""

import os
import argparse

from utils import check_directories, initialize_script, end_script
from loader import get_fov_names
import bigfish.stack as stack
import bigfish.detection as detection
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
    parser.add_argument("--threshold",
                        help="Threshold to discriminate spots.",
                        type=int,
                        default=-1)

    # initialize parameters
    args = parser.parse_args()
    input_directory = args.input_directory
    output_directory = args.output_directory
    spot_directory = os.path.join(output_directory, "detected_spots")
    foci_directory = os.path.join(output_directory, "detected_foci")
    plot_directory = os.path.join(output_directory, "plot", "spot_detection")
    experiment = args.experiment
    log_directory = args.log_directory
    threshold = args.threshold

    # check directories exists
    check_directories([input_directory, output_directory, spot_directory,
                       foci_directory, plot_directory, log_directory])

    # initialize script
    start_time = initialize_script(log_directory, experiment)
    nb_images = 0
    print("Images are saved with the pattern plate_well_gene_drug_fov")
    print()

    # parameters
    plate = experiment.split("_")[0]
    if plate in ["4", "5", "6"]:
        voxel_size_z = None
        voxel_size_yx = 206
    else:
        voxel_size_z = None
        voxel_size_yx = 103
    psf_z = None
    psf_yx = 150

    # compute radius
    (radius_yx, _) = detection.get_radius(
        voxel_size_z, voxel_size_yx, psf_z, psf_yx)

    # read smfish images
    fov_names_generator = get_fov_names(experiment)
    for i, fov_name in enumerate(fov_names_generator):
        filename = "{0}".format(fov_name)
        print("\r", filename)

        # read image
        path = os.path.join(input_directory, "{0}_561.tif".format(fov_name))
        rna = stack.read_image(path)

        # detect spots
        if threshold != -1:
            spots = detection.detect_spots(
                rna,
                threshold=threshold,
                voxel_size_z=voxel_size_z,
                voxel_size_yx=voxel_size_yx,
                psf_z=psf_z,
                psf_yx=psf_yx)
        else:
            spots, threshold = detection.detect_spots(
                rna,
                return_threshold=True,
                voxel_size_z=voxel_size_z,
                voxel_size_yx=voxel_size_yx,
                psf_z=psf_z,
                psf_yx=psf_yx)
        print("\r threshold: {0}".format(threshold), "\n")

        # decompose clusters
        spots_post_decomposition, _, _ = detection.decompose_cluster(
            rna, spots,
            voxel_size_z=voxel_size_z,
            voxel_size_yx=voxel_size_yx,
            psf_z=psf_z,
            psf_yx=psf_yx,
            alpha=0.7,  # alpha impacts the number of spots per cluster
            beta=1)  # beta impacts the number of detected clusters

        # detect foci
        clustered_spots, foci = detection.detect_foci(
            spots_post_decomposition,
            voxel_size_z=voxel_size_z,
            voxel_size_yx=voxel_size_yx,
            radius=350,
            nb_min_spots=4)

        # save spots and foci
        path = os.path.join(spot_directory, "{0}.npy".format(filename))
        stack.save_array(clustered_spots, path)
        path = os.path.join(foci_directory, "{0}.npy".format(filename))
        stack.save_array(foci, path)

        # plot
        rna_contrasted = stack.rescale(rna, channel_to_stretch=0)
        path = os.path.join(plot_directory, "{0}.png".format(filename))
        plot.plot_detection(rna_contrasted,
                            spots=[clustered_spots[:, :2], foci[:, :2]],
                            shape=["circle", "polygon"],
                            radius=[radius_yx, radius_yx * 3],
                            color=["red", "blue"],
                            linewidth=[1, 2],
                            fill=[False, False],
                            framesize=(15, 15),
                            title="threshold: {0} | spots: {1}".format(
                                threshold, len(clustered_spots)),
                            path_output=path,
                            show=False)

        nb_images += 1

    print()

    print("Number of images: {0}".format(nb_images))
    end_script(start_time)
