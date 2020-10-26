# -*- coding: utf-8 -*-
# Author: Arthur Imbert <arthur.imbert.pro@gmail.com>
# License: BSD 3 clause

"""
Plot results at the cell level.
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
    experiment = args.experiment
    input_directory = args.input_directory
    output_directory = args.output_directory
    extraction_directory = os.path.join(output_directory, "extracted_cell")
    plot_directory = os.path.join(output_directory, "plot")
    extraction_plot_directory = os.path.join(plot_directory, "cell_extraction")
    dataframe_directory = os.path.join(output_directory,
                                       "dataframes_extraction")
    log_directory = args.log_directory

    # check directories exists
    check_directories([input_directory, output_directory, extraction_directory,
                       plot_directory, extraction_plot_directory,
                       dataframe_directory])

    # initialize script
    start_time = initialize_script(log_directory, experiment)
    nb_cells = 0
    print("Cells are saved with the pattern plate_well_gene_drug_fov_cell")
    print()

    # process images
    fov_names_generator = get_fov_names(experiment)
    for i, fov_name in enumerate(fov_names_generator):
        filename = "{0}".format(fov_name)
        print("\r", filename)

        # load fov dataframe
        path = os.path.join(dataframe_directory, "{0}.csv".format(fov_name))
        df_fov = stack.read_dataframe_from_csv(path)

        # read cell results
        cells_id = sorted(list(df_fov.loc[:, "cell_id"]))
        cells_id = [str(int(i)) for i in cells_id]
        for cell_id in cells_id:
            path = os.path.join(extraction_directory, "{0}_{1}.npz"
                                .format(fov_name, cell_id))
            cell_results = stack.read_cell_extracted(path)

            # contrast image
            rna = cell_results["smfish"]
            rna_contrasted = stack.rescale(rna, channel_to_stretch=0)

            # plot cell results
            path = os.path.join(extraction_plot_directory, "{0}_{1}.png"
                                .format(filename, cell_id))
            plot.plot_cell(
                ndim=2,
                cell_coord=cell_results["cell_coord"],
                nuc_coord=cell_results["nuc_coord"],
                rna_coord=cell_results["rna_coord"],
                foci_coord=cell_results["foci"],
                other_coord=cell_results["centrosomes"],
                image=rna_contrasted,
                cell_mask=cell_results["cell_mask"],
                nuc_mask=cell_results["nuc_mask"],
                title="{0}_{1}".format(fov_name, cell_id),
                path_output=path)

        nb_cells += 1

    print()

    print("Number of cells: {0}".format(nb_cells))
    end_script(start_time)
