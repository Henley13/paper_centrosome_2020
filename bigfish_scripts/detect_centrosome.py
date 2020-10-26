# -*- coding: utf-8 -*-
# Author: Arthur Imbert <arthur.imbert.pro@gmail.com>
# License: BSD 3 clause

"""
Detect centrosomes spots in the GFP images.
"""

import os
import argparse

from utils import check_directories, initialize_script, end_script
from loader import get_fov_names
import bigfish.stack as stack
import bigfish.detection as detection
import bigfish.plot as plot

import numpy as np


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
                        help="Threshold to discriminate centrosomes.",
                        type=int,
                        default=-1)

    # initialize parameters
    args = parser.parse_args()
    input_directory = args.input_directory
    output_directory = args.output_directory
    centrosome_directory = os.path.join(output_directory,
                                        "detected_centrosomes")
    plot_directory = os.path.join(output_directory, "plot",
                                  "centrosome_detection")
    experiment = args.experiment
    log_directory = args.log_directory
    threshold = args.threshold

    # check directories exists
    check_directories([input_directory, output_directory, centrosome_directory,
                       plot_directory, log_directory])

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
    psf_z_gfp = None
    psf_yx_gfp = 300

    print("Spot detection...", "\n")

    # read gfp images
    images = []
    filenames = []
    fov_names_generator = get_fov_names(experiment)
    for i, fov_name in enumerate(fov_names_generator):
        filename = "{0}".format(fov_name)
        filenames.append(filename)
        print("\r", filename)

        # read image
        plate = fov_name.split("_")[0]
        if plate in ["4", "5", "6"]:
            path = os.path.join(input_directory,
                                "{0}_640.tif".format(fov_name))
        else:
            path = os.path.join(input_directory,
                                "{0}_488.tif".format(fov_name))
        gfp = stack.read_image(path)
        images.append(gfp)
        nb_images += 1

    # detect spots
    if threshold != -1:
        spots = detection.detect_spots(
            images,
            threshold=threshold,
            voxel_size_z=voxel_size_z,
            voxel_size_yx=voxel_size_yx,
            psf_z=psf_z_gfp,
            psf_yx=psf_yx_gfp)
    else:
        spots, threshold = detection.detect_spots(
            images,
            return_threshold=True,
            voxel_size_z=voxel_size_z,
            voxel_size_yx=voxel_size_yx,
            psf_z=psf_z_gfp,
            psf_yx=psf_yx_gfp)
    print()
    print("\r threshold: {0}".format(threshold), "\n")

    print("Clustering and postprocessing...", "\n")

    # process all images from the experiment
    for i in range(nb_images):
        image = images[i]
        spots_ = spots[i]
        filename = filenames[i]
        print("\r", filename)

        # decompose clusters
        spots_post_decomposition, _, _ = detection.decompose_cluster(
            image, spots_,
            voxel_size_z=voxel_size_z,
            voxel_size_yx=voxel_size_yx,
            psf_z=psf_z_gfp,
            psf_yx=psf_yx_gfp,
            alpha=0.7,  # alpha impacts the number of spots per cluster
            beta=1)  # beta impacts the number of detected clusters

        # detect centrosomes
        centrosomes_post_clustering, foci_centrosome = detection.detect_foci(
            spots_post_decomposition,
            voxel_size_z=voxel_size_z,
            voxel_size_yx=voxel_size_yx,
            radius=1000,
            nb_min_spots=2)
        centrosomes = np.concatenate(
            (centrosomes_post_clustering[
             centrosomes_post_clustering[:, 2] == -1, :2],
             foci_centrosome[:, :2]),
            axis=0)

        # save centrosomes
        path = os.path.join(centrosome_directory, "{0}.npy".format(filename))
        stack.save_array(centrosomes, path)

        # plot
        image_contrasted = stack.rescale(image, channel_to_stretch=0)
        path = os.path.join(plot_directory, "{0}.png".format(filename))
        plot.plot_detection(image_contrasted,
                            spots=centrosomes,
                            shape="polygon",
                            radius=15,
                            color="orange",
                            linewidth=2,
                            framesize=(15, 15),
                            title="threshold: {0} | centrosomes: {1}".format(
                                threshold, len(centrosomes)),
                            path_output=path,
                            show=False)

    print()

    print("Number of images: {0}".format(nb_images))
    end_script(start_time)
